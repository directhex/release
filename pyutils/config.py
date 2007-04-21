# Config vars
import os

import stat

# Default distro to make tarballs on (can be overridden in def file)
mktarball_host = "suse-102-x86_64"

# Mono repo svn location
#MONO_ROOT = " svn+ssh://distro@mono-cvs.ximian.com/source"
MONO_ROOT = " svn+ssh://wade@mono-cvs.ximian.com/source"


# Set release base dir
#  Must do at startup, opposed to doing this in a function
module_dir = os.path.dirname(__file__)
if module_dir != "": module_dir += os.sep
release_repo_root = os.path.abspath(module_dir + '..')
# This gets set to /home/wberrier/wa/msvn/release


# Packaging paths
packaging_dir = release_repo_root + '/packaging'
platform_conf_dir = packaging_dir + "/conf"
def_dir = packaging_dir + "/defs"

# Full path to where the builds are output
packages_dir = packaging_dir + "/packages"
snapshot_packages_dir = packaging_dir + "/snapshot_packages"

# Source dirs
sources_dir = packaging_dir + "/sources"
snapshot_sources_dir = packaging_dir + "/snapshot_sources"


# Url path from view of webserver
web_root_url = ""
web_root_dir = release_repo_root + "/monobuild/www"

# 
#build_info_dir = web_root_dir + "/builds/testing"
#build_info_url = web_root_url + "/builds/testing"
build_info_dir = web_root_dir + "/builds"
build_info_url = web_root_url + "/builds"

mktarball_logs = web_root_dir + "/tarball_logs"
mktarball_logs_release_relpath = 'monobuild/www/tarball_logs'

# Can set this to a full path if needed
tar_path="tar"

# Tarball daemon config info
##############################################
td_active = True
# Seconds
td_network_error_interval = 60
td_max_poll_interval = 60
#td_max_poll_interval = 10

# How many revisions to go back when starting to build sequential tarballs
td_num_sequential = 10

# static list of packages to create tarballs for
td_packages = ['mono', 'libgdiplus', 'mono-basic', 'mono-tools', 'monodevelop', 'monodoc', 'xsp', 'gecko-sharp-2.0', 'mono-debugger', 'gtk-sharp', 'mod_mono', 'olive' ]

# builds each and every checkin if true, otherwise, only build the latest checkin
td_sequential = False

##############################################


# Scheduler daemon config info
##############################################
sd_active = True
#  (auto reloading only works for the wakeup_interval and latest_build_packages on the scheduler daemon)
# seconds
sd_wakeup_interval = 60
#sd_wakeup_interval = 300

# Currently not used...
sd_sequential_build_distros = [ 'redhat-9-i386' ]
sd_sequential_build_packages = [ 'mono', 'mono-1.1.13' ]

# List of platforms/packages
sd_latest_build_distros = [ 'redhat-9-i386', 'sles-9-x86_64', 'win-4-i386', 'macos-10-ppc', 'macos-10-x86', 'sunos-8-sparc', 'sunos-10-x86', 'sles-9-ia64', 'sles-9-s390', 'sles-9-s390x', 'sles-9-ppc', 'debian-31-arm', 'debian-31-sparc', 'suse-100-i586' ]
sd_latest_build_packages = td_packages
##############################################

# Sync thread options
##############################################
sync_active = True
sync_host = 'mono-web@mono.ximian.com'
sync_target_dir = '~/release'

# Testing
#sync_host = 'wberrier@wblinux.provo.novell.com'
#sync_target_dir = 'wa/msvn/release/monobuild/www/builds'

#sync_num_builds = 50 # 880 MB in one test...
#sync_num_builds = 20 # 434 MB in one test...
sync_num_builds = 10 # 268 MB in one test...

sync_sleep_time = 10
##############################################

##############################################
# Default environment (used by sshutils and packaging.buildenv)
env_vars = {
	'chroot_path':		'/usr/sbin/chroot',
	'strip_path':		'strip',
	'tar_path':		'tar',
	'make_path':		'make',
	'build_location':	'/tmp'
}

######################################
# Common place for source extensions, which can be compiled to reg later
# Ennumerate to make it simpler...
#  (Src.zip for IronPython)
# (note: these need to be in the order of increasingly less specific, for 'packaging/build')
source_extensions = """
        -src.tar.bz2
        -src.tar.gz
        .tar.bz2
        .tar.gz
        -Src.zip
        -src.zip
        .zip
""".split()

# Results in something like:
# = "(\.tar\.gz|\.zip)"
sources_ext_re_string = "(" + "|".join(source_extensions).replace(".", "\.") + ")"

######################################

######################################
# Commonly used permission settings

all_rwx = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO # 777
shell_perms = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH # 755
data_perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH # 644

######################################

