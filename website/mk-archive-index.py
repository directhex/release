#!/usr/bin/env python

import sys
import os
import distutils.dir_util
import re
import string
import glob
import getopt

import pdb

sys.path += [ '../pyutils' ]

import packaging
import config
import utils
import build

skip_installers = False
skip_packages = False
distros = build.get_platforms()
# Command line options
try:
        opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "skip_installers", "skip_packages", "platforms=" ])

	(bundle, output_dir) = remaining_args

        for option, value in opts:
                if option == "--skip_installers":
                         skip_installers = True
                if option == "--skip_packages":
                         skip_packages = True
                if option == "--platforms":
                        distros = value.split(",")

except:
        print "Usage: ./mk-archive-index.py [ --skip_installers | --platforms=distros ] <bundle name> <output webdir>"
        print " --platforms: comma separated list of platforms (distros) to include"
        print " --skip_installers: don't include installers in listing"
        sys.exit(1)

bundle_conf = packaging.bundle(bundle_name=bundle)
#print bundle_conf.info

# Create url dirs
out_file = os.path.join(output_dir, "archive", bundle_conf.info['archive_version'], 'download', 'index.html')
distro_out_file = os.path.join(output_dir, 'download-' + bundle_conf.info['bundle_urlname'], 'index.html')
distutils.dir_util.mkpath(os.path.dirname(out_file))
distutils.dir_util.mkpath(os.path.dirname(distro_out_file))

version = bundle_conf.info['archive_version']
md_version = bundle_conf.info['md_version']

bundle_short_desc = bundle_conf.info['bundle_urlname']
if bundle_conf.info.has_key('bundle_short_desc'):
        bundle_short_desc = bundle_conf.info['bundle_short_desc']

#### Sources ####
sources = "<p> <a href='../sources'>Sources</a> </p>"
distro_sources = "<p> <a href='../sources-%s'>Sources</a> </p>" % bundle_conf.info['bundle_urlname']

#### Installers ####

installer_info = [
	{ 'dir_name': 'windows-installer', 'name': 'Windows Installer',                         'ext': 'exe'},
	{ 'dir_name': 'macos-10-universal','name': 'Mac OSX Installer (universal)',             'ext': 'dmg'},
	{ 'dir_name': 'md-macos-10',       'name': 'MonoDevelop for OSX Installer (universal)', 'ext': 'dmg'},
	{ 'dir_name': 'sunos-8-sparc',     'name': 'Solaris 8 SPARC Package',                   'ext': 'pkg.gz'}
]

installers = ""
distro_installers = ""

if not skip_installers:
	for installer_map in installer_info:
		print "Writing %s to index page" % installer_map['dir_name']
		topdir = 'archive'
		_version = version

		if installer_map['dir_name'] == "md-macos-10":
			topdir = 'monodevelop'
			_version = md_version

		my_dir = os.path.join(output_dir, topdir, _version, installer_map['dir_name'])

		# Skip if the installer doesn't exist for this release
		if not os.path.exists(my_dir):
			print "Directory '%s' doens't exist" % my_dir			
			continue

		revision = utils.get_latest_ver(my_dir)
		installer_dir = my_dir + os.sep + revision
		ref_dir = os.path.join("..",installer_map['dir_name'], revision)
		ref_dir2 = os.path.join("..", topdir, _version, installer_map['dir_name'], revision)


		#tab = 20
		#print "installer_dir = ".rjust(tab) + installer_dir
		#print "revision = ".rjust(tab) + revision
		#print "ref_dir = ".rjust(tab) + ref_dir
		#print "ref_dir2 = ".rjust(tab) + ref_dir2

		filename = os.path.basename(glob.glob(installer_dir + os.sep + '*.%s' % installer_map['ext']).pop())
		sum_filename = os.path.basename(glob.glob(installer_dir + os.sep + '*.md5').pop())

		#print "filename = ".rjust(tab) + filename
		#print "sum_filename = ".rjust(tab) + sum_filename

		installers += "<p>%s: <a href='%s/%s'>%s</a> [<a href='%s/%s'>MD5SUM</a>] </p>\n" % (installer_map['name'], ref_dir, filename, filename, ref_dir, sum_filename)
		distro_installers += "<p>%s: <a href='%s/%s'>%s</a> [<a href='%s/%s'>MD5SUM</a>] </p>\n" % (installer_map['name'], ref_dir2, filename, filename, ref_dir2, sum_filename)


#### Packages ####
packages = "<ul>"

# Links to distros
for distro_conf in distros:
	if skip_packages: continue
	conf = packaging.buildconf(os.path.basename(distro_conf), exclusive=False)
	# Skip the distros that use zip packaging system
	if not conf.get_info_var('USE_ZIP_PKG'):
		if os.path.exists(os.path.join(output_dir, 'download-' + bundle_conf.info['bundle_urlname'], conf.name)):
			if conf.get_info_var('distro_aliases'):
				alias_text = "[ " + " | ".join(conf.get_info_var('distro_aliases')) + " ]"
			else: alias_text = ""
			packages += "<li><a href='%s'>%s</a> %s</li>\n" % (conf.name, conf.name, alias_text)

packages += "</ul>"

#### Repositories ####
repositories = "<ul>"
obs_repos = utils.get_dict_var('obs_repos', bundle_conf.info)
for obs_repo in obs_repos:
	repo_name = string.split(obs_repo, "/")[-2]
	repositories += "<li><a href=\"%s\">%s</a></li>\n" % (repo_name, repo_name)
repositories += "</ul>"

fd = open(os.path.join(config.release_repo_root, 'website', 'archive-index'))
out_text = fd.read()
fd.close()

distro_out_text = out_text

out_text = out_text.replace('[[webroot_path]]',    '../../..')
out_text = out_text.replace('[[version]]',    version)
out_text = out_text.replace('[[sources]]',    sources)
out_text = out_text.replace('[[installers]]', installers)
out_text = out_text.replace('[[packages]]',   packages)
out_text = out_text.replace('[[repositories]]', repositories)
out_text = out_text.replace('([[bundle_short_desc]])',   '')

distro_out_text = distro_out_text.replace('[[webroot_path]]',    '..')
distro_out_text = distro_out_text.replace('[[version]]',    version)
distro_out_text = distro_out_text.replace('[[sources]]',    distro_sources)
distro_out_text = distro_out_text.replace('[[installers]]', distro_installers)
distro_out_text = distro_out_text.replace('[[packages]]',   packages)
distro_out_text = distro_out_text.replace('[[repositories]]', repositories)
distro_out_text = distro_out_text.replace('[[bundle_short_desc]]',  bundle_short_desc)

out = open(out_file, 'w')
out.write(out_text)
out.close()

# TODO: Make this part optional if needed later
out = open(distro_out_file, 'w')
out.write(distro_out_text)
out.close()

