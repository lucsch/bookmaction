import os
import platform
import subprocess
import wx
import pickle
import bookmarksdlg


##########################################################
#   BOOKMARK CLASS
##########################################################
class BookMark():
    """Contains bookmark data, such as name, description and action"""

    def __init__(self, ):
        """Constructor for BookMark"""
        self.m_id = wx.NewIdRef()
        self.m_path = ""
        self.m_description = ""
        self.m_action_index = 0
        self.m_action_list = ["Open", "Copy to Clipboard", "Website"]

    def GetMemberAsList(self):
        myList = []
        myList.append(self.m_action_list[self.m_action_index])
        myList.append(self.m_path)
        myList.append(self.m_description)
        return myList

    def DoAction(self):
        if (self.m_action_index == 0):  # Open
            self.DoActionOpen()
        elif (self.m_action_index == 1):  # Copy to clipboard
            self.DoActionCopyToClipboard()
        elif (self.m_action_index == 2):  # website
            self.DoActionOpenWebsite()
        else:
            wx.LogError("This action isn't supported (for now)!")

    def DoActionOpen(self):
        # check if the path exist
        if (os.path.exists(self.m_path) == False):
            wx.LogError("The path '{}' didn't exist".format(self.m_path))
            return
        if platform.system() == "Windows":
            os.startfile(self.m_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", self.m_path])
        else:
            subprocess.Popen(["xdg-open", self.m_path])

    def DoActionCopyToClipboard(self):
        if (wx.TheClipboard.Open()):
            wx.TheClipboard.SetData(wx.TextDataObject(self.m_path))
            wx.TheClipboard.Close()

    def DoActionOpenWebsite(self):
        wx.LaunchDefaultBrowser(self.m_path)


##########################################################
#   BOOKMARK DOCUMENT
##########################################################
class BookMarkDocument():
    """"""

    def __init__(self, ):
        """Constructor for BookMarkDocument"""
        self.m_bookMarksList = []
        self.m_docName = ""
        self.m_isModified = False

    def SaveObject(self, outputstream):
        pickle.dump(self.m_bookMarksList, open(outputstream, "wb"))
        self.m_docName = outputstream
        self.m_isModified = False

    def LoadObject(self, inputstream):
        self.m_bookMarksList = pickle.load(open(inputstream, "rb"))
        self.m_docName = inputstream
        self.m_isModified = False

    def SetBookMarksToList(self, listctrl):
        listctrl.DeleteAllItems()
        for bookmark in self.m_bookMarksList:
            listctrl.Append(bookmark.GetMemberAsList())
            listctrl.SetItemData(listctrl.GetItemCount() - 1, bookmark.m_id)

    def GetBookMarksFromList(self, listctrl):
        self.m_bookMarksList.clear()
        for index in range(listctrl.GetItemCount()):
            myData = listctrl.GetBookMarkDataFromList(index)
            self.m_bookMarksList.append(myData)

    def BookMarkAdd(self, listctrl):
        dlg = bookmarksdlg.BookMarkDlg(listctrl.GetParent())
        if (dlg.ShowModal() != wx.ID_OK):
            return False

        my_bookmark = dlg.m_BookMarkData
        self.m_bookMarksList.append(my_bookmark)
        listctrl.BookMarkAdd(my_bookmark)
        self.m_isModified = True
        return True

    def __GetIndexById(self, id):
        for index, item in enumerate(self.m_bookMarksList):
            if (item.m_id == id):
                return index
        return -1

    def BookMarkEdit(self, listctrl):
        if (listctrl.IsValidSelectedItem() == False):
            return

        my_index = self.__GetIndexById(listctrl.GetItemData(listctrl.GetFirstSelected()))
        dlg = bookmarksdlg.BookMarkDlg(listctrl.GetParent())
        dlg.m_BookMarkData = self.m_bookMarksList[my_index]
        if (dlg.ShowModal() != wx.ID_OK):
            return False

        self.m_bookMarksList[my_index] = dlg.m_BookMarkData
        listctrl.BookMarkEdit(self.m_bookMarksList[my_index], listctrl.GetFirstSelected())
        self.m_isModified = True

    def BookMarkDelete(self, listctrl):
        if (listctrl.IsValidSelectedItem() == False):
            return

        my_index = self.__GetIndexById(listctrl.GetItemData(listctrl.GetFirstSelected()))
        self.m_bookMarksList.pop(my_index)
        listctrl.DeleteItem(listctrl.GetFirstSelected())
        self.m_isModified = True
