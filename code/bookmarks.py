import os
import platform
import subprocess
import wx
import pickle
from enum import Enum
import bookmarksdlg


class BookMarkAction(Enum):
    OPEN = 0
    COPY_TO_CLIPBOARD = 1


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
        self.m_action = BookMarkAction.OPEN

    def GetMemberAsList(self):
        myList = []
        myList.append(self.GetBookMarkActionToText())
        myList.append(self.m_path)
        myList.append(self.m_description)
        return myList

    def GetBookMarkActionToText(self):
        myActionTxt = "Open"
        if (self.m_action == BookMarkAction.COPY_TO_CLIPBOARD):
            myActionTxt = "Copy to Clipboard"
        return myActionTxt

    def SetBookMarkActionFromText(self, text):
        self.m_action = BookMarkAction.COPY_TO_CLIPBOARD
        if (text == "Open"):
            self.m_action = BookMarkAction.OPEN

    def DoAction(self):
        if (self.m_action == BookMarkAction.COPY_TO_CLIPBOARD):
            if (wx.TheClipboard.Open()):
                wx.TheClipboard.SetData(wx.TextDataObject(self.m_path))
                wx.TheClipboard.Close()
        elif (self.m_action == BookMarkAction.OPEN):
            if platform.system() == "Windows":
                os.startfile(self.m_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.m_path])
            else:
                subprocess.Popen(["xdg-open", self.m_path])


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

        my_bookmark = BookMark()
        if (dlg.m_radioBtn2.GetValue() == True):
            my_bookmark.m_action = BookMarkAction.COPY_TO_CLIPBOARD
        my_bookmark.m_path = dlg.m_bookmarkCtrl.GetValue()
        my_bookmark.m_description = dlg.m_descriptionCtrl.GetValue()
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
