import wx

from bookmarks import *


class BookMarkDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Edit BookMarks", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"BookMark"), wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bookmarkCtrl = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(-1, -1), 0)
        self.m_bookmarkCtrl.SetMinSize(wx.Size(300, -1))

        bSizer3.Add(self.m_bookmarkCtrl, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.m_btnClipboard = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Paste from Clipboard", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        sbSizer1.Add(self.m_btnClipboard, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        bSizer2.Add(sbSizer1, 1, wx.EXPAND, 5)

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

        self.__SetDialogAppearance()

        self.m_BookMarkData = BookMark()

        # Connect Events
        self.m_btnClipboard.Bind(wx.EVT_BUTTON, self.OnPasteFromClipboard)

    def __del__(self):
        pass

    def TransferDataFromWindow(self):
        self.m_BookMarkData.m_path = self.m_bookmarkCtrl.GetValue()
        self.m_BookMarkData.m_description = ""
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

    # Virtual event handlers, overide them in your derived class
    def OnPasteFromClipboard(self, event):
        event.Skip()
