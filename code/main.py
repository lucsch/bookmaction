#!/usr/bin/python

##########################################################
# bookmaction
# (c) Lucien SCHREIBER 2020
# Bookmarks action
##########################################################

import wx
import wx.adv
import bitmaps
import version  # this file is generated with git-version
from bookmarklistctrl import *
from settingsdlg import *


##########################################################
# MAIN FRAME CLASS
##########################################################


class BAFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, id=wx.ID_ANY,
            title=u"Bookmaction", pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.__CreateControls()
        self.__CreateMenus()
        self.__CreateStatusAndVersion()

        # computing minimum size
        # mysizepanel = bSizer5.ComputeFittingWindowSize(self)
        # self.SetMinSize([mysizebutton[0] + mysizepanel[0], mysizebutton[1]])
        self.SetSize([900, 600])
        self.Layout()
        self.Centre(wx.BOTH)

        self.__SetDialogAppearance()

    def __SetDialogAppearance(self):
        self.m_config = wx.FileConfig("bookmaction")
        myAppearance = self.m_config.ReadInt("Appearance", 0)
        if (myAppearance == 0):  # light mode
            pass  # do nothing for da
            # self.SetBackgroundColour(wx.Colour(236,236,236))
            # self.SetForegroundColour(wx.BLACK)
        else:
            self.SetBackgroundColour(wx.Colour(21, 21, 21))

    def __CreateControls(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(bitmaps.bookmaction.GetBitmap())
        self.SetIcon(icon)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_listCtrl = BookMarkListCtrl(self)
        bSizer1.Add(self.m_listCtrl, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(bSizer1)

    def __CreateMenus(self):
        # menubar
        self.m_menubar = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuNew = wx.MenuItem(self.m_menu1, wx.ID_NEW, u"New" + u"\t" + u"Ctrl+N", wx.EmptyString,
                                     wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuNew)

        self.m_menuOpen = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Open" + u"\t" + u"Ctrl+O", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuOpen)

        self.m_menuSave = wx.MenuItem(self.m_menu1, wx.ID_SAVE, u"Save" + u"\t" + u"Ctrl+S", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuSave)

        self.m_menuSaveAs = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Save as...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuSaveAs)

        self.m_menu1.AppendSeparator()

        self.m_menuSettings = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"Settings...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuSettings)

        self.m_menu1.AppendSeparator()

        self.m_menuExit = wx.MenuItem(self.m_menu1, wx.ID_EXIT, u"Quit" + u"\t" + u"Alt+F4", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuExit)

        self.m_menubar.Append(self.m_menu1, u"File")

        self.m_menu2 = wx.Menu()
        self.m_menuBookAdd = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Add..." + u"\t" + u"Ctrl+D", wx.EmptyString,
                                         wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuBookAdd)

        self.m_menuBookRemove = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Remove" + u"\t" + u"Del", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuBookRemove)

        self.m_menuBookEdit = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Edit...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuBookEdit)

        self.m_menubar.Append(self.m_menu2, u"Bookmarks")

        self.m_menu3 = wx.Menu()
        self.m_menuAbout = wx.MenuItem(self.m_menu3, wx.ID_ABOUT, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_menuAbout)

        self.m_menuWebsite = wx.MenuItem(self.m_menu3, wx.ID_ANY, u"website...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_menuWebsite)

        self.m_menubar.Append(self.m_menu3, u"About")

        self.SetMenuBar(self.m_menubar)

        # connect Menu events
        self.Bind(wx.EVT_MENU, self.OnWebSite, id=self.m_menuWebsite.GetId())
        self.Bind(wx.EVT_MENU, self.OnAddBookMarkMenu, id=self.m_menuBookAdd.GetId())
        self.Bind(wx.EVT_MENU, self.OnSettingsMenu, id=self.m_menuSettings.GetId())

        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

    def __CreateStatusAndVersion(self):
        self.CreateStatusBar(2)
        self.SetStatusText(self.__GetGitVersion(), 1)

    def __GetGitVersion(self):
        return "version: " + str(version.GIT_COMMITS_SINCE_TAG) + " (" + version.GIT_COMMIT_ID + ")"

    def __del__(self):
        pass

    def OnQuit(self, event):
        self.Close()

    def OnWebSite(self, event):
        wx.LaunchDefaultBrowser("https://github.com/lucsch/bookmaction")

    def OnAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = self.Title
        info.Version = self.__GetGitVersion()
        info.Icon = self.GetIcon()
        info.Developers = ["Lucien SCHREIBER"]
        info.Description = """Bookmarks manager with actions"""
        wx.adv.AboutBox(info)

    def OnAddBookMarkMenu(self, event):
        self.m_listCtrl.AddBookMark()

    def OnSettingsMenu(self, event):
        mydlg = SettingsDlg(self)
        mydlg.ShowModal()


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
