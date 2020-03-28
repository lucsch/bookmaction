import wx

from bookmarks import *


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
        self.m_bookmarkCtrl.SetMinSize(wx.Size(300, -1))

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

        bSizer2.Add(sbSizer1, 0, wx.EXPAND, 5)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Description"), wx.VERTICAL)

        self.m_descriptionCtrl = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(300, 100), 0)
        sbSizer4.Add(self.m_descriptionCtrl, 1, wx.ALL | wx.EXPAND, 5)

        bSizer2.Add(sbSizer4, 1, wx.EXPAND, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Action when double-clicked"), wx.VERTICAL)

        self.m_radioBtn1 = wx.RadioButton(sbSizer2.GetStaticBox(), wx.ID_ANY, u"Open folder", wx.DefaultPosition,
                                          wx.DefaultSize, wx.RB_GROUP)
        self.m_radioBtn1.SetValue(True)
        sbSizer2.Add(self.m_radioBtn1, 0, wx.ALL, 5)

        self.m_radioBtn2 = wx.RadioButton(sbSizer2.GetStaticBox(), wx.ID_ANY, u"Copy to clipboard", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        sbSizer2.Add(self.m_radioBtn2, 0, wx.ALL, 5)

        bSizer2.Add(sbSizer2, 0, wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize();

        bSizer2.Add(m_sdbSizer1, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()
        bSizer2.Fit(self)

        self.Centre(wx.BOTH)

        # End of the control definition
        self.__SetDialogAppearance()
        self.m_BookMarkData = BookMark()

        # Connect Events
        self.m_btnClipboardTxt.Bind(wx.EVT_BUTTON, self.OnPasteTxtFromClipboard)
        self.m_btnClipboardPath.Bind(wx.EVT_BUTTON, self.OnPastePathFromClipboard)

    def __del__(self):
        pass

    def TransferDataFromWindow(self):
        self.m_BookMarkData.m_path = self.m_bookmarkCtrl.GetValue()
        self.m_BookMarkData.m_description = self.m_descriptionCtrl.GetValue()
        self.m_BookMarkData.m_action = BookMarkAction.OPEN
        if (self.m_radioBtn2.GetValue() == True):
            self.m_BookMarkData.m_action = BookMarkAction.COPY_TO_CLIPBOARD
        return True

    def __SetDialogAppearance(self):
        self.m_config = wx.FileConfig("bookmaction")
        myAppearance = self.m_config.ReadInt("Appearance", 0)
        if (myAppearance == 0):  # light mode
            pass  # do nothing for da
            # self.SetBackgroundColour(wx.Colour(236,236,236))
            # self.SetForegroundColour(wx.BLACK)
        else:
            self.SetBackgroundColour(wx.Colour(21, 21, 21))

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
