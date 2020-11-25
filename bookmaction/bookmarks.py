import os
import platform
import subprocess
import wx


# from bookmaction.bookmarksdlg import BookMarkDlg


##########################################################
#   BOOKMARK CLASS
##########################################################
class BookMark:
    """Contains bookmark data, such as name, description and action"""

    def __init__(self, ):
        """Constructor for BookMark"""
        self.m_id = wx.NewIdRef()
        self.m_path = ""
        self.m_description = ""
        self.m_action_index = 0
        self.m_action_list = ["Open", "Copy to Clipboard", "Website"]
        self.m_tag_color = wx.BLACK

    def GetMemberAsList(self):
        myList = [
            self.m_action_list[self.m_action_index],
            self.m_path,
            self.m_description,
            self.m_tag_color.GetAsString()
        ]
        return myList

    def LoadMemberFromList(self, list_member):
        self.m_action_index = self.m_action_list.index(list_member[0])
        self.m_path = list_member[1]
        self.m_description = list_member[2]
        if len(list_member) > 3:
            self.m_tag_color = wx.Colour(list_member[3])

    def DoAction(self):
        if self.m_action_index == 0:  # Open
            self.DoActionOpen()
        elif self.m_action_index == 1:  # Copy to clipboard
            self.DoActionCopyToClipboard()
        elif self.m_action_index == 2:  # website
            self.DoActionOpenWebsite()
        else:
            wx.LogError("This action isn't supported (for now)!")

    def DoActionOpen(self):
        # check if the path exist
        if os.path.exists(self.m_path) is False:
            wx.LogError("The path '{}' didn't exist".format(self.m_path))
            return
        if platform.system() == "Windows":
            os.startfile(self.m_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", self.m_path])
        else:
            subprocess.Popen(["xdg-open", self.m_path])

    def DoActionCopyToClipboard(self):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.m_path))
            wx.TheClipboard.Close()

    def DoActionOpenWebsite(self):
        wx.LaunchDefaultBrowser(self.m_path)



