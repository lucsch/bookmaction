import wx


###########################################################################
## Class SettingsDlg
###########################################################################

class SettingsDlg(wx.Dialog):

    def __init__(self, parent, config_object):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Settings", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.m_config_object = config_object

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Appearance"), wx.VERTICAL)

        self.m_darkModeCtrl = wx.CheckBox(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Dark mode", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        sbSizer3.Add(self.m_darkModeCtrl, 0, wx.ALL, 5)

        self.m_staticText1 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY,
                                           u"Restart needed in order to take action", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        sbSizer3.Add(self.m_staticText1, 0, wx.ALL, 5)

        bSizer4.Add(sbSizer3, 1, wx.EXPAND | wx.ALL, 5)

        m_radio_tag_ctrlChoices = [u"Foreground", u"Background"]
        self.m_radio_tag_ctrl = wx.RadioBox(self, wx.ID_ANY, u"Tag", wx.DefaultPosition, wx.DefaultSize,
                                            m_radio_tag_ctrlChoices, 1, wx.RA_SPECIFY_ROWS)
        self.m_radio_tag_ctrl.SetSelection(0)
        bSizer4.Add(self.m_radio_tag_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Auto load document"), wx.VERTICAL)

        self.m_filePickerCtrl = wx.FilePickerCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                  u"*.bmka", wx.DefaultPosition, wx.DefaultSize,
                                                  wx.FLP_DEFAULT_STYLE | wx.FLP_FILE_MUST_EXIST | wx.FLP_OPEN)
        self.m_filePickerCtrl.SetMinSize(wx.Size(400, -1))

        sbSizer5.Add(self.m_filePickerCtrl, 0, wx.ALL | wx.EXPAND, 5)

        bSizer4.Add(sbSizer5, 0, wx.EXPAND | wx.ALL, 5)

        m_sdbSizer2 = wx.StdDialogButtonSizer()
        self.m_sdbSizer2OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer2.AddButton(self.m_sdbSizer2OK)
        self.m_sdbSizer2Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer2.AddButton(self.m_sdbSizer2Cancel)
        m_sdbSizer2.Realize();

        bSizer4.Add(m_sdbSizer2, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer4)
        self.Layout()
        bSizer4.Fit(self)

        self.Centre(wx.BOTH)

        self.SetMinSize(wx.Size(250, 280))

        # appareance
        self.__SetDialogAppearance()

        # connecting event
        self.Bind(wx.EVT_BUTTON, self.OnBtnOk, id=wx.ID_OK)

    def TransferDataToWindow(self):
        myAppearance = self.m_config_object.ReadInt("Appearance", 0)
        myLoadFile = self.m_config_object.Read("AutoLoadFile", "")
        my_tag_config = self.m_config_object.ReadInt("Tag", 0)
        self.m_darkModeCtrl.SetValue(myAppearance)
        self.m_filePickerCtrl.SetPath(myLoadFile)
        self.m_radio_tag_ctrl.SetSelection(my_tag_config)
        return True

    def __SetDialogAppearance(self):
        # self.m_config = wx.FileConfig("bookmaction")
        myAppearance = self.m_config_object.ReadInt("Appearance", 0)
        if (myAppearance == 0):  # light mode
            pass  # do nothing for da
            # self.SetBackgroundColour(wx.Colour(236,236,236))
            # self.SetForegroundColour(wx.BLACK)
        else:
            self.SetBackgroundColour(wx.Colour(21, 21, 21))

    def OnBtnOk(self, event):
        self.m_config_object.WriteInt("Appearance", self.m_darkModeCtrl.IsChecked())
        self.m_config_object.Write("AutoLoadFile", self.m_filePickerCtrl.GetPath())
        self.m_config_object.WriteInt("Tag", self.m_radio_tag_ctrl.GetSelection())
        self.m_config_object.Flush()
        self.Close()

    def __del__(self):
        pass
