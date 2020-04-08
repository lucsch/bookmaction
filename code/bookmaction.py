#!/usr/bin/python

##########################################################
# bookmaction
# (c) Lucien SCHREIBER 2020
# Bookmarks action
##########################################################

import os
import platform
import wx
import wx.adv
import bitmaps
import version  # this file is generated with git-version
from bookmarklistctrl import *
from settingsdlg import *
from bookmarks import *
from aboutdlg import *


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

        # id
        self.ID_SEARCH_ACTION = wx.Window.NewControlId()
        self.ID_SEARCH_BOOKMARK = wx.Window.NewControlId()
        self.ID_SEARCH_DESCRIPTION = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_NONE = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_RED = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_ORANGE = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_YELLOW = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_GREEN = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_BLUE = wx.Window.NewControlId()
        self.ID_MENU_TAG_COLOR_VIOLET = wx.Window.NewControlId()

        self.m_title = self.GetTitle()
        self.__CreateControls()
        self.__CreateMenus()
        self.__CreateStatusAndVersion()
        self.__ConnectEvents()

        self.m_bookmarkDocument = BookMarkDocument()

        # computing minimum size
        # mysizepanel = bSizer5.ComputeFittingWindowSize(self)
        # self.SetMinSize([mysizebutton[0] + mysizepanel[0], mysizebutton[1]])
        self.SetSize([900, 600])
        self.Layout()
        self.Centre(wx.BOTH)

        # autoload project if needed
        self.m_config = wx.FileConfig("bookmaction")
        myfile = self.m_config.Read("AutoLoadFile", "")
        self.__OpenFile(myfile)

        # populate menu file history
        self.m_fileHistoryMenu.Load(self.m_config)

        # End of the control definition
        self.__SetDialogAppearance()

    def __CreateControls(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(bitmaps.bookmaction.GetBitmap())
        self.SetIcon(icon)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_listCtrl = BookMarkListCtrl(self.m_panel1)
        bSizer6.Add(self.m_listCtrl, 1, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_searchCtrl = wx.SearchCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(250, -1), style=wx.TE_PROCESS_ENTER)
        self.m_searchCtrl.ShowSearchButton(True)
        if (platform.system() == "Darwin"):
            self.m_searchCtrl.ShowCancelButton(True)

        bSizer7.Add(self.m_searchCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer6.Add(bSizer7, 0, wx.ALIGN_RIGHT, 5)

        self.m_panel1.SetSizer(bSizer6)
        self.m_panel1.Layout()
        bSizer6.Fit(self.m_panel1)
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)

        # create menu for SearchCtrl
        self.m_searchMenu = wx.Menu()
        self.m_searchMenu.AppendRadioItem(self.ID_SEARCH_ACTION, "Action")
        self.m_searchMenu.AppendRadioItem(self.ID_SEARCH_BOOKMARK, "BookMarks")
        self.m_searchMenu.AppendRadioItem(self.ID_SEARCH_DESCRIPTION, "Description")
        self.m_searchMenu.Check(self.ID_SEARCH_BOOKMARK, True)
        self.m_searchCtrl.SetMenu(self.m_searchMenu)

    def __SetDialogAppearance(self):
        myAppearance = self.m_config.ReadInt("Appearance", 0)
        if (myAppearance == 0):  # light mode
            pass  # do nothing for light mode
            # self.SetBackgroundColour(wx.Colour(236,236,236))
            # self.SetForegroundColour(wx.BLACK)
        else:
            self.SetBackgroundColour(wx.Colour(45, 45, 45))
            self.m_searchCtrl.SetForegroundColour(wx.Colour(221, 221, 221))

    def __CreateMenus(self):
        self.m_fileHistoryMenu = wx.FileHistory(maxFiles=5, idBase=wx.ID_FILE1)
        self.m_menu_tag_names = ["No Color", "Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        self.m_menu_tag_colors = [wx.NullColour, wx.RED, wx.Colour(253, 177, 80), wx.YELLOW, wx.GREEN, wx.BLUE,
                                  wx.Colour(190, 119, 226)]
        self.m_menu_tag_ids = [self.ID_MENU_TAG_COLOR_NONE, self.ID_MENU_TAG_COLOR_RED, self.ID_MENU_TAG_COLOR_ORANGE,
                               self.ID_MENU_TAG_COLOR_YELLOW, self.ID_MENU_TAG_COLOR_GREEN, self.ID_MENU_TAG_COLOR_BLUE,
                               self.ID_MENU_TAG_COLOR_VIOLET]

        # menubar
        self.m_menubar = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuNew = wx.MenuItem(self.m_menu1, wx.ID_NEW, u"New" + u"\t" + u"Ctrl+N", wx.EmptyString,
                                     wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuNew)

        self.m_menuOpen = wx.MenuItem(self.m_menu1, wx.ID_OPEN, u"Open" + u"\t" + u"Ctrl+O", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuOpen)

        self.m_menuSave = wx.MenuItem(self.m_menu1, wx.ID_SAVE, u"Save" + u"\t" + u"Ctrl+S", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuSave)

        self.m_menuSaveAs = wx.MenuItem(self.m_menu1, wx.ID_SAVEAS, u"Save as...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuSaveAs)

        self.m_menu1.AppendSeparator()

        self.subMenu = wx.Menu()
        self.m_fileHistoryMenu.UseMenu(self.subMenu)
        self.m_fileHistoryMenu.AddFilesToMenu()
        self.m_menu1.AppendSubMenu(self.subMenu, "Recent Files...")

        self.m_menu1.AppendSeparator()

        self.m_menuSettings = wx.MenuItem(self.m_menu1, wx.ID_PREFERENCES, u"Settings...", wx.EmptyString,
                                          wx.ITEM_NORMAL)
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

        self.m_menuBookEdit = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Edit..." + u"\t" + u"Ctrl+E", wx.EmptyString,
                                          wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuBookEdit)

        self.m_menuTag = wx.Menu()

        for index in range(len(self.m_menu_tag_names)):
            my_menu = wx.MenuItem(self.m_menuTag, self.m_menu_tag_ids[index], self.m_menu_tag_names[index],
                                  wx.EmptyString, wx.ITEM_NORMAL)
            self.m_menuTag.Append(my_menu)

        self.m_menu2.AppendSubMenu(self.m_menuTag, u"Tag")

        self.m_menubar.Append(self.m_menu2, u"Bookmarks")

        self.m_menu3 = wx.Menu()
        self.m_menuAbout = wx.MenuItem(self.m_menu3, wx.ID_ABOUT, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_menuAbout)

        self.m_menuWebsite = wx.MenuItem(self.m_menu3, wx.ID_ANY, u"website...", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_menuWebsite)

        self.m_menubar.Append(self.m_menu3, u"About")

        self.SetMenuBar(self.m_menubar)

    def __ConnectEvents(self):
        # connect events
        self.Bind(wx.EVT_MENU, self.OnWebSite, id=self.m_menuWebsite.GetId())
        self.Bind(wx.EVT_MENU, self.OnBookMarkMenuAdd, id=self.m_menuBookAdd.GetId())
        self.Bind(wx.EVT_MENU, self.OnBookMarkMenuEdit, id=self.m_menuBookEdit.GetId())
        self.Bind(wx.EVT_MENU, self.OnBookMarkMenuDelete, id=self.m_menuBookRemove.GetId())
        self.Bind(wx.EVT_MENU, self.OnSettingsMenu, id=self.m_menuSettings.GetId())

        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnFileNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnFileOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnFileSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnFileSaveAs, id=wx.ID_SAVEAS)

        self.Bind(wx.EVT_IDLE, self.OnUpdateIdle)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        my_history_list = [wx.ID_FILE1, wx.ID_FILE2, wx.ID_FILE3, wx.ID_FILE4, wx.ID_FILE5]
        for item in my_history_list:
            self.Bind(wx.EVT_MENU, self.OnFileOpenHistory, id=item)

        self.m_searchCtrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearch)
        self.m_searchCtrl.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch)
        self.m_searchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_NONE)
        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_RED)
        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_ORANGE)
        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_YELLOW)
        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_GREEN)
        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_BLUE)
        self.Bind(wx.EVT_MENU, self.OnTagMenu, id=self.ID_MENU_TAG_COLOR_VIOLET)

    def OnSearch(self, event):
        column = 0  # action column
        if (self.m_searchMenu.IsChecked(self.ID_SEARCH_BOOKMARK)):
            column = 1
        elif (self.m_searchMenu.IsChecked(self.ID_SEARCH_DESCRIPTION)):
            column = 2
        self.m_bookmarkDocument.SetBookMarksToList(self.m_listCtrl, filtertext=event.GetString(), filtercolumn=column)
        event.Skip()

    def OnTagMenu(self, event):
        my_id = event.GetId()
        my_index = self.m_menu_tag_ids.index(my_id)
        # wx.LogMessage("Tag menu pressed, color : {}".format(self.m_menu_tag_names[my_index]))

        # temporary code
        if (self.m_listCtrl.IsValidSelectedItem() == False):
            return

        my_listindex = self.m_listCtrl.GetFirstSelected()
        my_colour = self.m_menu_tag_colors[my_index]
        self.m_listCtrl.SetItemTextColour(my_listindex, my_colour)

    def __CreateStatusAndVersion(self):
        self.CreateStatusBar(2)
        self.SetStatusText(self.__GetGitVersion(), 1)

    def __GetGitVersion(self):
        return "version: " + str(version.COMMIT_NUMBER) + " (" + version.COMMIT_ID + ")"

    def __del__(self):
        pass

    def OnQuit(self, event):
        self.Close()

    def OnWebSite(self, event):
        wx.LaunchDefaultBrowser("https://github.com/lucsch/bookmaction")

    def OnAbout(self, event):
        my_dlg = AboutDlg(self, self.m_title)
        my_dlg.ShowModal()

    def OnBookMarkMenuAdd(self, event):
        self.m_bookmarkDocument.BookMarkAdd(self.m_listCtrl)

    def OnBookMarkMenuEdit(self, event):
        self.m_bookmarkDocument.BookMarkEdit(self.m_listCtrl)

    def OnBookMarkMenuDelete(self, event):
        self.m_bookmarkDocument.BookMarkDelete(self.m_listCtrl)

    def OnSettingsMenu(self, event):
        mydlg = SettingsDlg(self, self.m_config)
        mydlg.ShowModal()

    def OnFileSave(self, event):
        if (self.m_bookmarkDocument.m_docName == ""):
            return self.OnFileSaveAs(event)

        self.__SaveFile(self.m_bookmarkDocument.m_docName)

    def OnFileSaveAs(self, event):
        mydlg = wx.FileDialog(self, "Save Bookmaction project", wildcard="BMKA files (*.bmka)|*.bmka",
                              style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (mydlg.ShowModal() == wx.ID_CANCEL):
            return

        self.__SaveFile(mydlg.GetPath())

    def __SaveFile(self, filename):
        self.m_bookmarkDocument.GetBookMarksFromList(self.m_listCtrl)
        self.m_bookmarkDocument.SaveObject(filename)

    def OnFileNew(self, event):
        if (self.m_bookmarkDocument.m_isModified == True):
            if (self.__ProjectQuestion("creating new project") == False):
                return
        self.m_bookmarkDocument.ClearDocument()
        self.m_bookmarkDocument.SetBookMarksToList(self.m_listCtrl)

    def OnFileOpen(self, event):
        mydlg = wx.FileDialog(self, "Open Bookmaction project", wildcard="BMKA files (*.bmka)|*.bmka",
                              style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if (mydlg.ShowModal() == wx.ID_CANCEL):
            return

        self.__OpenFile(mydlg.GetPath())

    def OnFileOpenHistory(self, event):
        my_menu_id = [wx.ID_FILE1, wx.ID_FILE2, wx.ID_FILE3, wx.ID_FILE4, wx.ID_FILE5].index(event.GetId())
        self.__OpenFile(self.m_fileHistoryMenu.GetHistoryFile(my_menu_id))

    def __OpenFile(self, filename):
        if (filename == ""):
            return False

        if (os.path.exists(filename) == False):
            wx.LogError("The file : {} didn't exists".format(filename))
            self.__RemoveFileFromHistory(filename)
            return False

        if (self.m_bookmarkDocument.LoadObject(filename) == True):
            self.m_fileHistoryMenu.AddFileToHistory(filename)
        else:
            self.__RemoveFileFromHistory(filename)
            pass
        self.m_bookmarkDocument.SetBookMarksToList(self.m_listCtrl)

    def __RemoveFileFromHistory(self, filename):
        for index in range(self.m_fileHistoryMenu.GetCount()):
            my_file = self.m_fileHistoryMenu.GetHistoryFile(index)
            if (filename == my_file):
                self.m_fileHistoryMenu.RemoveFileFromHistory(index)
                return

    def OnUpdateIdle(self, event):
        # set document name
        mydocname = self.m_bookmarkDocument.m_docName
        mytitletext = ""
        if (mydocname == ""):
            mytitletext = self.m_title + " - " + "untitled"
        else:
            mytitletext = self.m_title + " - " + mydocname

        if (self.m_bookmarkDocument.m_isModified == True):
            mytitletext = mytitletext + "*"

        self.SetTitle(mytitletext)

        # compute the number of items in the list
        my_text = "{} visible / {} total items".format(self.m_listCtrl.GetCountVisible(),
                                                       len(self.m_bookmarkDocument.m_bookMarksList))
        self.GetStatusBar().SetStatusText(my_text, 0)

    def OnClose(self, event):
        if (event.CanVeto() and self.m_bookmarkDocument.m_isModified == True):
            if (self.__ProjectQuestion("closing") == False):
                event.Veto()
                return
        self.m_fileHistoryMenu.Save(self.m_config)
        event.Skip()

    def __ProjectQuestion(self, text):
        myprojname = self.m_bookmarkDocument.m_docName
        if (myprojname == ""):
            myprojname == "untitled"

        myanswer = wx.MessageBox("Project {} was modified, Save modification before {}".format(myprojname, text),
                                 "Project modified",
                                 wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL, self)
        if (myanswer == wx.YES):
            self.OnFileSave(wx.CommandEvent())
            return True
        elif (myanswer == wx.NO):
            return True
        return False


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
