import wx
import bookmarks


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
        self.InsertColumn(0, "Action", width=150)
        self.InsertColumn(1, "BookMark", width=400)
        self.InsertColumn(2, "Description", width=200)

        self.AppendDefaultText()

        # bind events
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.OnDeleteListItem)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClickItem)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem)

    def AppendDefaultText(self):
        self.defaultColumnText = "Add BookMark to start!"
        self.Append(["", self.defaultColumnText])

    def ClearList(self):
        self.DeleteAllItems()
        self.Append(["", self.defaultColumnText])

    def SetColumnText(self, index, column, text):
        self.SetItem(index, column, str(text))

    def BookMarkAdd(self, bookmark):
        # check if default text is present
        if (self.GetItemText(0, 1) == self.defaultColumnText):
            self.DeleteAllItems()

        self.Append(bookmark.GetMemberAsList())
        self.SetItemData(self.GetItemCount() - 1, bookmark.m_id)

    def BookMarkEdit(self, bookmark, index):
        self.SetColumnText(index, 0, bookmark.m_action_list[bookmark.m_action_index])
        self.SetColumnText(index, 1, bookmark.m_path)
        self.SetColumnText(index, 2, bookmark.m_description)

    def IsValidSelectedItem(self):
        # check for selected item
        if (self.GetSelectedItemCount() == 0 or self.GetSelectedItemCount() > 1):
            wx.LogWarning("Select only one bookmark!")
            return False

        itemindex = self.GetFirstSelected()
        # check and ignore default text
        if (self.GetItemText(itemindex, col=1) == self.defaultColumnText):
            return False
        return True

    def GetSelectedItems(self):
        """    Gets the selected items for the list control.
        Selection is returned as a list of selected indices,
        low to high.
        """
        selection = []
        index = self.GetFirstSelected()

        # check for default text
        if (self.GetItemText(index, col=1) == self.defaultColumnText):
            return  selection

        selection.append(index)
        while len(selection) != self.GetSelectedItemCount():
            index = self.GetNextSelected(index)
            selection.append(index)
        return selection

    def GetCountVisible(self):
        my_count = self.GetItemCount()
        if (my_count == 0):
            return 0
        elif (my_count == 1 and self.GetItemText(0, col=1) == self.defaultColumnText):
            return 0
        return self.GetItemCount()

    def GetBookMarkDataFromList(self, index):
        my_data = bookmarks.BookMark()
        my_data.m_id = self.GetItemData(index)
        my_data.m_action_index = my_data.m_action_list.index(self.GetItemText(index, col=0))
        my_data.m_path = self.GetItemText(index, col=1)
        my_data.m_description = self.GetItemText(index, col=2)
        return my_data

    def OnDoubleClickItem(self, event):
        my_data = self.GetBookMarkDataFromList(event.GetIndex())
        my_data.DoAction()

    def OnRightClickItem(self, event):
        if (self.IsValidSelectedItem() == False):
            event.Skip()
            return
        id_remove = self.GetParent().GetParent().m_menuBookRemove.GetId()
        id_edit = self.GetParent().GetParent().m_menuBookEdit.GetId()

        m_menu_popup = wx.Menu()
        m_menuPopupRemove = wx.MenuItem(m_menu_popup, id_remove, u"Remove" + u"\t" + u"Del", wx.EmptyString,
                                        wx.ITEM_NORMAL)
        m_menu_popup.Append(m_menuPopupRemove)
        m_menuPopupEdit = wx.MenuItem(m_menu_popup, id_edit, u"Edit..." + u"\t" + u"Ctrl+E", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        m_menu_popup.Append(m_menuPopupEdit)
        m_menu_popup.AppendSeparator()
        m_menuPopupDoOpen = wx.MenuItem(m_menu_popup, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL)
        m_menuPopupDoCopyToClipboard = wx.MenuItem(m_menu_popup, wx.ID_ANY, u"Copy to Clipboard", wx.EmptyString,
                                                   wx.ITEM_NORMAL)
        m_menuPopupDoWebsite = wx.MenuItem(m_menu_popup, wx.ID_ANY, u"Open in web browser", wx.EmptyString,
                                           wx.ITEM_NORMAL)
        m_menu_popup.Append(m_menuPopupDoOpen)
        m_menu_popup.Append(m_menuPopupDoCopyToClipboard)
        m_menu_popup.Append(m_menuPopupDoWebsite)

        # edit and remove event are processed by the parent
        self.Bind(wx.EVT_MENU, self.OnPopupDoOpen, id=m_menuPopupDoOpen.GetId())
        self.Bind(wx.EVT_MENU, self.OnPopupDoCopyToClipboard, id=m_menuPopupDoCopyToClipboard.GetId())
        self.Bind(wx.EVT_MENU, self.OnPopupDoWebsite, id=m_menuPopupDoWebsite.GetId())
        self.PopupMenu(m_menu_popup)

    def OnDeleteListItem(self, event):
        if (event.GetKeyCode() != wx.WXK_DELETE or event.GetKeyCode() != wx.WXK_BACK):
            event.Skip()
            return

        self.GetParent().OnBookMarkMenuDelete(wx.CommandEvent())
        event.Skip()

    def OnPopupDoOpen(self, event):
        my_data = self.GetBookMarkDataFromList(self.GetFirstSelected())
        my_data.DoActionOpen()

    def OnPopupDoCopyToClipboard(self, event):
        my_data = self.GetBookMarkDataFromList(self.GetFirstSelected())
        my_data.DoActionCopyToClipboard()

    def OnPopupDoWebsite(self, event):
        my_data = self.GetBookMarkDataFromList(self.GetFirstSelected())
        my_data.DoActionOpenWebsite()
