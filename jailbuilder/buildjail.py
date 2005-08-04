#!/usr/bin/env python

# Check out the build rpm from ftp://ftp.suse.com/pub/suse/i386/9.3/suse/noarch/build-2005.5.12-0.1.noarch.rpm for ideas how to lay down a jail

# 
# Initialize the rpm database in the jail root
# 
# Get some base packages...
# 
# Resolve all of the dependencies (figure out what packages require, then find what packages provide)  red-carpet libraries may provide this (as well as some yum python bindings)
# 
# install all required users and groups (get this list as we process the rpms) (Doesn't seem to work, may have to install once, capture output of users/groups, and then reinstall with first adding certain users)
# 
# 
# set up resolv.conf
# 
# install rcd/rug
# 
# Add service
# activate the server
# subscribe to the correct channels
# activate the services for red-carpet
# 
# 
# 
# Then, any time a new package is added to the jail, just add the package to the jail definition
# 
# 

# Will be provided a list of rpms for jail

# Need to get the rpms' deps and requirements (might as well do this for all the rpms) (Could be lengthy!)

# Check to make sure the lists' requirements are provided for, and add to the list as needed

# Don't need to worry about other types of package managers (ex: dpkg) because debian have tools to build jails already (not sure how good they are)


import sys
import os
import commands
import re
import string
import tempfile
import shutil
import pdb


class Package:

	# "Static" Members/Methods
	# Being here they only get compiled once
	ignoresource = re.compile("\.(no)?src\.rpm$")
	matchrpm = re.compile("\.rpm$")
	marker = re.compile("^____")
	rpmlib_req = re.compile("^rpmlib(.*)")

	# Remove the versioned portion from a string (provides/requires)
	#  Assuming I can do this here because I'm dealing with a base distro
	def remove_version_req(class_object, string):
		string = string.split(' <= ')[0]
		string = string.split(' >= ')[0]
		string = string.split(' = ' )[0]
		string = string.split(' < ' )[0]
		string = string.split(' > ' )[0]
		return string
	# Make this a 'static' class method... weird?? 
	#supposed to be updated to be simpler syntax... ? first hackish thing I've seen in Python
	#  But there may be a clearer newer syntax I'm not aware of
	remove_version_req = classmethod(remove_version_req)


	def __init__(self, full_path):
		self.full_path = full_path
		self.rpm_filename = os.path.basename(full_path)

		self.provides = []
		self.requires = []

		# collect the users/groups we need to create in the jail (so everything doesn't get created as root)
		self.groups = {}
		self.users = {}

		print full_path

		if self.valid_rpm_name():
			self.load_package_info()


	# rpm base name: NAME
	# provides: PROVIDES
	# requires: REQUIRES
	# users and groups? (FILEGROUPNAME, FILEUSERNAME)
	# Reference website: http://rikers.org/rpmbook/node30.html
	def load_package_info(self):
		(status, output) = commands.getstatusoutput("""rpm -qp --queryformat "____NAME\n%{NAME}\n____ARCH\n%{ARCH}\n____FILELIST\n[%{FILENAMES}\n]" --queryformat "____REQUIRES\n" --requires --queryformat "____PROVIDES\n" --provides """ + self.full_path)
		#(status, output) = commands.getstatusoutput("""rpm --nosignature -qp --queryformat "____NAME\n%{NAME}\n____ARCH\n%{ARCH}\n____FILELIST\n[%{FILENAMES}|%{FILEGROUPNAME}|%{FILEUSERNAME}\n]" --queryformat "____REQUIRES\n" --requires --queryformat "____PROVIDES\n" --provides """ + self.full_path)

		#print output

		for line in output.split("\n"):
			line = line.strip()

			# If this is a marker, set the marker
			if Package.marker.search(line):
				marker = line
			else:
				if marker == "____NAME":
					self.name = line.strip()
				elif marker == "____ARCH":
					self.arch = line.strip()
				elif marker == "____REQUIRES":
					# Ignore 'rpmlib(' requirements (don't know how to find out what the rpm binary provides)
					if not Package.rpmlib_req.search(line):
						line = Package.remove_version_req(line)
						self.requires.append(line)
				elif marker == "____PROVIDES":
					line = Package.remove_version_req(line)
					self.provides.append(line)
				elif marker == "____FILELIST":
					try:
						# We're not collecting users/groups anymore
						#(filename, group, user) = line.split("|")
						#self.provides.append(filename)
						#self.groups[group] = 1
						#self.users[user] = 1
						self.provides.append(line)
					except ValueError:
						print "Line: " + line
						sys.exit(1)
				else:
					print "Unknown marker tag: " + marker
					sys.exit(1)



	def valid_rpm_name(self):

		if Package.matchrpm.search(self.full_path):
			return 1
		else:
			return 0


class Jail:

	def __init__(self, config, path):
		self.config = config
		self.jail_location = os.path.abspath(path)

		if not os.path.exists(self.jail_location):
			print("Target jail location does not exists: %s" % self.jail_location)
			sys.exit(1)

		# These are base names of rpms
		#    for rpm based distros, you must add the rpm dep since we are ignoring rpmlib requirements
		self.orig_required_rpms = config.get_required_rpms()
		self.orig_required_rpms.append("rpm")
		self.required_rpms = []
		self.valid_arch_types = config.get_valid_arch()

		# Get and set environment
		self.environment = self.config.get_environment()

		self.available_rpms = {} # map of rpm_name -> Package object
		self.provide_map = {} # Large map to have quick access to provides

		self.total_requirements = {}  # requirment -> true of false, whether it's been met
		self.requires = {}
		self.provides = {}

		self.users = {}
		self.groups = {}

		self.load_package_cache()

		#print self.provide_map

		# Start collecting/satisfying dependencies
		self.collect_required_packages()

		self.initialize_jail()

		# Do without base accounts... oh well, we'll see if it causes any problems later
		#self.install_base_accounts()

		# Lay down the rpms
		self.install_packages()

		self.post_config()



	# May be able to cache this later to speed things up
	# TODO: load up external rpms as well
	def load_package_cache(self):

		files = os.listdir(self.config.get_rpm_repository_path())
		files.sort()

		for rpm_filename in files:
			my_package = Package(
				os.path.join(self.config.get_rpm_repository_path(), rpm_filename))
				

			# Make sure it's a valid architecture
			#print self.valid_arch_types
			#print my_package.arch
			# TODO What if there are two packages with each a different valid arch?  Probably won't
			#  matter because the packages are going to get updated with rug anyway... (or are they?)

			if self.valid_arch_types.count(my_package.arch):
				self.available_rpms[my_package.name] = my_package

				# Load up dictionary lookup to quickly resolve deps
				for provide in my_package.provides:
					self.provide_map[provide] = my_package.name
			else:
				print "Skipping %s package for arch %s" % (my_package.name, my_package.arch)
				# Don't need this object anymore
				del my_package



	def collect_required_packages(self):
		# Have two data structures: current requires, and current supplied provides (these structures deal with rpms names, not filenames)
		#  Start adding new packages to get rid of the requires list

		# Add initial deps
		for req_rpm in self.orig_required_rpms:
			self.add_package(req_rpm)

		#print "Current requires:"
		#for i in self.requires:
		#	print i


		# Solve remaining deps
		while(len(self.requires)):
			# remove requires that are provides by our current list of packages
			for req in self.requires.keys():
				if self.provides.has_key(req):
					# remove from requires
					self.requires.pop(req)

			# Add a package for each of the remaining requires
			for req in self.requires.keys():
				if self.provide_map.has_key(req):
					self.add_package(self.provide_map[req])
				else:
					print "ERROR!: need requirement '%s' but do not have a package to satisfy it!" % req
					print "\tmake sure you have the correct arch types in valid_arch in your jail config"
					print "Current Distro Hint:"
					(status, output) = commands.getstatusoutput("""rpm -q --whatprovides '%s' """ % req)
					print output
					sys.exit(1)

			#print self.requires
			#print "***provides***"
			#print self.provides

		# When you make it here, you've got all your deps!
		print self.required_rpms
		print self.groups
		print self.users




	# Add package to list of required rpms
	def add_package(self, package_name):

		#pdb.set_trace()

		# Only add the package if it's not there already
		if not self.required_rpms.count(package_name):
			if self.available_rpms.has_key(package_name):
				print "Adding %s to required_rpms" % package_name
				self.required_rpms.append(package_name)
				# Add the requirements
				for req in self.available_rpms[package_name].requires:
					# If it's not already provided, add to list of requires
					if not self.provides.has_key(req):
						self.requires[req] = 1 # don't want duplicates
				for prov in self.available_rpms[package_name].provides:
					self.provides[prov] = 1 # don't want duplicates

				for user in self.available_rpms[package_name].users:
					#print "User:" + user
					self.users[user] = 1 # Don't want duplicates
				for group in self.available_rpms[package_name].groups:
					#print "Group:" + group
					self.groups[group] = 1 # Don't want duplicates

			else:
				print "ERROR!: requesting package %s but do not have %s in available rpms!" % (package_name, package_name)
				sys.exit(1)
		else:
			print "-required_rpms already has " + package_name


	# TODO: the rpm database version (berkeley db) needs to be customized for each jail
	def initialize_jail(self):

		# Blow away the directory
		shutil.rmtree(self.jail_location)
		
		os.makedirs(self.jail_location + os.sep + "var/lib/rpm") # Needed for rpm version 3
		command = """rpm --root %s --initdb""" % self.jail_location
		print command
		(status, output) = commands.getstatusoutput(command)
		if status:
			print "Error initializing the rpm database inside the jail"
			sys.exit(1)

	# Ended up not being needed...	
	def install_base_accounts(self):

		group_count = 1
		user_count = 1

		# Remove root from groups and users
		self.groups.pop("root")
		self.users.pop("root")

		etc_dir = self.jail_location + os.sep + "etc"
		os.mkdir(etc_dir)

		# Create the groups
		group_file = open(etc_dir + os.sep + "group", 'w')
		group_file.write("%s:x:%d:\n" % ( "root", 0))
		for group in self.groups:
			group_file.write("%s:x:%d:\n" % ( group, group_count) )
			group_count += 1
		group_file.close()

		# Create the users
		user_file = open(etc_dir + os.sep + "passwd", 'w')
		user_file.write("%s:x:%d:0:::\n" % ( "root", 0))
		for user in self.users:
			user_file.write("%s:x:%d::::\n" % ( user, user_count))
			user_count += 1
		user_file.close()

		#shadow_file = open(self.jail_location + os.sep + "etc" + os.sep + "shadow", 'w')
		#shadow_file.write("%s:*:%d:0:::::\n" % ( "root", 0))
		#shadow_file.write("%s:*:%d:0:10000::::\n" % ( user, user_count))
		#shadow_file.close()
		
		# convert the shadow accounts
		#commands.getstatusoutput("pwconv -P %s" % etc_dir)


	def install_packages(self):

		# Generate a manifest file (list of rpm files)
		manifest_filename = tempfile.mktemp()
		manifest = open(manifest_filename, 'w')

		for rpm in self.required_rpms:
			path = self.available_rpms[rpm].full_path
			manifest.write(path + "\n")
		manifest.close()

		# This will work (using a manifest filename) as long as you're using rpm version 4 and above
		command = """rpm --root %s -i %s""" % (self.jail_location, manifest_filename)
		print command
		(status, output) = commands.getstatusoutput(command)
		print output
		if status:
			print "Error installing rpms inside the jail!!!"
			print "***Usually this is ok for now***"

		# Copy all required rpms to inside the jail
		package_dir = self.jail_location + os.sep + "jailbuilder"
		os.mkdir(package_dir)

		# Copy the required rpms and write a new manifest file (can't use manifest file on rpm < 4)
		#jail_manifest = open(self.jail_location + os.sep + "jailbuilder" + os.sep + "manifest", 'w')
		rpm_list = ""
		for rpm in self.required_rpms:
			rpm_path = self.available_rpms[rpm].full_path
			shutil.copy(rpm_path, package_dir)
			#jail_manifest.write("jailbuilder" + os.sep + os.path.basename(rpm_path) + "\n")
			rpm_list = rpm_list + " jailbuilder" + os.sep + os.path.basename(rpm_path)
		#jail_manifest.close()

		# Is this ever going to be different for different distros?
		shutil.rmtree(self.jail_location + os.sep + "var/lib/rpm")
		os.mkdir(self.jail_location + os.sep + "var/lib/rpm")
		
		command = "chroot %s env %s rpm --initdb" % (self.jail_location, self.environment)
		print command
		(status, output) = commands.getstatusoutput(command)
		print "Status: %d" % status
		print "Output: " + output
		
		# manifest files don't work on rpm 3 and below...
		#command = "chroot %s env %s rpm --force -U %s" % (self.jail_location, self.environment, "jailbuilder" + os.sep + "manifest")

		# But, this method may be a problem because of the length of the arguments
		command = "chroot %s env %s rpm --force -U %s" % (self.jail_location, self.environment, rpm_list)
		print command
		(status, output) = commands.getstatusoutput(command)
		print "Status: %d" % status
		print "Output: " + output

		# Cleanup...
		os.unlink(manifest_filename)
		shutil.rmtree(self.jail_location + os.sep + "jailbuilder")

		# Remove rpmorig and rpmnew files from the jail
		match_rpmorig = re.compile("rpmorig$")
		match_rpmnew = re.compile("rpmnew$")
		for root, dirs, files in os.walk(self.jail_location):
			for file in files:
				full_path = os.path.join(root, file)
				if match_rpmorig.search(full_path):
					print "Removing: " + full_path
					os.remove(full_path)
				if match_rpmnew.search(full_path):
					# Remove .rpmnew from string
					new_full_path = full_path.replace(".rpmnew", "")
					os.rename(full_path, new_full_path)
					print "Renamed file:" + full_path



	def post_config(self):
		
		# Process resolv.conf
		name_servers = self.config.get_nameservers()
		
		if name_servers:
			resolv_conf = open(os.path.join(self.jail_location, "etc", "resolv.conf"), 'w')
			for server in name_servers:
				resolv_conf.write("nameserver %s\n" % server)
			resolv_conf.close()


		# Process user creation


# This will parse the config file and have values available (probably xml?  could be simpler...)
class Config:

	comment = re.compile("^[\s#]")

	def __init__(self, filename):
		self.setting = {}

		# Load all elements into a dictionary
		for line in open(filename).readlines():
			if not Config.comment.search(line):
				(key, value) = line.split("=", 1)
				self.setting[key] = value.strip()

		
		print self.setting

	def get_setting(self, name):
		if self.setting.has_key(name):
			return self.setting[name]
		else:
			return ""

	def get_rpm_repository_path(self):
		return self.get_setting("rpm_repository_path")

	def get_valid_arch(self):
		return self.get_setting("valid_arch").split()

	def get_required_rpms(self):
		return self.get_setting("required_rpms").split()

	def get_nameservers(self):
		return self.get_setting("nameservers").split()

	def get_environment(self):
		return self.get_setting("environment")


def commandline():
	if len(sys.argv) < 3:
		print "Usage: ./buildjail.py <config_file> <jail_dir>"
		sys.exit(1)
        
	# Collect args
        config_file = sys.argv[1]
        destdir = sys.argv[2]

	print "Are you sure you want to blow away %s and install a jail? [Y/n]" % destdir
	user_input = sys.stdin.readline().strip().lower()
	#print """'%s'""" % user_input
	if user_input == '': user_input = 'y'

	if not user_input[0] == 'n':
		print "Proceeding..."
		jail = Jail(Config(config_file), destdir)
		print "Jail creationg successful!"
	else:
		print "Exiting..."
		sys.exit(0)




# If called from the command line, run main, otherwise, functions are callable through imports
if __name__ == "__main__":
        commandline()
 

