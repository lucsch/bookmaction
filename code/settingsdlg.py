import wx


###########################################################################
## Class SettingsDlg
###########################################################################

class SettingsDlg(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        m_radioBox1Choices = [u"Light mode", u"Dark mode"]
        self.m_radioBox1 = wx.RadioBox(self, wx.ID_ANY, u"Appearance", wx.DefaultPosition, wx.DefaultSize,
                                       m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS)
        self.m_radioBox1.SetSelection(0)
        bSizer4.Add(self.m_radioBox1, 1, wx.ALL | wx.EXPAND, 5)

        m_sdbSizer2 = wx.StdDialogButtonSizer()
        self.m_sdbSizer2OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer2.AddButton(self.m_sdbSizer2OK)
        self.m_sdbSizer2Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer2.AddButton(self.m_sdbSizer2Cancel)
        m_sdbSizer2.Realize();

        bSizer4.Add(m_sdbSizer2, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer4)
        self.Layout()
        bSizer4.Fit(self)

        self.Centre(wx.BOTH)

        self.m_config = wx.FileConfig("bookmaction")

        self.Bind(wx.EVT_BUTTON, self.OnBtnOk, id=wx.ID_OK)

    def TransferDataFromWindow(self):
        myAppearance = self.m_config.ReadInt("Appearance", 0)
        self.m_radioBox1.SetSelection(myAppearance)
        return True

    def OnBtnOk(self, event):
        self.m_config.WriteInt("Appearance", self.m_radioBox1.GetSelection())
        self.Close()

    def __del__(self):
        pass
