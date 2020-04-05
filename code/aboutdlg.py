import wx
import version
import bitmaps


class AboutDlg(wx.Dialog):

    def __init__(self, parent, programname):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"About", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_bitmap1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, programname, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(250, 100),
                                       wx.TE_MULTILINE)
        bSizer8.Add(self.m_textCtrl3, 1, wx.EXPAND | wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
        bSizer8.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_sdbSizer3 = wx.StdDialogButtonSizer()
        self.m_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer3.AddButton(self.m_sdbSizer3Cancel)
        m_sdbSizer3.Realize();

        bSizer8.Add(m_sdbSizer3, 0, wx.EXPAND | wx.ALL, 5)

        # append bitmap
        my_bitmap = bitmaps.bookmaction.GetBitmap()
        my_image = my_bitmap.ConvertToImage()
        my_image.Rescale(32, 32)
        my_small_bmp = wx.Bitmap(my_image)
        self.m_bitmap1.SetBitmap(my_small_bmp)

        # change font and compute minimum size for text
        my_font = wx.SWISS_FONT
        my_font.SetPointSize(my_font.GetPointSize() + 3)
        self.m_staticText2.SetFont(my_font)
        dc = wx.ScreenDC()
        dc.SetFont(my_font)
        my_size = dc.GetTextExtent(programname)
        my_size += wx.Size(10, 10)
        self.m_staticText2.SetMinSize(my_size)

        # set copyright for the current year
        my_year = wx.DateTime.Now().GetCurrentYear()
        self.m_staticText3.SetLabel("(c) Lucien SCHREIBER, " + str(my_year))
        my_font.SetPointSize(my_font.GetPointSize() - 5)
        self.m_staticText3.SetFont(my_font)

        # set version number
        self.m_textCtrl3.AppendText("Commit id: " + version.COMMIT_ID + "\n")
        self.m_textCtrl3.AppendText("Commit number: " + version.COMMIT_NUMBER + "\n")
        self.m_textCtrl3.AppendText("Branch: " + version.BRANCH_NAME)

        self.__SetDialogAppearance()

        self.SetSizer(bSizer8)
        self.Layout()
        bSizer8.Fit(self)

        self.Centre(wx.BOTH)

    def __SetDialogAppearance(self):
        self.m_config = wx.FileConfig("bookmaction")
        myAppearance = self.m_config.ReadInt("Appearance", 0)
        if (myAppearance == 0):  # light mode
            pass  # do nothing for light mode
            # self.SetBackgroundColour(wx.Colour(236,236,236))
            # self.SetForegroundColour(wx.BLACK)
        else:
            self.SetBackgroundColour(wx.Colour(45, 45, 45))
            self.m_textCtrl3.SetForegroundColour(wx.Colour(221, 221, 221))
            self.m_staticText2.SetForegroundColour(wx.Colour(221, 221, 221))
            self.m_staticText3.SetForegroundColour(wx.Colour(221, 221, 221))

    def __del__(self):
        pass
