Name:           IPCE
Version:        r7
Release:        1
License:        Any permissive
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  mono-devel mono-winforms unzip
Url:            http://www.codeplex.com/Wiki/View.aspx?ProjectName=IronPython
Source0:        %{name}-%{version}.zip
Patch0:         IPCE-fix_fepy_init.patch
Summary:        Implementation of the Python programming language running on .NET
Group:          Development/Languages/Python
Provides:       IronPython
Obsoletes:      IronPython
####  fedora  ####
%if 0%{?fedora_version}
# All fedora distros (5 and 6) have the same names, requirements
# Needed to generate wrapper
BuildRequires:  which
%endif
#################

%description
IronPython is the code name of the new implementation of the Python
programming language running on .NET. It supports an interactive
console with fully dynamic compilation. It is well integrated with the
rest of the .NET Framework and makes all .NET libraries easily
available to Python programmers, while maintaining full compatibility
with the Python language.



Authors:
--------
    Jim Hugunin

%files
%defattr(-, root, root)
%doc License.html
/usr/bin/*
/usr/lib/IPCE

%prep
%setup -n %{name}-%{version} -q
%patch0 -p1

%build
# For now, package prebuilt version, as it would be a lot of work
#  to put together the sources that fepy does for it's builds
#  (They don't ship them)  If the point does come where we need
#  to patch a build, we could include the ironpython source, add their
#  patches, and then their supplementary files.
true

%install
# Create dirs
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/IPCE
#Install binaries
cp -a ipy  ${RPM_BUILD_ROOT}/usr/lib/IPCE
cp -a ipy2 ${RPM_BUILD_ROOT}/usr/lib/IPCE
cp -a Lib  ${RPM_BUILD_ROOT}/usr/lib/IPCE
# Generate wrapper scripts
for f in $(find . -name "*\.exe") ; do
	# For the 2.x assemblies...
	if test x$(dirname $f) == x"./ipy2" ; then
		script_name="/usr/bin/$(basename $f .exe)2"
		assembly="ipy2/$(basename $f)"
	else
		script_name="/usr/bin/$(basename $f .exe)"
		assembly="ipy/$(basename $f)"
	fi
        cat <<EOF > ${RPM_BUILD_ROOT}$script_name
#!/bin/sh
exec $(which mono) /usr/lib/IPCE/$assembly "\$@"
EOF
        chmod 755 ${RPM_BUILD_ROOT}$script_name
done
# TODO: patch site.py
# Substitute location of python interpreter to make sure the rpm doesn't depend on /usr/local/bin/python
for i in lib/IPCE/Lib/cgi.py lib/IPCE/Lib/Crypto/Util/RFC1751.py ; do
        sed -i "s/\/usr\/local\/bin\/python/\/usr\/bin\/python/" ${RPM_BUILD_ROOT}/usr/$i
done
# New in r6 (oops, they must have missed this in their source tarball)
find ${RPM_BUILD_ROOT} -name .svn | xargs rm -Rf

%clean
rm -rf "$RPM_BUILD_ROOT"
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
