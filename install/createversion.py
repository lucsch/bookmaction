#!/usr/bin/python

import os
from subprocess import check_output
import argparse


class GitVersion():
    """Generate a file with Git Version info"""

    def __init__(self, ):
        self.m_commit_id = self.__ComputeGitCommand(["git", "describe", "--always", "--dirty=+"])[:-1].decode("utf-8")
        self.m_commit_number = self.__ComputeGitCommand(["git", "rev-list", "HEAD", "--count"])[:-1].decode("utf-8")
        self.m_branch_name = self.__ComputeGitCommand(["git", "rev-parse", "--abbrev-ref", "HEAD"])[:-1].decode("utf-8")
        self.m_dirpath = os.path.dirname(__file__)

    def __ComputeGitCommand(self, commandlist):
        out = ""
        try:
            out = check_output(commandlist)
        except:
            print("Error running command: {}".format(commandlist))
            return ""
        return out

    def WriteToFile(self, filename):
        my_filename = os.path.join(self.m_dirpath, filename)
        file = open(my_filename, "w")
        file.write("""# ---------------------------------------------------
# This file is autogenerated by createversion.py
# DO NOT MODIFY!
# ---------------------------------------------------
""")
        file.write("COMMIT_ID=\"" +self.m_commit_id + '"\n')
        file.write("COMMIT_NUMBER=\"" + self.m_commit_number + '"\n')
        file.write("BRANCH_NAME=\"" + self.m_branch_name + '"\n')
        file.close()


##########################################################
# Main function, parse command line arguments
##########################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='filename (using relative path is possible)')
    args = parser.parse_args()
    my_gitversion = GitVersion()
    my_gitversion.WriteToFile(args.name)
