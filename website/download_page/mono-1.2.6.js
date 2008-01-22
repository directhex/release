var i586 = "x86 32bit (i586)";
var x86_64 = "x86 64bit (x86_64)";
var ppc = "PowerPC 32bit (ppc32)";
var ia64 = "Itanium (ia64)";
var s390 = "IBM s390 32bit";
var s390x = "IBM s390x 64bit";

var data =
{
	"release" : "1.2.6",
	"platforms" : [
	{
		"name" : "VMware",
		"icon" : "vmware_icon_2.jpg",
		"dlicon" : "vmware_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 10.2",
			"arch" : [
			{
				"name" : "Mono 1.2.5.1",
				"desc" : "",
				"downloadText" : ""
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
			"name" : "openSUSE 10.1",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : ppc,
				"desc" : "",
				"downloadText" : "",
			}
			]
		},
		{
			"name" : "openSUSE 10.2",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : ppc,
				"desc" : "",
				"downloadText" : "",
			}
			]
		},
		{
			"name" : "openSUSE 10.3",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
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
			"name" : "Suse Linux Enterprise Server 9 (SLES)",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : ppc,
				"desc" : "",
				"downloadText" : "",
			},
			{
				"name" : ia64,
				"desc" : "",
				"downloadText" : "",
			},
			{
				"name" : s390,
				"desc" : "",
				"downloadText" : "",
			},
			{
				"name" : s390x,
				"desc" : "",
				"downloadText" : "",
			}
			]
		},
		{
			"name" : "Suse Linux Enterprise Server 10 (SLES)",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : ppc,
				"desc" : "",
				"downloadText" : "",
			},
			{
				"name" : ia64,
				"desc" : "",
				"downloadText" : "",
			}
			]
		},
		{
			"name" : "Suse Linux Enterprise Desktop 10 (SLED)",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
			}
			]
		},
		{
			"name" : "Novell Linux Desktop 9 (NLD)",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			},
			{
				"name" : x86_64,
				"desc" : "",
				"downloadText" : ""
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
				"desc" : "",
				"downloadText" : ""
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
			"name" : "Mac OS X Tiger (10.4) and Leopard (10.5)",
			"arch" : [
			{
				"name" : "All",
				"desc" : "",
				"downloadText" : ""
			}
			]
		}
		]
	},

	{
		"name" : "RedHat",
		"icon" : "http://www.mono-project.com/files/6/6e/Mono_icon_redhat.gif",
		"dlicon" : "http://www.mono-project.com/files/6/6e/Mono_icon_redhat.gif",
		"version" : [
		{
			"name" : "RedHat Enterprise Linux 4",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			}
			]
		}
		]
	},

	{
		"name" : "Other&nbsp;Linux's",
		"icon" : "linux.jpg",
		"dlicon" : "linux.jpg",
		"version" : [
		{
			"name" : "Generic Linux",
			"arch" : [
			{
				"name" : i586,
				"desc" : "",
				"downloadText" : ""
			}
			]
		}
		]
	},

	{
		"name" : "Maemo",
		"icon" : "http://www.mono-project.com/files/a/aa/Maemo.gif",
		"dlicon" : "http://www.mono-project.com/files/a/aa/Maemo.gif",
		"version" : [
		{
			"name" : "Maemo",
			"arch" : [
			{
				"name" : "Nokia 770 and 800",
				"desc" : "",
				"downloadText" : ""
			}
			]
		}
		]
	},

	{
		"name" : "Solaris",
		"icon" : "http://www.mono-project.com/files/2/2f/Mono_icon_solaris.gif",
		"dlicon" : "http://www.mono-project.com/files/2/2f/Mono_icon_solaris.gif",
		"version" : [
		{
			"name" : "Solaris 8",
			"arch" : [
			{
				"name" : "SPARC",
				"desc" : "",
				"downloadText" : ""
			}
			]
		}
		]
	}

	]
};
