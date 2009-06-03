var i586 = "x86 32bit (i586)";
var x86_64 = "x86 64bit (x86_64)";

//var release_title = "Moonlight test";

var data =
{
	"title"   : "Moonlight 2.0 preview 4",
	"release" : "1.9.3",
	"tarball" : "http://ftp.novell.com/pub/mono/sources/moon/moonlight-1.9.3.tar.bz2",
	"tag"     : "http://anonsvn.mono-project.com/source/tags/moon/1.9.3",
	"archs" : [
		{
			"name" : "32 bit",
			"2.0" : "novell-moonlight-1.9.3-586.xpi"
		},
		{
			"name" : "64 bit",
			"2.0" : "novell-moonlight-1.9.3-x86_64.xpi"
		},
		{
			"name" : "PowerPC",
			"2.0" : ""
		}
	],
	"browsers" : [ "Firefox 2*","Firefox 3"],
	"platforms" : [
		{
			"name" : "openSuse 11.0",
			"browser" : ["yes","yes","no","no"]
		},
		{
			"name" : "Fedora 9",
			"browser" : ["yes", "yes","no","no"]
		},
		{
			"name" : "Ubuntu 8.04",
			"browser" : ["yes", "yes","no","no"]
		},
		{
			"name" : "SLED 10",
			"browser" : ["yes", "yes","no","no"]
		}
	],
	"releaseNotes" : [
		"coming soon",
		"no really"
	],
	"mono_version" : "123456"
};
