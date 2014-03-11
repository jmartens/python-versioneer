#!/usr/bin/env python

import os, base64, tempfile
from distutils.core import setup
from distutils.command.build_scripts import build_scripts

LONG="""
Versioneer is a tool to automatically update version strings (in setup.py and
the conventional 'from PROJECT import _version' pattern) by asking your
version-control system about the current tree.
"""

class my_build_scripts(build_scripts):
    def run(self):
        with open("versioneer.py") as f:
            v = f.read()
        v_b64 = base64.b64encode(v)
        lines = [v_b64[i:i+60] for i in range(0, len(v_b64), 60)]
        v_b64 = "\n".join(lines)+"\n"

        with open("src/installer.py") as f:
            s = f.read()
        s = s.replace("@VERSIONEER-INSTALLER@", v_b64)

        tempdir = tempfile.mkdtemp()
        installer = os.path.join(tempdir, "versioneer-installer")
        with open(installer, "w") as f:
            f.write(s)

        self.scripts = [installer]
        rc = build_scripts.run(self)
        os.unlink(installer)
        os.rmdir(tempdir)
        return rc

setup(
    name = "versioneer",
    license = "public domain",
    version = "0.8+",
    description = "Easy VCS-based management of project version strings",
    author = "Brian Warner",
    author_email = "warner@lothar.com",
    url = "https://github.com/warner/python-versioneer",
    # "fake" is replaced with versioneer-installer in build_scripts. We need
    # a non-empty list to provoke "setup.py build" into making scripts,
    # otherwise it skips that step.
    scripts = ["fake"],
    long_description = LONG,
    cmdclass = { "build_scripts": my_build_scripts },
    )
