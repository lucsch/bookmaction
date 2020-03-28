#!/usr/bin/python

##########################################################
# Create a DMG package for OSX
# (c) Lucien SCHREIBER 2015
# usage :
#     createdmg.py <installer name> <app path>
##########################################################
import os
import argparse
import subprocess


def CreateInstaller(name, app_path, use_version=True):
    version = 0
    basepath = os.path.join(os.path.dirname(__file__), "..")
    if use_version is True:
        with open(os.path.join(basepath, "code", "version.py")) as reader:
            for line in reader:
                if line.startswith("GIT_COMMITS_SINCE_TAG"):
                    version = int(line[24:])

        if (version):
            print("Git version is:", version)
        else:
            print("Error getting Git version number!")

    mycommand = [
        'hdiutil',
        'create',
        '-volname', name,
        '-srcfolder', app_path,
        name + str(version) + ".dmg"]
    print(mycommand)

    try:
        p = subprocess.Popen(mycommand)
        # , 0, None, None, None,  None, None, False, False, gDirInstall)
        p.wait()
    except:
        print("Error creating DMG!")
        return
    print("Creating DMG finished!")


##########################################################
# Main function, parse command line arguments
##########################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Installer Name')
    parser.add_argument('path', help='Application Path')
    args = parser.parse_args()
    CreateInstaller(args.name, args.path)
