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


def CreateInstaller(name, app_path, output_path, use_version=True):
    version = 0
    basepath = os.path.join(os.path.dirname(__file__), "..")
    if use_version is True:
        with open(os.path.join(basepath, "bookmaction", "version.py")) as reader:
            for line in reader:
                if line.startswith("COMMIT_NUMBER"):
                    version = int(line[15:-2])

        if (version):
            print("Git version is:", version)
        else:
            print("Error getting Git version number!")

    mycommand = [
        'hdiutil',
        'create',
        '-volname', name,
        '-srcfolder', app_path,
        os.path.join(output_path, name + str(version) + ".dmg")]
    print(mycommand)

    try:
        p = subprocess.Popen(mycommand)
        # , 0, None, None, None,  None, None, False, False, gDirInstall)
        p.wait()
    except:
        print("Error creating DMG!")
        return
    print("Creating DMG finished!")


def delete_binary(app_path):
    for name in os.listdir(app_path):
        if os.path.isfile(os.path.join(app_path, name)) and not name.startswith("."):
            print("removing : " + name)
            os.remove(os.path.join(app_path, name))


##########################################################
# Main function, parse command line arguments
##########################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Installer Name')
    parser.add_argument('path', help='Application Path')
    parser.add_argument('output_path', help="Output path for DMG")
    args = parser.parse_args()
    delete_binary(args.path)
    CreateInstaller(args.name, args.path, args.output_path)
