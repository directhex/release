# Config vars
import os


# Default distro to make tarballs on (can be overridden in def file)
mktarball_host = "suse-93-i586"

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
