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
