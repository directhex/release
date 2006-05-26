
import xml.xpath
import xml.dom.minidom
import fcntl
import stat
import os
import glob
import re
import distutils.dir_util

import pdb

import config
import utils

all_rwx = stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU

# Locking wrappers
def lock_file(fd):
	fcntl.flock(fd, fcntl.LOCK_EX)

def unlock_file(fd):
	fcntl.flock(fd.fileno(), fcntl.LOCK_UN)


# tarball datastore

# info for where tarballs are at and what's available
#  any reason for making this file xml?
class source_file_repo:

        def __init__(self):
                self.data_store_filename = config.packaging_dir + os.sep + 'tarball_map'

                # Create the file if it doesn't exist
                #  TODO: does this need locking?
                if not os.path.exists(self.data_store_filename):
                        fd = open(self.data_store_filename, 'w')
                        fd.write("")
                        fd.close()

		# Why are these here?

                # Load file
                self.load_info()

                self.info = {}


        def add_file(self, HEAD_or_RELEASE, package_name, version, filename_path):

                #print "Adding file: %s %s %s %s"  % (package_name, version, snapshot_rev, filename_path)

                self.load_info()
                # Add to structure
                key = ":".join([HEAD_or_RELEASE, package_name, version])
                self.info[key] = filename_path

                # Lock file
                # Write out file
                self.write_info()

        def contains(self, HEAD_or_RELEASE, package_name, version):
                self.load_info()
                return self.info.has_key(":".join([HEAD_or_RELEASE, package_name, version]))


        # Probably won't need this...
        def remove_file(self):
                # Remove from map
                # delete file from disk?
                pass

        def load_info(self):
                # Ex: HEAD:mono-1.1.13:57664=snapshot_sources/mono-1.1.13/mono-1.1.13.4.57664.tar.gz

                self.info = {}

                fd = open(self.data_store_filename, 'r')
                lock_file(fd)

                for line in fd.readlines():
                        matches = re.compile('(.*)=(.*)').search(line)
                        self.info[matches.group(1)] = matches.group(2)

		# Not needed since we're closing the file
                #unlock_file(fd)
                fd.close()


        def write_info(self):

                fd = open(self.data_store_filename, 'w')
                lock_file(fd)

		keys = self.info.keys()
		keys.sort()
                for key in keys:
                        fd.write('%s=%s\n' % (key, self.info[key]))
                fd.close()

	def get_log_file(self, source_file):
		self.load_info()
		key = ""
		for k,v in self.info.iteritems():
			if v == source_file:
				key = k
				break

		# Ex: /<full_path>/tarball_logs/RELEASE/libgdiplus-1.1/1.1.13.4.log
		return config.mktarball_logs + os.sep + key.replace(":", "/") + ".log"

	def get_latest_tarball(self, HEAD_or_RELEASE, package_name):
		self.load_info()

		versions = []
		# Ex: HEAD:mono-1.1.13:57664=snapshot_sources/mono-1.1.13/mono-1.1.13.4.57664.tar.gz
		for key in self.info.iterkeys():
			stuff = key.split(":")
			# If this is the release and packagename
			if stuff[0] == HEAD_or_RELEASE and stuff[1] == package_name:
				# If the tarball creation succeeded
				if self.info[":".join([HEAD_or_RELEASE, package_name, stuff[2]])] != "tarball_creation_failed":
					versions.append(stuff[2])

		# TODO: Better error handling here
		try:
			latest = utils.version_sort(versions).pop()
			latest_filename = self.info[":".join([HEAD_or_RELEASE, package_name, latest])]
		except:
			latest_filename = ""

		return latest_filename


# XML data store
class build_info:

	def __init__(self, HEAD_or_RELEASE, distro, package_name, version):

		self.HEAD_or_RELEASE = HEAD_or_RELEASE
		self.distro = distro
		self.package_name = package_name
		self.version = version

		self.xml_file = os.path.join(config.build_info_dir, HEAD_or_RELEASE, distro, package_name, version, "info.xml")

		self.rel_files_dir = os.path.join(HEAD_or_RELEASE, distro, package_name, version)

		self.exists = self.build_exists()


	#  This will probably mainly get used by ./build
	def new_build(self):

		if not self.exists:
			# Get a starter template if this doesn't exist
			doc = xml.dom.minidom.parse(config.release_repo_root + "/monobuild/info.xml_new")

			xml.xpath.Evaluate('/build/distro', doc.documentElement)[0].appendChild(doc.createTextNode(self.distro))
			xml.xpath.Evaluate('/build/package', doc.documentElement)[0].appendChild(doc.createTextNode(self.package_name))
			xml.xpath.Evaluate('/build/version', doc.documentElement)[0].appendChild(doc.createTextNode(self.version))

			# Create dir where xml doc and other files will be
			distutils.dir_util.mkpath(os.path.join(config.build_info_dir, self.rel_files_dir, 'files'))
			distutils.dir_util.mkpath(os.path.join(config.build_info_dir, self.rel_files_dir, 'logs'))

			# write new xml out
			self.doc = doc
			self.write_info_xml()

			# Mark build as exists
			self.exists = self.build_exists()

	def build_exists(self):
		return os.path.exists(self.xml_file)

	# Have one subroutine to do this because I'll want to considate options
	def read_info_xml(self):

		if self.exists:
			fd = open(self.xml_file, 'r')
			xml_string = fd.read()
			lock_file(fd)
			self.doc = xml.dom.minidom.parseString(xml_string)
			fd.close()


	# Consolidate options
	def write_info_xml(self):

		# Open a file
		file_obj = open(self.xml_file, 'w')

		# Blocking lock
		lock_file(file_obj)

		# Write out the file
		file_obj.write(self.doc.toxml())

		# Close and unlock file
		file_obj.close()

		# Will this be needed?
		# Make it world writable (0x777)
		# Only do this if it's not already all_rwx
		try:
			os.chmod(self.xml_file, all_rwx)
		except OSError:
			pass


	def update_build(self, **info):
		"""info is a dictionary of keys to update.

		TODO: Should the keys be validated?"""

		self.read_info_xml()

		# If something was passed in, put it into the
		for key,value in info.iteritems():
			key_node = xml.xpath.Evaluate('/build/%s' % key, self.doc.documentElement)[0]

			# Does text node exist?
			if key_node.childNodes:
				key_node.firstChild.nodeValue = value
			else:
				key_node.appendChild(self.doc.createTextNode(value))

		self.write_info_xml()


	def update_step(self, step_name, **info):
		"""Args: step_name, dictionary of things to update inside step
		
		TODO: Does this step need to be mutexed?
		If the step doesn't exist, create and append it"""

		self.read_info_xml()

		steps_node = xml.xpath.Evaluate('/build/steps', self.doc.documentElement)[0]

		node_step = ""
		# Find step node
		for node in xml.xpath.Evaluate('step/name/text()', steps_node):
			if node.nodeValue == step_name:
				node_step = node.parentNode.parentNode
				break

		# If not found, create a new one
		if not node_step:
			#print "%s step not found!" % step_name
			node_step = self.doc.createElement('step')

			name_node = self.doc.createElement('name')
			name_node.appendChild(self.doc.createTextNode(step_name))
			node_step.appendChild(name_node)

			node_step.appendChild(self.doc.createElement('start'))
			node_step.appendChild(self.doc.createElement('finish'))
			node_step.appendChild(self.doc.createElement('state'))
			node_step.appendChild(self.doc.createElement('log'))
			node_step.appendChild(self.doc.createElement('download'))
			steps_node.appendChild(node_step)
			
		# Iterate through info and insert or replace data
		for key, value in info.iteritems():
			value_node = xml.xpath.Evaluate('%s' % key, node_step)[0]

			# See if there's a value set already
			if value_node.childNodes:
				value_node.childNodes[0].nodeValue = value
			else:
				value_node.appendChild(self.doc.createTextNode(value))

		# persist data		
		self.write_info_xml()

	def get_build_info(self, read_info=1):
		values = {}

		if read_info: self.read_info_xml()
		
		if self.exists:
			for key in "distro package version state buildhost start finish".split():
				nodes = xml.xpath.Evaluate('/build/%s/text()' % key, self.doc.documentElement)
				if nodes:
					values[key] = nodes[0].nodeValue
				else: values[key] = ""

		return values

	def get_steps_info(self, read_info=1):
		"""Returns an array of step dictionaries.

		If you know you don't need (or want) a reread of the xml, you can pass in read_info=0"""

		if read_info: self.read_info_xml()

		steps = []

		for node in xml.xpath.Evaluate('/build/steps/step', self.doc.documentElement):
			step = {}
			for key in "name start finish state log download".split():
				tmp_node = xml.xpath.Evaluate('%s/text()' % key, node)
				if tmp_node:
					step[key] = tmp_node[0].nodeValue
				else:   step[key] = ""
			steps.append(step)

		return steps
	

	# Get the state of a package on a platform
	def get_state(self):

		state = ""

		if self.exists:
			self.read_info_xml()

			nodes = xml.xpath.Evaluate('/build/state/text()', self.doc.documentElement)
			if nodes:
				state = nodes[0].nodeValue

		return state

	def get_collective_state(self):
		"""Get a resulting state based on the states of the steps."""

		step_states = []
		state = ""
		

		if self.exists:
			self.read_info_xml()
			timeout = 0
			failure = 0
			testfailure = 0
			state = "success"
			for step_node in xml.xpath.Evaluate('/build/steps/step/state/text()', self.doc.documentElement):
				# Precedence of states
				if step_node.nodeValue == "timeout":
					timeout = 1
				elif step_node.nodeValue == "failure":
					failure = 1
				elif step_node.nodeValue == "testfailure":
					testfailure = 1

			# In order of precedence
			if timeout:
				state = "timeout"
			elif testfailure:
				state = "testfailure"
			elif failure:
				state = "failure"

		return state

