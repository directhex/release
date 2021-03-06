#!/usr/bin/env python

import threading
import sys
import os
import os.path
import time
import re
import signal

# TODO: this need some profiling... it uses too much processor...

# Note: if for some reason you use os.chdir, and try to reload a module in this dir, it won't work!
#  Either don't use os.chdir, or put a full path in here
sys.path.append('../pyutils')

import config
import build
import datastore
import logger
import packaging
import src_repo_utils
import utils

##############################################################
# Tarball thread options

# Don't compress these so we can use "tail -f" (they don't get pushed to a server anyway)
tarball_log = logger.Logger(filename='tarball_builder.log', print_screen=0, compressed=0)

#
##############################################################

##############################################################
# sync thread options
# Use rsync to synchronize the last n builds
sync_log = logger.Logger(filename='sync.log', print_screen=0, compressed=0)

#
##############################################################

##############################################################
# scheduler threads options

version_re = re.compile(".*-(.*).(tar.gz|tar.bz2|zip)")
tarballs = datastore.source_file_repo()
# Set the lock object
tarball_lock = threading.Lock()

scheduler_log = logger.Logger(filename='scheduler.log', print_screen=0, compressed=0)

#
##############################################################

# TODO: CTRL-C is killing mktarball... what's going on? (looks like tarball-builder-daemon didn't work either...? Could it be a python regression?)
class tarball_builder(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.load_info()

	def load_info(self):

		# reload list of packages (allows us to update the list without restarting the daemon)
		reload(config)

		self.td_active = config.td_active

		self.max_poll_interval = config.td_max_poll_interval
		self.network_error_interval = config.td_network_error_interval

		self.num_sequential = config.td_num_sequential

		self.sequential = config.td_sequential

		self.src_repo = src_repo_utils.svn(config.MONO_ROOT, key_file=config.src_key_file)
		self.distfiles = datastore.source_file_repo()

		self.pack_objs = {}
		for pack in config.td_packages:
			self.pack_objs[pack] = packaging.package("", pack)

	def cancelled(self):

		self.load_info()

		if config.td_active and not sigint_event.isSet():
			return False
		else:   
			return True
		

	def run(self):

		tarball_log.log("Tarball creator starting...\n")

		while not self.cancelled():

			start_time = utils.get_time()

			# routinely check for updates (sleep every so often)
			for pack_name, pack_obj in self.pack_objs.iteritems():

				# We are reloading pack_objs, but this for loop won't notice it until we enter it again
				if self.cancelled(): continue

				# get latest version from the tree
				latest_tree_rev = self.src_repo.latest_tree_revision()
				#print "Latest tree rev: %d (%s)" % (latest_tree_rev, pack_name)

				if not latest_tree_rev:
					tarball_log.log("Error getting latest tree rev, trying later... (%s)\n" % pack_name)

					# Restart for loop over...
					break

				# Only do for the last couple of commits, rather than constantly updating a base revision
				if latest_tree_rev <= self.num_sequential:
					starting_rev = 1
				else:   
					starting_rev = latest_tree_rev - self.num_sequential

				# If we're not building each and every checkin, only build the latest
				if not self.sequential:
					starting_rev = latest_tree_rev

				# Pretty much do every commit (for binary search on regressions) (should be adjustable)
				#  The + 1 is so that the latest tree revision will be checked (range func does not include the last number in the sequence)
				for i in range(starting_rev, latest_tree_rev + 1):

					latest_for_package = self.src_repo.latest_path_revision(pack_obj.info['HEAD_PATH'], revision=i)
					if not latest_for_package:
						tarball_log.log("Error getting revision %d, trying later... (%s)\n" % (i, pack_name) )
						# Skip to next pack...
						break

					if not self.distfiles.contains('HEAD', pack_name, str(latest_for_package)) and not self.cancelled():
						command = "cd %s; ./mktarball --snapshot %s %d" % (config.packaging_dir, pack_name, latest_for_package)
						tarball_log.log("Executing: %s\n" % (command) )

						# TODO: the system needs to be smarter about reinstalling the same rpms over and over...

						# This will show console output, but not write to the log
						#  Log will be for brief info, and the console will watch what's currently going on
						  # (For some reason my signal gets ignored if I'm using os.system... seems to work with popen)
						(code, output) = utils.launch_process(command, print_output=0)
						tarball_log.log("Exit code: %d (%s)\n" % (code, pack_name))

						# handle jail busy errors (exit code of 2)
						if code == 2:
							tarball_log.log("Jail busy, retrying later... (%s)\n" % pack_name)

						# handle svn timeouts
						elif code == utils.KILLED_EXIT_CODE:
							tarball_log.log("svn commands killed, retrying later... (%s)\n" % pack_name)

						# Handle failed tarballs...
						elif code:
							tarball_log.log("Tarball creation failed...(%s)\n" %pack_name)

							# Send out the log with the tarball, or at least a link... ?
							link = "http://mono.ximian.com/monobuild/tarball_logs/HEAD/%s/%d.log" % (pack_name, latest_for_package)
							utils.send_mail('wberrier@novell.com', 'wberrier@novell.com', 'mktarball failed (%s %d)' % (pack_name, latest_for_package), "mktarball has failed for package %s revision %d\n\n%s" % (pack_name, latest_for_package, link))

			time_duration = utils.time_duration_asc(start_time, utils.get_time()) * 60

			# Only sleep if this loop was shorter than max_poll_interval
			#  and if we do sleep, discount the time_duration
			if not self.cancelled() and time_duration < self.max_poll_interval:
				#tarball_log.log("Sleeping for %d seconds...\n" % (self.max_poll_interval - time_duration) )
				time.sleep(self.max_poll_interval - time_duration)

		# Exiting because we've been cancelled
		tarball_log.log("Tarball creator shutting down...\n")




class build_scheduler(threading.Thread):

	def __init__(self, distro):
		threading.Thread.__init__(self)

		self.distro = distro

		self.setName(distro)

	# We can unschedule this platform by removing it from the list in pyutils/config.py or turning off the scheduler
	# Reload config info (only useful for sleep times and which packages to build for a distro)
	def cancelled(self):
		# reload python module
		reload(config)

		if config.sd_latest_build_distros.count(self.distro) and config.sd_active and not sigint_event.isSet():
			return False
		else:   
			return True

	def run(self):

		distro = self.distro
		scheduler_log.log("%s:\tStarting scheduler\n" % (distro) )

		while not self.cancelled():

			packages_to_build = []
			for pack_def in config.sd_latest_build_packages:
				pack_obj = packaging.package("", pack_def)
				if pack_obj.valid_build_platform(distro):
					packages_to_build.append(pack_def)

			num_started_builds = 0
			start_time = utils.get_time()

			# Build each package for this jail
			for package_name in packages_to_build:

				# Skip builds so we can exit
				if self.cancelled(): continue

				# Check to see what the latest tarball is
				# The src_file_repo class is not threadsafe, so provide a mutex here
				tarball_lock.acquire()
				try:
					tarball_filename = tarballs.get_latest_tarball("HEAD", package_name)
				except:
					# catch this in case the filename is being edited by hand
					tarball_filename = ""
				tarball_lock.release()

				if not tarball_filename:
					#scheduler_log.log("%s:\t*** Error getting latest tarball (%s) (Probably doesn't exist...)!!!\n" % (distro, package_name) )
					pass

				else:

					#print "Latest tarball: " + tarball_filename

					# Get version
					version, ext = version_re.search(tarball_filename).groups()

					info = datastore.build_info("HEAD", distro, package_name, version)

					# Build if the build doesn't exist already
					if not info.exists:
						command = "cd %s; ./build --suppress_output %s %s %s" % (config.packaging_dir, distro, package_name, version)
						scheduler_log.log("%s:\t%s\n" % (distro, command) )

						num_started_builds += 1
						# TODO: hmm... is this not blocking?  Seems this code continues before being able to run tests?
						(code, output) = utils.launch_process(command, print_output=0)
						# Testing...
						#code = 2

						# Is the jail busy?  if so, just repeat this loop (and select a new tarball if a newer one exists)      
						# Hmm... this really shouldn't happen, as much at least
						if code == 2:
							#scheduler_log.log("%s:\tJail is busy or offline... will retry again (%s)\n" % (distro, package_name) )
							num_started_builds -= 1

						if code == 5:
							scheduler_log.log("%s:\tbuild info is missing, but packages exist... ?? will retry again (%s)\n" % (distro, package_name) )
							num_started_builds -= 1
					else:   
						#scheduler_log.log("%s:\tSkipping existing build (%s, %s)\n" % (distro, package_name, version) )
						pass


			time_duration = utils.time_duration_asc(start_time, utils.get_time() ) * 60
			if num_started_builds == 0 and time_duration < config.sd_wakeup_interval:
				#scheduler_log.log("%s:\tSleeping %d seconds...\n" % (distro, config.sd_wakeup_interval - time_duration) )
				time.sleep(config.sd_wakeup_interval - time_duration)

		# Exiting because we've been removed from the configuration
		scheduler_log.log("%s:\tExiting upon user request...\n" % distro)


# TODO: When CTRL-C is pressed, this should keep running until the other threads stop... ?
class sync(threading.Thread):


	def __init__(self):
		threading.Thread.__init__(self)
		self.load_info()

	def load_info(self):

		# reload options
		reload(config)

		self.sync_active = config.sync_active
		self.sync_host = config.sync_host
		self.sync_target_dir = config.sync_target_dir
		self.sync_num_builds = config.sync_num_builds
		self.sync_sleep_time = config.sync_sleep_time
		self.sync_max_arg_len = config.sync_max_arg_len

	def cancelled(self):
		# Don't shut this thread down until the tarball and build threads are done
		#  Are these vars available across threads?  (if not, we'll have to use a signal)
		# TODO: Cafeful, this thread may not have been started yet
		#   (second check is so you can have the sync daemon running during a release time, when the other daemons are not...)
		if len(build_threads) == 0 and not tarball_thread.isAlive() and not config.sync_active == True:
			return True
		else:
			return False

	def run(self):

		sync_log.log("sync thread starting...\n")

		while not self.cancelled():

			self.load_info()

			# Must base these dirs off 'trunk/release'
			dirs = []

			# Add tarball_map
			dirs += ['packaging/tarball_map']

			# Add config
			dirs += ['pyutils/config.py']

			#sync_log.log(" *** Gathering dirs ***\n")

			# Gather dirs to synchronize
			for i in ['HEAD', 'RELEASE']:
				i_dir = config.build_info_dir + os.sep + i
				if os.path.exists(i_dir):
					for distro in os.listdir(i_dir):
						distro_dir = i_dir + os.sep + distro
						if os.path.exists(distro_dir):
							for component in os.listdir(distro_dir):
								# Get the last 'num_builds' number of elements from the list
								versions = build.get_versions(i, distro, component)[-self.sync_num_builds:]
								for j in versions:
									dirs.append(os.path.join('monobuild/www/builds', i, distro, component, j))

				# Grab latest num_builds for tarball log files as well
				tarball_path = os.path.join(config.build_info_dir, '..', 'tarball_logs', i)
				if os.path.exists(tarball_path):
					for component in os.listdir(tarball_path):
						component_dir = tarball_path + os.sep + component
						versions = utils.version_sort(os.listdir(component_dir))
						for j in versions[-self.sync_num_builds:]:
							dirs.append(os.path.join('monobuild/www/tarball_logs', i, component, j))

			# conduct a dirs string up to the length of the max arg length, and run rsync for each of those blocks (what's the real maximum?)
			while len(dirs):

				dir_string = ""
				counter = 0
				for i in dirs:
					# +1 is for the space char
					if len(i) + 1 + len(dir_string) < self.sync_max_arg_len:
						dir_string += " %s" % i
					else:
						break
					counter +=1

				# Remove counter elements from dirs
				dirs = dirs[counter:]

				#sync_log.log(" *** Syncing ***\n")
				#  For some reason the --delete option crashes when running the second time to go-mono.com and mono.ximian.com ... ?
				# rsync all files over, and don't include the builds... just logs and info.xml
				command = 'cd %s; rsync -avzR -e "ssh %s" --exclude "files/downloads" --exclude "files/*.tar.*" --exclude "files/steps/*/*.tar.*" %s %s:%s' % (config.release_repo_root, config.ssh_options, dir_string, self.sync_host, self.sync_target_dir)
				#sync_log.log(command + "\n")
				status, output = utils.launch_process(command, print_output=0, output_timeout=600)
			
				#sync_log.log(output)
				if status:
					sync_log.log("Error running rsync: " + output)

			#sync_log.log(" *** sync Sleeping ***\n")
			time.sleep(self.sync_sleep_time)

		sync_log.log("sync thread shutting down...\n")


# Signal handler routine
#  This will let the threads finish when CTRL-C is pushed
def keyboard_interrupt(signum, frame):
	print "*** Signaling all threads to finish ***"
	sync_log.log("*** Signaling all threads to finish ***\n")
	sigint_event.set()

# Set up event object
sigint_event = threading.Event()

# Keep track of build threads
build_threads = []

# Set signal handler
signal.signal(signal.SIGINT, keyboard_interrupt)

# Start up mktarball thread (start this thread up first, cause sync looks for it)
tarball_thread = tarball_builder()
tarball_thread.start()

# Start up a sync thread
sync_thread = sync()
sync_thread.start()

# Sleep if threads are still alive
#  Wow... here was the key... the main thread would exit, but pressing ctrl-c would go to the main thread (which had already exited)
#  source: http://groups.google.com/group/comp.lang.python/browse_thread/thread/bb177d4cff9cde4e/d39dbc7e71a897c2?lnk=st&q=threading+sigint+group%3Acomp.lang.python&rnum=4&hl=en#d39dbc7e71a897c2


# Start the threads, as well as allow changes to config.sd_latest_build_distros to start and stop platforms
#  (Main execution counts as a thread)
firstrun = True  # emulate dowhile
while threading.activeCount() > 1 or firstrun:
	firstrun = False
	# Check for newly activated threads
	reload(config)

	# TODO: how to schedule alternate jails?
	for distro in config.sd_latest_build_distros:
		found = False
		for thread in build_threads:
			# If this thread has quit, remove from the list
			# TODO: Could this actually mean the thread is sleeping?  is that how more than 1 thread is getting started??  How to check this better?
			#  TODO: Starting and stopping jails by changing the list is BROKEN!!!
			#  I just saw more than one debian-4-arm thread exit... ????
			if not thread.isAlive():
				build_threads.remove(thread)

			# Found an existing thread, don't start a new one
			elif thread.getName() == distro:
				found = True

		# Start this thread if it isn't running and if sigint hasn't been triggered
		if not found and not sigint_event.isSet() and config.sd_active:
			thread = build_scheduler(distro)
			thread.start()
			build_threads.append(thread)

	# TODO: when ctrl-C is pressed, don't stop the sync thread.  Only stop the sync thread if the td and build threads are done
	# Check if we need to start up the sync thread
	if not sync_thread.isAlive() and not sigint_event.isSet() and config.sync_active:
		sync_thread = sync()
		sync_thread.start()

	# Check if we need to start up the tarball thread
	if not tarball_thread.isAlive() and not sigint_event.isSet() and config.td_active:
		tarball_thread = tarball_builder()
		tarball_thread.start()

	# Wait for threads to die
	time.sleep(5)


# Wrong!!
# This results blocks the main thread (and thus sigint gets ignored)
#for thread in threads:
#       thread.join()

