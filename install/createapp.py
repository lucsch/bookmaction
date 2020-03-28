#!/usr/bin/python

##########################################################
# Create a APP package for OSX
# (c) Lucien SCHREIBER 2020
# usage :
#     createapp.py
##########################################################
import os
import subprocess
import fileinput
import argparse

ACTIVE_PLATEFORM = ["Windows", "Linux", "OSX"]


class CreateApp(object):
    def __init__(self, plateform="OSX"):
        if (plateform not in ACTIVE_PLATEFORM):
            raise ValueError("plateform must be one of %r." % ACTIVE_PLATEFORM)

        self.basepath = os.path.join(os.path.dirname(__file__), "..")
        self.binpath = os.path.join(self.basepath, "bin")
        self.plateform = plateform
        self.iconfile = os.path.join(self.basepath, "art", self._get_icon())

    def _get_icon(self):
        """return the icon based on the plateform"""
        icon = "bookmaction.icns"
        if self.plateform == ACTIVE_PLATEFORM[0]:  # Windows
            icon = "bookmaction.ico"
        elif self.plateform == ACTIVE_PLATEFORM[1]:  # Linux
            icon = "bookmaction.png"
        return icon

    def update_version(self):
        """update the about.py file with the version number"""
        command = [
            "python",
            "-m",
            "gitversionbuilder",
            "--dir",
            ".",
            "--lang",
            "python",
            "version.py"]
        try:
            p = subprocess.Popen(command, cwd=os.path.join(self.basepath, "code"))
            p.wait()
        except:
            print("Error running" + command)
            return False

        # load the version number
        self.softversion = 0
        for line in fileinput.input(os.path.join(self.basepath, "code", "version.py")):
            if line.startswith("GIT_COMMITS_SINCE_TAG"):
                self.softversion = int(line[24:])

        print("version is:", self.softversion)

        return True

        # create about.py
        # mi = mercurialinfo.MercurialInfo()
        # self.softversion = mi.get_version()
        # mi.write_about_dialog(filename=os.path.join(self.basepath, "code", "about.py"))

    def modify_spec_file(self):
        """modifiy the spec file before building"""
        # update the spec file for finding the font
        # for line in fileinput.input(os.path.join(self.binpath, "fipro.spec"), inplace=1):
        #    print(line[:-1])
        #    if line.startswith("exe = EXE"):
        #        if self.plateform == ACTIVE_PLATEFORM[0]:  # Windows
        #            print("          Tree('..\\\\font', prefix='font'),")
        #        else:
        #            print("          Tree('..{}font', prefix='font'),".format(os.path.sep))

        if self.plateform == ACTIVE_PLATEFORM[2]:  # OSX
            for line in fileinput.input(os.path.join(self.binpath, "main.spec"), inplace=1):
                if "bundle_identifier=None)" in line:
                    print("             bundle_identifier=None,")
                    print("             info_plist={")
                    print("                 'CFBundleShortVersionString': '1.0.{}',".format(self.softversion))
                    print("                 'NSHumanReadableCopyright': '(c) 2020, Lucien SCHREIBER',".format(
                        self.softversion))
                    print("                 'NSHighResolutionCapable': 'True'")
                    print("             })")
                else:
                    print(line[:-1])

    def create_exe(self):
        """run pyInstaller to create the exe"""
        if not os.path.exists(self.binpath):
            os.makedirs(self.binpath)

        icon = os.path.join(self.basepath, "art", "bookmaction.png")
        command = [
            "pyi-makespec",
            "--onefile",
            "--windowed",
            "--icon={}".format(self.iconfile),
            os.path.join(self.basepath, "code", "main.py")]
        print(command)
        try:
            p = subprocess.Popen(command, cwd=self.binpath)
            p.wait()
        except:
            print("Error running" + command)
            return False

        self.modify_spec_file()

        # run pyinstaller with fipro.spec
        try:
            p = subprocess.Popen(["pyinstaller", "main.spec", "-y"], cwd=self.binpath)
            p.wait()
        except:
            print("Error running : pyinstaller bookmaction.spec")
            return False


##########################################################
# Main function, parse command line arguments
##########################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plateform', help="choose a plateform. Supported values are : " + ", ".join(ACTIVE_PLATEFORM))
    args = parser.parse_args()

    myApp = CreateApp(plateform=args.plateform)
    myApp.update_version()
    myApp.create_exe()
