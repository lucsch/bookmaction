import json

import wx

from bookmaction.bookmarks import BookMark
from bookmaction.bookmarksdlg import BookMarkDlg


class BookMarkDocument:
    """"""

    def __init__(self, tag_foreground):
        """Constructor for BookMarkDocument"""
        self.ClearDocument()
        self.m_tag_foreground = tag_foreground
        self.m_isModified = False
        self.m_bookMarksList = []
        self.m_docName = ""
        self.m_isModified = False
        self.m_data_version = 1

    def ClearDocument(self):
        self.m_bookMarksList = []
        self.m_docName = ""
        self.m_isModified = False
        self.m_data_version = 1

    def SaveObject(self, outputstream):
        my_data = {'bookmaction_data_version': self.m_data_version}
        for index, bookmark in enumerate(self.m_bookMarksList):
            my_list = bookmark.GetMemberAsList()
            my_data[str(index)] = my_list
        with open(outputstream, 'w') as f:
            json.dump(my_data, f, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        self.m_docName = outputstream
        self.m_isModified = False

    def LoadObject(self, inputstream):
        my_data = {}
        with open(inputstream) as f:
            try:
                my_data = json.load(f)
            except:
                wx.LogError("Error loading {}! File may be corrupted!".format(inputstream))
                return False

        # check file version
        if 'bookmaction_data_verison' in my_data is False:
            wx.LogError("This isn't a Bookmaction file!")
            return False

        if my_data['bookmaction_data_version'] > self.m_data_version:
            wx.LogError("This file was created with a newer version. Please download the latest version!")
            return False

        # clear
        self.ClearDocument()

        # load data
        for key, values in my_data.items():
            if key.isnumeric():
                my_bookmark = BookMark()
                my_bookmark.LoadMemberFromList(values)
                self.m_bookMarksList.append(my_bookmark)

        self.m_docName = inputstream
        self.m_isModified = False
        return True

    def SetBookMarksToList(self, listctrl, filtertext="", filtercolumn=1):
        listctrl.DeleteAllItems()
        if len(self.m_bookMarksList) == 0:
            listctrl.AppendDefaultText()
            return

        if filtertext == "":
            for bookmark in self.m_bookMarksList:
                listctrl.BookMarkAdd(bookmark, self.m_tag_foreground)
            return

        # support list filtering
        for bookmark in self.m_bookMarksList:
            if self.__HasBookMarkText(filtertext, bookmark, filtercolumn) is True:
                listctrl.BookMarkAdd(bookmark, self.m_tag_foreground)

    def BookMarkAdd(self, listctrl):
        dlg = BookMarkDlg(listctrl.GetParent(), BookMark())
        if dlg.ShowModal() != wx.ID_OK:
            return False

        my_bookmark = dlg.m_BookMarkData
        self.m_bookMarksList.append(my_bookmark)
        listctrl.BookMarkAdd(my_bookmark, self.m_tag_foreground)
        self.m_isModified = True
        return True

    def __GetIndexById(self, iid):
        for index, item in enumerate(self.m_bookMarksList):
            if item.m_id == iid:
                return index
        return -1

    def BookMarkEdit(self, listctrl):
        if listctrl.IsValidSelectedItem() is False:
            return

        my_index = self.__GetIndexById(listctrl.GetItemData(listctrl.GetFirstSelected()))
        dlg = BookMarkDlg(listctrl.GetParent(), self.m_bookMarksList[my_index])
        if dlg.ShowModal() != wx.ID_OK:
            return False

        self.m_bookMarksList[my_index] = dlg.m_BookMarkData
        listctrl.BookMarkEdit(self.m_bookMarksList[my_index], listctrl.GetFirstSelected(), self.m_tag_foreground)
        self.m_isModified = True

    def BookMarkTagSelected(self, listctrl, colour, tag_foreground=0):
        # loop for setting tags in the document and in the list
        for item in listctrl.GetSelectedItems():
            my_bookmark_index = self.__GetIndexById(listctrl.GetItemData(item))
            self.m_bookMarksList[my_bookmark_index].m_tag_color = colour
            listctrl.BookMarkEdit(self.m_bookMarksList[my_bookmark_index], item, tag_foreground)
        self.m_isModified = True

    def BookMarkDelete(self, listctrl):
        if listctrl.IsValidSelectedItem() is False:
            return

        my_index = self.__GetIndexById(listctrl.GetItemData(listctrl.GetFirstSelected()))
        self.m_bookMarksList.pop(my_index)
        listctrl.DeleteItem(listctrl.GetFirstSelected())
        self.m_isModified = True

    def __HasBookMarkText(self, searchtext, bookmark, column=1):
        if column == 1:  # Path
            return searchtext.lower() in bookmark.m_path.lower()
        elif column == 2:  # Description
            return searchtext.lower() in bookmark.m_description.lower()
        elif column == 0:
            return searchtext.lower() in bookmark.m_action_list[bookmark.m_action_index].lower()
        else:
            wx.LogError("This column number isn't supported!")
        return False
