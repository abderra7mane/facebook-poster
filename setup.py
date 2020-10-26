#-*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

from poster.common import consts


################################################################
# The manifest will be inserted as resource into your .exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store it in a file named
# and copy it with the data_files option into the dist-dir.
#
manifest_template = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""
    
RT_MANIFEST = 24

distribution = "poster"


setup(

    windows = [{
        
        "script" : "main.py",
        
        "name" : consts.__appname__,
        
        "version" : consts.__version__,
        
        "author" : consts.__author__,

        "author_email" : consts.__email__,

        "url" : consts.__domain__,
        
        "company_name" : consts.__company__,
        
        "copyright" : consts.__copyright__,
        
        "description" : consts.__description__,
        
        # "other_resources" : [
        #     (RT_MANIFEST, 1, manifest_template % dict(prog=distribution))
        # ],
        
        "icon_resources" : [
            (1, "poster\\rc\\img\\icon.ico")
        ],
        
        "dest_base" : distribution,

    }],

    options = {

        "py2exe" : {

            "compressed" : True,

            "optimize" : 2,

            # "bundle_files" : 1,

            # "ascii" : 1,

            # "skip_archive" : True,

            "includes" : [

                "sip",
                "PyQt4.QtCore",
                "PyQt4.QtGui",
                "PyQt4.QtNetwork",
                "PyQt4.QtWebKit",
                "PyQt4.QtXml",
                "PyQt4.QtSvg",
                "requests",

            ],

            "excludes" : [
            ],

            "dll_excludes" : [
                # "msvcp90.dll",
            ],

            "packages" : [
            ],

        },

    },

    packages = [
    ],

    package_data = {
    },

    data_files = [

        ("imageformats", [
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qgif4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qico4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qjpeg4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qmng4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qsvg4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qtga4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\imageformats\\qtiff4.dll",
        ]),

        ("bearer", [
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\bearer\\qnativewifibearer4.dll",
            "C:\\Python\\2.7\\Lib\\site-packages\\PyQt4\\plugins\\bearer\\qgenericbearer4.dll",
        ]),
    
    ],

    zipfile = None,

)
