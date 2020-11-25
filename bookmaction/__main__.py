import wx

from bookmaction.bookmaction import BAFrame


class BAApp(wx.App):
    """
    Main application class
    initialize the BAFrame class and the main loop
    """

    def OnInit(self):
        dlg = BAFrame()
        dlg.Show(True)
        self.SetTopWindow(dlg)
        return True


app = BAApp()
app.MainLoop()
