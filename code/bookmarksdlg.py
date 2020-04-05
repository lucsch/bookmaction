import wx

import bookmarks


class BookMarkDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Edit BookMarks", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"BookMark"), wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_bookmarkCtrl = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(-1, -1), 0)
        self.m_bookmarkCtrl.SetMinSize(wx.Size(400, -1))

        bSizer3.Add(self.m_bookmarkCtrl, 0, wx.ALL | wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_btnClipboardPath = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Paste Path", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        bSizer5.Add(self.m_btnClipboardPath, 0, wx.ALL, 5)

        self.m_btnClipboardTxt = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Paste text", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        bSizer5.Add(self.m_btnClipboardTxt, 0, wx.ALL, 5)

        bSizer3.Add(bSizer5, 0, wx.ALIGN_RIGHT, 5)

        sbSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

        bSizer2.Add(sbSizer1, 0, wx.EXPAND | wx.ALL, 5)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Description"), wx.VERTICAL)

        self.m_descriptionCtrl = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(300, 100), 0)
        sbSizer4.Add(self.m_descriptionCtrl, 1, wx.ALL | wx.EXPAND, 5)

        bSizer2.Add(sbSizer4, 1, wx.EXPAND | wx.ALL, 5)

        m_actionCtrlChoices = [u"Open", u"Copy to clipboard", u"Website"]
        self.m_actionCtrl = wx.RadioBox(self, wx.ID_ANY, u"Action", wx.DefaultPosition, wx.DefaultSize,
                                        m_actionCtrlChoices, 1, wx.RA_SPECIFY_COLS)
        self.m_actionCtrl.SetSelection(2)
        bSizer2.Add(self.m_actionCtrl, 0, wx.ALL | wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize();

        bSizer2.Add(m_sdbSizer1, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer2)
        self.Layout()
        bSizer2.Fit(self)

        self.Centre(wx.BOTH)

        self.SetMinSize(wx.Size(250, 350))

        # End of the control definition
        self.__SetDialogAppearance()
        self.m_BookMarkData = bookmarks.BookMark()

        # Connect Events
        self.m_btnClipboardTxt.Bind(wx.EVT_BUTTON, self.OnPasteTxtFromClipboard)
        self.m_btnClipboardPath.Bind(wx.EVT_BUTTON, self.OnPastePathFromClipboard)

    def __del__(self):
        pass

    def TransferDataFromWindow(self):
        self.m_BookMarkData.m_path = self.m_bookmarkCtrl.GetValue()
        self.m_BookMarkData.m_description = self.m_descriptionCtrl.GetValue()
        self.m_BookMarkData.m_action_index = self.m_actionCtrl.GetSelection()
        return True

    def TransferDataToWindow(self):
        self.m_bookmarkCtrl.SetValue(self.m_BookMarkData.m_path)
        self.m_descriptionCtrl.SetValue(self.m_BookMarkData.m_description)
        self.m_actionCtrl.SetSelection(self.m_BookMarkData.m_action_index)
        return True

    def __SetDialogAppearance(self):
        self.m_config = wx.FileConfig("bookmaction")
        myAppearance = self.m_config.ReadInt("Appearance", 0)
        if (myAppearance == 0):  # light mode
            pass  # do nothing for light mode
            # self.SetBackgroundColour(wx.Colour(236,236,236))
            # self.SetForegroundColour(wx.BLACK)
        else:
            self.SetBackgroundColour(wx.Colour(45, 45, 45))
            self.m_bookmarkCtrl.SetForegroundColour(wx.Colour(221,221,221))
            self.m_descriptionCtrl.SetForegroundColour(wx.Colour(221,221,221))

    def OnPasteTxtFromClipboard(self, event):
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.m_bookmarkCtrl.SetValue(do.GetText())
            else:
                wx.MessageBox("""There is no data in the clipboard
                         in the required format""")

    def OnPastePathFromClipboard(self, event):
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.FileDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.m_bookmarkCtrl.SetValue(do.GetFilenames()[0])
            else:
                wx.MessageBox("""There is no data in the clipboard
                         in the required format""")
