#!/usr/bin/python

##########################################################
# bookmaction
# (c) Lucien SCHREIBER 2020
# Bookmarks action
##########################################################

import wx

##########################################################
# MAIN FRAME CLASS
##########################################################


class BAFrame (wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, id=wx.ID_ANY,
            title=u"Bookmaction", pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        #icon = wx.Icon()
        #icon.CopyFromBitmap(bitmaps.pro.GetBitmap())
        #self.SetIcon(icon)


        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
        bSizer1.Add( self.m_listCtrl, 1, wx.ALL|wx.EXPAND, 0 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # menubar
        self.m_menubar = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menu_paste = wx.MenuItem(
            self.m_menu1, wx.ID_PASTE, u"Paste" + u"\t" + u"Ctrl+V",
            wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menu_paste)

        self.m_menu_exit = wx.MenuItem(
            self.m_menu1, wx.ID_EXIT, u"Exit" + u"\t" + u"Alt+F4",
            wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menu_exit)

        self.m_menubar.Append(self.m_menu1, u"File")
        self.SetMenuBar(self.m_menubar)

        # computing minimum size
        #mysizebutton = bSizer14.ComputeFittingWindowSize(self)
        #mysizepanel = bSizer5.ComputeFittingWindowSize(self)
        #self.SetMinSize([mysizebutton[0] + mysizepanel[0], mysizebutton[1]])
        #self.SetSize([900, mysizebutton[1]])




        # connect Menu events
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)


    def __del__(self):
        pass

  

    def OnQuit(self, event):
        self.Close()


##########################################################
#  MAIN APP CLASS
##########################################################


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
