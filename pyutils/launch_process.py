#!/usr/bin/env python

import sys
import getopt
import os

import utils

def usage():
	print "Usage: ./launch_process.py [--terminate_reg=<reg string>] [--output_timeout=<secs>] [--max_output_size=<num chars>] [--kill_process_group] [--interruptable] <command>"

def commandline():

        if len(sys.argv) < 2:
                usage()
                sys.exit(1)

	# Options for launch process
	try:
		opts, command = getopt.getopt(sys.argv[1:], "", [ "terminate_reg=", "output_timeout=", "max_output_size=", "kill_process_group", "env=", "working_dir=", "interruptable=" ])
	except getopt.GetoptError:
                usage()
		sys.exit(1)

	# Get args to pass to function
	args = {}
	for option, value in opts:
		if option == "--terminate_reg":
			args['terminate_reg'] = value
		if option == "--output_timeout":
			args['output_timeout'] = int(value)
		if option == "--kill_process_group":
			args['kill_process_group'] = 1
		if option == "--max_output_size":
			args['max_output_size'] = float(value)
		if option == "--env":
			for e in value.split(','):
				k, v = e.split('=')
				os.environ[k] = v
		if option == "--working_dir":
			try:
				os.chdir(value)
			except:
				print "Failed to chdir: " + value
				print "Exiting..."
				sys.exit(1)
		if option == "--interruptable":
			args['interruptable'] = value

	command = " ".join(command)
	code, output = utils.launch_process(command, **args)
	sys.exit(code)

# If called from the command line, run main, otherwise, functions are callable through imports
if __name__ == "__main__":
        commandline()


