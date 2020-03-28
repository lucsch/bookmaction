import wx
import pickle
from enum import Enum


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


##########################################################
#   BOOKMARK DOCUMENT
##########################################################
class BookMarkDocument():
    """"""
    def __init__(self,):
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
            mylist = bookmark.GetMemberAsList()
            listctrl.Append(mylist)

    def GetBookMarksFromList(self, listctrl):
        self.m_bookMarksList.clear()
        for index in range(listctrl.GetItemCount()):
            myData = BookMark()
            myData.SetBookMarkActionFromText(listctrl.GetItemText(index, col=0))
            myData.m_path = listctrl.GetItemText(index, col=1)
            myData.m_description = listctrl.GetItemText(index, col=2)
            self.m_bookMarksList.append(myData)

