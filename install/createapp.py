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
import createversion

ACTIVE_PLATEFORM = ["Windows", "Linux", "OSX"]


class CreateApp(object):
    def __init__(self, plateform="OSX"):
        if (plateform not in ACTIVE_PLATEFORM):
            raise ValueError("plateform must be one of %r." % ACTIVE_PLATEFORM)

        self.basepath = os.path.join(os.path.dirname(__file__), "..")
        self.binpath = os.path.join(self.basepath, "bin")
        self.plateform = plateform
        self.iconfile = os.path.join(self.basepath, "art", self._get_icon())
        self.m_commit_number = ""

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
        my_version = createversion.GitVersion()
        my_version.WriteToFile("../code/version.py")
        self.m_commit_number = my_version.m_commit_number
        return True

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
            for line in fileinput.input(os.path.join(self.binpath, "bookmaction.spec"), inplace=1):
                if "bundle_identifier=None)" in line:
                    print("             bundle_identifier=None,")
                    print("             info_plist={")
                    print("                 'CFBundleShortVersionString': '1.0.{}',".format(self.m_commit_number))
                    print("                 'NSHumanReadableCopyright': '(c) 2020, Lucien SCHREIBER',".format(
                        self.m_commit_number))
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
            os.path.join(self.basepath, "code", "bookmaction.py")]
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
            p = subprocess.Popen(["pyinstaller", "bookmaction.spec", "-y"], cwd=self.binpath)
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
