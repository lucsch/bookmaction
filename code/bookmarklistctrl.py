import wx
from bookmarksdlg import *


class BookMarkListCtrl(wx.ListCtrl):
    """a wx.listctrl component for pasting and manipulating bookmarks"""

    def __init__(self, parent):
        wx.ListCtrl.__init__(
            self, parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.Size(800, 200),
            style=wx.LC_REPORT | wx.LC_HRULES)

        # initing 2 columns
        self.InsertColumn(0, "Action", format=wx.LIST_FORMAT_CENTER, width=100)
        self.InsertColumn(1, "BookMark", width=400)
        self.InsertColumn(2, "Description", width=200)

        self.defaultColumnText = "Add BookMark to start!"
        self.Append(["", self.defaultColumnText])

        # bind events
        # self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnDeleteListItem)
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.OnDeleteListItem)

    def SetDefaultEmptyListText(self, text=""):
        if text != "":
            self.defaultColumnText = text

    def ClearList(self):
        self.DeleteAllItems()
        self.Append(["", self.defaultColumnText])

    def SetColumnText(self, index, column, text):
        self.SetStringItem(index, column, str(text))

    def AddBookMark(self):
        dlg = BookMarkDlg(self)
        if (dlg.ShowModal() != wx.ID_OK):
            pass

        myInfo = dlg.m_BookMarkData.GetMemberAsList()
        self.Append(myInfo)


    # def SetFiles(self, filenames, clearlist):
    #     if clearlist is True:
    #         self.DeleteAllItems()
    #     if (len(self.GetFilenames()) == 0):
    #         self.DeleteAllItems()
    #     starter = self.GetItemCount()
    #     for index, filename in enumerate(filenames):
    #         self.Append([index + 1 + starter, filename])
    #
    # def PasteFilesFromClipboard(self, clearlist):
    #     if not wx.TheClipboard.IsOpened():  # may crash, otherwise
    #         do = wx.FileDataObject()
    #         wx.TheClipboard.Open()
    #         success = wx.TheClipboard.GetData(do)
    #         wx.TheClipboard.Close()
    #         if success:
    #             self.SetFiles(do.GetFilenames(), clearlist)
    #         else:
    #             wx.MessageBox("""There is no data in the clipboard
    #             in the required format""")
    #
    # def CopyFilesToClipboard(self):
    #     """copy the list content to the clipboard"""
    #     if (len(self.GetFilenames()) == 0):
    #         return
    #
    #     mytxt = "\n".join(self.GetFilenames())
    #
    #     if not wx.TheClipboard.IsOpened():
    #         do = wx.TextDataObject(mytxt)
    #         wx.TheClipboard.Open()
    #         wx.TheClipboard.SetData(do)
    #         wx.TheClipboard.Close()

    def OnDeleteListItem(self, event):
        if (event.GetKeyCode() == wx.WXK_DELETE or
                event.GetKeyCode() == wx.WXK_BACK and
                self.GetFirstSelected() != -1):
            if (self.GetItemText(
                    self.GetFirstSelected(), 1) != self.defaultColumnText):
                self.DeleteItem(self.GetFirstSelected())

                # change all numbers
                for index in range(self.GetItemCount()):
                    self.SetItemText(index, str(index + 1))

                if self.GetItemCount() == 0:
                    self.Append(["", self.defaultColumnText])
        event.Skip()
