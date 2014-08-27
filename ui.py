#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
import wx.grid as  gridlib
import sys
import os
import time


class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.frmPanel = wx.Panel(self)
        
        self.PhotoMaxSize = 240
        self.frmPanel.SetBackgroundColour('White')
        self.InitUI()
        
    def InitUI(self):    
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        menubar = wx.MenuBar()
        topMenu = {'&File':['Add a book(s)', 'Restart', '&Quit \t Crtl+Q'], '&Edit':['Undo', 'Redo', 'Edit a book info', 'Edit a book info in bulk'], 'Preferences':[], '&View':[], '&Help':['About Better Calibre']}
        tomMenuKey = ('&File', '&Edit', 'Preferences', '&View', '&Help')
        i=1
        j=1
        
        for key in tomMenuKey:
            menu = wx.Menu()
            print key, topMenu[key]
            for v in topMenu[key]:
                print v
                print i, j
                menu.Append(i*10+j, v, v)
                
                j=j+1
            print topMenu[key]
            menubar.Append(menu, key)
            i=i+1

        viewMenu = wx.Menu()
        # helpMenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=13)
        self.Bind(wx.EVT_MENU, self.OnRestart, id=12)
        
        
        
        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statubar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar', 'Show Toolbar', kind=wx.ITEM_CHECK)
            
        viewMenu.Check(self.shst.GetId(), True)
        viewMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)

        # menubar.Append(fileMenu, '&File')
        menubar.Append(viewMenu, '&View')
        # menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        # self.toolbar.AddLabelTool(1, '', wx.Bitmap('../img/new.png'))
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')


#         instructions = 'Browse for an image'
#         img = wx.EmptyImage(240, 240)
#         self.imageCtrl = wx.StaticBitmap(wx.Panel(self), wx.ID_ANY, wx.BitmapFromImage(img))
#         instructLbl = wx.StaticText(self.panel, label=instructions)
#         self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))
#        # browseBtn = wx.Button(self.panel, label='Browse')
#         #browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
#         self.mainSizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer = wx.BoxSizer(wx.HORIZONTAL)
#         self.sizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)
#         self.sizer.Add(instructLbl, 0, wx.ALL, 5)
#         self.sizer.Add(self.imageCtrl, 0, wx.ALL, 5)
#         self.SetSizer(self.sizer)
#         self.SetAutoLayout(1)
        
        # Creating Grid Panel
        self.gridPnl = wx.Panel(self.frmPanel)
        self.grid = gridlib.Grid(self.gridPnl)
        self.grid.CreateGrid(25, 8)
        self.grid.SetRowLabelSize(30)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 5)
        self.gridPnl.SetSizer(sizer)
        self.grid.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.showPopupMenu)
        
        
        # Add another panel and some buttons
        self.colourPnl = wx.Panel(self.frmPanel)
        self.colourPnl.SetBackgroundColour('GRAY')
        self.redBtn = wx.Button(self.frmPanel, label='Red')
        self.greenBtn = wx.Button(self.frmPanel, label='Green')
        self.exitBtn = wx.Button(self.frmPanel, label='Exit')

        # Add them to sizer.
        colorPnlAndBtn_vSizer = wx.BoxSizer(wx.VERTICAL)
        colorPnlAndBtn_vSizer.Add(self.colourPnl, 1, wx.EXPAND | wx.ALL, 1)
        colorPnlAndBtn_vSizer.Add(self.gridPnl, 1, wx.EXPAND | wx.ALL, 1)

        # Add buttons in their own sizer
        btn_hSizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_hSizer.AddStretchSpacer()
        btn_hSizer.Add(self.redBtn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        btn_hSizer.Add(self.greenBtn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        btn_hSizer.Add(self.exitBtn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        btn_hSizer.AddStretchSpacer()

        # colorPnlAndBtn_vSizer.Add(btn_hSizer, 0, wx.EXPAND | wx.ALL, 5)

        # SetSizer both sizers in the most senior control that has sizers in it.
        self.frmPanel.SetSizer(colorPnlAndBtn_vSizer)
        self.frmPanel.Layout()

#-----

        # Must call before any event handler is referenced.
        self.eventsHandler = EventsHandler(self)

        # Bind event handlers to all controls that have one.
        self.redBtn.  Bind(wx.EVT_BUTTON, self.eventsHandler.OnRedBtn)
        self.greenBtn.Bind(wx.EVT_BUTTON, self.eventsHandler.OnGreenBtn)
        self.exitBtn. Bind(wx.EVT_BUTTON, self.eventsHandler.OnExitBtn)

        # Create more convenient ways to close this app.
        # Adding these makes a total of 5 separate ways to exit.
        self.frmPanel .Bind(wx.EVT_LEFT_DCLICK, self.eventsHandler.OnExitBtn)
        self.colourPnl.Bind(wx.EVT_LEFT_DCLICK, self.eventsHandler.OnExitBtn)
#         self.sizer = wx.BoxSizer(wx.HORIZONTAL)
#         self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
#         self.buttons = []
#         for i in range(0, 6):
#             self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
#             self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)
# 
#         # Use some sizers to see layout options
#         self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer.Add(self.control, 1, wx.EXPAND)
#         self.sizer.Add(self.sizer2, 0, wx.EXPAND)
# 
#         #Layout sizers
#         self.SetSizer(self.sizer)
#         self.SetAutoLayout(1)
#         self.sizer.Fit(self)
        # setup taskbar icon
        # tbicon = wx.TaskBarIcon()
        # tbicon.SetIcon(icon, "I am an Icon")
        
        # add taskbar icon event
        # wx.EVT_TASKBAR_RIGHT_UP(tbicon, OnTaskBarRight)
#         image = wx.Image('../img/Bible.ico', wx.BITMAP_TYPE_ANY).ConvertToBitmap() 
#         icon = wx.EmptyIcon() 
#         icon.CopyFromBitmap(image) 
#         self.SetIcon(icon) 
        # favicon = wx.Icon('../img/new.png', wx.BITMAP_TYPE_ANY, 16, 16)
        # self.SetIcon(favicon)
#         self.icon = wx.Icon(fn, wx.BITMAP_TYPE_ICO)
#         self.SetIcon(self.icon)
        self.SetSize((350, 250))
        self.SetTitle('Better Calibre')
        self.Centre()
        self.Show(True)
     
       
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
        
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard, style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()
        
    def ToggleStatusBar(self, e):
        
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):
        
        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide() 
            
    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()
    
    def OnQuit(self, event):
        self.Close()
        
    def OnRightDown(self, e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())

    def OnRestart(self,event):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        self.Close()
        self.Destroy()
        self.Show(False)
        time.sleep(5)
        main()
        
        #----------------------------------------------------------------------
    def showPopupMenu(self, event):
        """
        Create and display a popup menu on right-click event
        """
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            # make a menu
 
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "One")
        menu.AppendItem(item)
        menu.Append(self.popupID2, "Two")
        menu.Append(self.popupID3, "Three")
 
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
        
class MyPopupMenu(wx.Menu):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        super(MyPopupMenu, self).__init__()
        
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)


    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()    

#------------------------------------------------------------------------------

class EventsHandler() :

    def __init__(self, parent) :
        self.parent = parent

    def OnRedBtn(self, event) :
        self.ShowColourAndDialog(wx.RED)

    def OnGreenBtn(self, event) :
        self.ShowColourAndDialog(wx.GREEN)

    def ShowColourAndDialog(self, pnlColour) :

        self.parent.colourPnl.SetBackgroundColour(pnlColour)
        self.parent.colourPnl.Refresh()
        dlg = wx.MessageDialog(self.parent, 'Changed colour !', 'Successful', style=wx.ICON_INFORMATION | wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExitBtn(self, event) :
        self.parent.Destroy()

# end Events class

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
