var yast = "This distribution supports installing packages via YaST. Add the following installation source to YaST:"
var yast_help = "For assistance with using repositories and installing packages with YaST, <a href=\"http://en.opensuse.org/Add_Package_Repositories_to_YaST\">visit the YaST help page.</a>"
var zypper = "This distribution supports installing packages via Zypper. Add the following repository to Zypper:"
var zypper_help_1 = "<p>To add the repository, execute the following commands (as root):</p><pre><blockquote><code>zypper addrepo <em>"
var zypper_help_2 = "</em> mono-stable<br/>zypper refresh --repo mono-stable<br/>zypper dist-upgrade --repo mono-stable</code></blockquote></pre>"
var discontinued = "<div style=\"color: darkred; font-weight: bold\">Binaries for this platform have been discontinued.  Builds may be available from <a href=\"http://www.mono-project.com/Other_Downloads\">unsupported downloads</a> or we may be looking for a volunteer to maintain packages.</div>";
var i586_x86_64 = "i586, x86_64"
var i586_x86_64_ppc64_ia64 = "i586, x86_64, ppc64, and ia64"
var enterprise = "<p>The <a href=\"http://www.novell.com/products/mono/\">SUSE Linux Enterprise Mono Extension</a> is available for purchase from <a href=\"http://www.novell.com/\">Novell</a>.</p>"

// URLS

var download_url_base = "http://ftp.novell.com/pub/mono"

var vpc_torrent_url = download_url_base + "/appliance/2.8/Mono-2.8-vpc.zip.torrent"
var vpc_zip_url = download_url_base + "/appliance/2.8/Mono-2.8-vpc.zip"

var vmx_torrent_url = download_url_base + "/appliance/2.8/Mono-2.8-vmx.zip.torrent"
var vmx_zip_url = download_url_base + "/appliance/2.8/Mono-2.8-vmx.zip"

var livecd_torrent_url = download_url_base + "/appliance/2.8/Mono-2.8.iso.torrent"
var livecd_iso_url = download_url_base + "/appliance/2.8/Mono-2.8.iso"

var ops110_repo_url = download_url_base + "/download-stable/openSUSE_11.0"
var ops111_repo_url = download_url_base + "/download-stable/openSUSE_11.1"
var ops112_repo_url = download_url_base + "/download-stable/openSUSE_11.2"
var ops113_repo_url = download_url_base + "/download-stable/openSUSE_11.3"

var sle11_repo_url = download_url_base + "/download-stable/SLE_11"
var rhel5_repo_url = download_url_base + "/download-stable/RHEL_5"

var win_exe_url = download_url_base + "/archive/2.8/windows-installer/9/mono-2.8-gtksharp-2.12.10-win32-9.exe"
var win_gtk_url = download_url_base + "/gtk-sharp/gtk-sharp-2.12.10.win32.msi"

var osx_x86_url = download_url_base + "/archive/2.8/macos-10-x86/9/MonoFramework-2.8_9.macos10.novell.x86.dmg"
var osx_x86_csdk_url = download_url_base + "/archive/2.8/macos-10-x86/9/MonoFramework-CSDK-2.8_9.macos10.novell.x86.dmg"
var osx_ppc_url = download_url_base + "/archive/2.8/macos-10-ppc/9/MonoFramework-2.8_9.macos10.novell.ppc.dmg"
var osx_ppc_csdk_url = download_url_base + "/archive/2.8/macos-10-ppc/9/MonoFramework-CSDK-2.8_9.macos10.novell.ppc.dmg"
var osx_univ_url = download_url_base + "/archive/2.8/macos-10-universal/9/MonoFramework-2.8_9.macos10.novell.universal.dmg"
var osx_univ_csdk_url = download_url_base + "/archive/2.8/macos-10-universal/9/MonoFramework-CSDK-2.8_9.macos10.novell.universal.dmg"
var osx_cocoa_source_url = "http://go-mono.com/sources/cocoa-sharp/cocoa-sharp-0.9.5.tar.bz2"

var codice = "These packages are provided by <a href=\"http://www.codicesoftware.com/\">Codice Software</a>."
var solaris_10_sparc_url = download_url_base + "/third-party/codice/mono-2.6.1-sol10-sparc.pkg.gz"
var opensolaris_x86_url = download_url_base + "/third-party/codice/mono-2.6.1-opensolaris-x86.pkg.gz"


var data =
{
	"release" : "2.8",
	"platforms" : [
	{
		"name" : "Virtual PC",
		"icon" : "virtualpc.jpg",
		"dlicon" : "virtualpc_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.3",
			"arch" : [
			{
				"name" : "Mono 2.8",
				"desc" : "",
				"downloadText" : "Download an openSUSE 11.3 Virtual PC image which includes Mono 2.8<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href=\"" + vpc_torrent_url + "\">via Torrent</a> <li><a href=\"" + vpc_zip_url + "\">via http</a> </ul><a href=\"http://mono-project.com/VirtualPC_Image\">Instructions for using the Virtual PC image</a>."
			}
			]
		}
		]
	},
	{
		"name" : "VMware",
		"icon" : "vmware_icon_2.jpg",
		"dlicon" : "vmware_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.3",
			"arch" : [
			{
				"name" : "Mono 2.8",
				"desc" : "",
				"downloadText" : "Download an openSUSE 11.3 VMWare image which includes Mono 2.8<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href=\"" + vmx_torrent_url + "\">via Torrent</a> <li><a href=\"" + vmx_zip_url + "\">via http</a> </ul><a href=\"http://mono-project.com/VMware_Image\">Instructions for using the VMware image</a>."
			}
			]
		}
		]
	},
	{
		"name" : "LiveCD",
		"icon" : "livecd.jpg",
		"dlicon" : "livecd.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.3 Live CD",
			"arch" : [
			{
				"name" : "Mono 2.8",
				"desc" : "",
				"downloadText" : "Download the openSUSE 11.3 Live CD which includes Mono 2.8<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href=\"" + livecd_torrent_url + "\">via Torrent</a> <li><a href=\"" + livecd_iso_url + "\">via http</a> </ul>"
			}
			]
		}
		]
	},
	{
		"name" : "openSUSE",
		"icon" : "opensuse.jpg",
		"dlicon" : "opensuse.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"" + ops111_repo_url + "\">" + ops111_repo_url + "</a></ul>" + zypper_help_1 + ops111_repo_url + zypper_help_2
			}
			]
		},
		{
			"name" : "openSUSE 11.2",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"" + ops112_repo_url + "\">" + ops112_repo_url + "</a></ul>" + zypper_help_1 + ops112_repo_url + zypper_help_2
			}
			]
		},
		{
			"name" : "openSUSE 11.3",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"" + ops113_repo_url + "\">" + ops113_repo_url + "</a></ul>" + zypper_help_1 + ops113_repo_url + zypper_help_2
			}
			]
		}
		]
	},

	{
		"name" : "SLES/SLED",
		"icon" : "sles.jpg",
		"dlicon" : "sles.jpg",
		"version" : [
		{
			"name" : "SUSE Linux Enterprise 11",
			"arch" : [
			{
				"name" : "Novell Supported for i586, x86_64, and s390x",
				"desc" : "",
				"downloadText" : enterprise
			},
			{
				"name" : i586_x86_64_ppc64_ia64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"" + sle11_repo_url + "\">" + sle11_repo_url + "</a></ul>" + zypper_help_1 + sle11_repo_url + zypper_help_2
			}
			]
		}
		]
	},

	{
		"name" : "RHEL/CentOS",
		"icon" : "centos.jpg",
		"dlicon" : "centos.jpg",
		"version" : [
		{
			"name" : "Red Hat Enterprise Linux 5",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : "<ul><li><a href=\"" + rhel5_repo_url + "\">" + rhel5_repo_url + "</a></li></ul>"
			}
			]
		}
		]
	},

	{
		"name" : "Windows",
		"icon" : "http://www.mono-project.com/files/0/00/Mono_icon_windows.gif",
		"dlicon" : "http://www.mono-project.com/files/0/00/Mono_icon_windows.gif",
		"version" : [
		{
			"name" : "Windows 2000, XP, 2003 and Vista",
			"arch" : [
			{
				"name" : "All",
				"desc" : "This download works on all versions of Windows 2000, XP, 2003 and Vista.",
				"downloadText" : "<ul><li><a href=\"" + win_exe_url + "\">Mono for Windows, Gtk#, and XSP</a></li><li><a href=\"" + win_gtk_url + "\">Gtk# for .NET</a></li><li><a href=\"http://mono-project.com/MoMA\">Mono Migration Analyzer</a></li></ul>"
			}
			]
		}
		]
	},

	{
		"name" : "Mac&nbsp;OS&nbsp;X",
		"icon" : "http://www.mono-project.com/files/b/bf/Mono_icon_mac.gif",
		"dlicon" : "http://www.mono-project.com/files/b/bf/Mono_icon_mac.gif",
		"version" : [
		{
			"name" : "Mac OS X Tiger (10.4), Leopard (10.5), and Snow Leopard (10.6)",
			"arch" : [
			{
				"name" : "All",
				"desc" : "This download works on Mac OS X Tiger (10.4), Leopard (10.5), and Snow Leopard (10.6).",
				"downloadText" : "Includes Mono, Cocoa#, Gtk# installs in /Library/Frameworks:<br/><em>The CSDK packages are for developers embedding mono into their applications.  If you don't know what that means you don't need it.</em><ul><li>Mono 2.8<ul><li>Intel: <a href=\"" + osx_x86_url + "\">Framework</a> <span style=\"font-size: small\">(<a href=\"" + osx_x86_csdk_url + "\">CSDK</a>)</span></li><li>PowerPC: <a href=\"" + osx_ppc_url + "\">Framework</a> <span style=\"font-size: small\">(<a href=\"" + osx_ppc_csdk_url + "\">CSDK</a>)</span></li><li>Universal: <a href=\"" + osx_univ_url + "\">Framework</a> (if you don't know what you need) <span style=\"font-size: small\">(<a href=\"" + osx_univ_csdk_url + "\">CSDK</a>)</span></li></ul><li><a href=\"http://monodevelop.com/Download/Mac_Preview\">MonoDevelop Preview</a></li></li><li><a href=\"" + osx_cocoa_source_url + "\">Cocoa# 0.9.5 source</a></ul>Gtk# and System.Windows.Forms applications require X11.  Installing on a machine without X11 installed will result in errors during install, and these components will not function correctly."
			}
			]
		}
		]
	},

	{
		"name" : "Solaris",
		"icon" : "solaris.jpg",
		"dlicon" : "solaris.jpg",
		"version" : [
		{
			"name" : "Solaris 10",
			"arch" : [
			{
				"name" : "sparc",
				"desc" : codice,
				"downloadText" : "<a href=\"" + solaris_10_sparc_url + "\">" + solaris_10_sparc_url + "</a>"
			}
			]
		},
		{
			"name" : "OpenSolaris",
			"arch" : [
			{
				"name" : "x86",
				"desc" : codice,
				"downloadText" : "<a href=\"" + opensolaris_x86_url + "\">" + opensolaris_x86_url + "</a>"
			}
			]
		}
		]
	},
	{
		"name" : "Other",
		"icon" : "linux_icon.jpg",
		"version" : [
		{
			"name" : "Debian",
			"icon" : "debian_icon.jpg",
			"url" : "http://mono-project.com/DistroPackages/Debian"
		},
		{
			"name" : "Ubuntu",
			"icon" : "ubuntu_icon.jpg",
			"url" : "http://mono-project.com/DistroPackages/Ubuntu"
		},
		{
			"name" : "Other",
			"icon" : "linux_icon.jpg",
			"url" : "http://www.mono-project.com/Other_Downloads"
		}
		]
	}
	]
};
