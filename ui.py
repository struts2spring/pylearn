#!/usr/bin/python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from wx.html import HtmlWindow
import json
import logging
import os
import sys
import time
import wx.grid

 
Base = declarative_base()



# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# create logger
logger = logging.getLogger('it-ebook')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('itebook.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

class Book(Base):
    """A Book class is an entity having database table."""
    
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bookName = Column('book_name', String(46), nullable=False)  # Title
    isbn_10 = Column(String)  # Title
    isbn_13 = Column(String)  # Title
    series = Column(String)  # Title
    dimension = Column(String)  # Title
    customerReview = Column('customer_review', String)  # Title
    bookDescription = Column('book_description', String)  # Title
    editionNo = Column('edition_no', String)  # Title
    publisher = Column(String)  # Title
    bookFormat = Column("book_format", String)  # Title
    fileSize = Column('file_size', String)  # Title
    numberOfPages = Column('number_of_pages', String)  # Title
    inLanguage = Column('in_language', String)  # Title
    publishedOn = Column('published_on', DateTime, default=func.now())
    hasCover = Column('has_cover', String)  # Title
    bookPath = Column('book_path', String)  # Title
    rating = Column('rating', String)  # Title
    uuid = Column('uuid', String)  # Title
    createdOn = Column('created_on', DateTime, default=func.now())
    authors = relationship(
        'Author',
        secondary='author_book_link'
    )
    
#     def __repr__(self):
#         rep=''
#         print self.__dict__
#         return  ''
# 
#     def __str__(self):
#         return ''
    
class Author(Base):
    """A Author class is an entity having database table."""
    
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    authorName = Column('author_name', String(46), nullable=False, autoincrement=True)
    aboutAuthor = Column('about_author', String)
    email = Column(String, unique=True)
    created_on = Column(DateTime, default=func.now())
    
    books = relationship(
        Book,
        secondary='author_book_link'
    )
 
 
class AuthorBookLink(Base):
    """A AuthorBookLink class is an entity having database table. This class is for many to many association between Author and Book."""
    
    __tablename__ = 'author_book_link'
    id = Column(Integer, primary_key=True)
    authorId = Column('book_id', Integer, ForeignKey('author.id'))
    bookId = Column('author_id', Integer, ForeignKey('book.id'))
    extra_data = Column(String(256))
    author = relationship(Author, backref=backref("book_assoc"))
    book = relationship(Book, backref=backref("dauthor_assoc"))

class CreateDatabase:
    
    def creatingDatabase(self):
        # engine = create_engine('sqlite:///calibre.sqlite', echo=True)
        engine = create_engine('sqlite:///calibre.sqlite', echo=True)
        session = sessionmaker()
        
        
        session.configure(bind=engine)
#         Base.metadata.drop_all(engine)
        
        Base.metadata.create_all(engine)
#         metadata = Base.metadata
#         for t in metadata.sorted_tables:
#             print t.name
#         pass
        return session
        
    def addingData(self, session):
        directory_name = '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books'
        listOfDir = os.listdir(directory_name)
        listOfDir.sort(key=int)
        one = ''
        # create a Session
        sess = session()
        
        for sName in listOfDir:
            one = directory_name + "/" + sName
            # print one
            file = open(one + "/book.json", 'r')
            
            rep = ''
            for line in file:
                rep = rep + line
            file.close
            # print str(rep)
            b = json.loads(rep)
            
            book = Book(bookName=b["name"], fileSize=b["fileSize"], hasCover='Y', bookPath=one , bookDescription=b["bookDescription"], publisher=b["publisher"], isbn_13=b["isbn"], numberOfPages=b["numberOfPages"], bookFormat=b["bookFormat"], inLanguage=b["inLanguage"])
            # book.bookName='one'
             
            author = Author(authorName=b["author"])
            authorList = list()
            authorList.append(author)
            book.authors = authorList
             
            authorBookLink = AuthorBookLink()
            authorBookLink.author = author
            authorBookLink.book = book
            sess.add(authorBookLink)
            
        sess.commit()

    def findAllBook(self, session):
        bs = session().query(Book).limit(3).all()
        return bs

    def findByBookName(self, session, bookName):
        query = session().query(Book).filter(Book.bookName.like('%'+bookName+'%'))
        bs = query.all()
        return bs


class SearchTextValidator(wx.PyValidator):
    """ This validator is used to ensure that the user has entered something
        into the text object editor dialog's text field.
    """
    def __init__(self):
        """ Standard constructor.
        """
        wx.PyValidator.__init__(self)
    
    
    
    def Clone(self):
        """ Standard cloner.
    
            Note that every validator must implement the Clone() method.
        """
        return SearchTextValidator()
    
    
    def Validate(self, win):
        """ Validate the contents of the given text control.
        """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
    
        if len(text) == 0:
            wx.MessageBox("A text object must contain some text!", "Error")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True
    
    
    def TransferToWindow(self):
        """ Transfer data from validator to window.
    
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.
    
    
    def TransferFromWindow(self):
        """ Transfer data from window to validator.
    
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.
    

aboutText = """<p>Sorry, there is no information about this program. It is
running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>"""
 
class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class MainWindow(wx.Frame):

    def __init__(self, parent, title,  *args, **kwargs):
        super(MainWindow, self).__init__(parent, title=title, size=wx.DisplaySize())
        self.frmPanel = wx.Panel(self)
        global books
        self.books = books
#         self.PhotoMaxSize = 240
#         self.frmPanel.SetBackgroundColour('sky blue')
        self.InitUI()
        
    def InitUI(self):    
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.items=list()
        menubar = wx.MenuBar()
        topMenu = (
                   {'&File':[
                                 {'addBooks':['Add a book(s)', 'normal','addBooks.png'] },
                                 {'restart':['Restart', 'normal','restart.png']},
                                 {'quite':['&Quit\tCtrl+Q', 'normal','quite.png']}
                             ]
                    },
                   {'&Edit':[
                             {'undo':['Undo', 'normal','undo.png']},
                             {'redo':['Redo', 'normal','redo.png']},
                             {'editBook':['Edit a book info', 'normal','editBook.png']},
                             {'editBooks':['Edit a book info in bulk', 'normal','editBooks.png']}
                             ]
                    },
                   {'Preferences':[]
                    },
                   {'&View':[
                             {'statusBar':['Show status bar', 'check','statusBar.png']},
                             {'toolbar':['Show toolbar', 'check','toolbar.png']}
                             ]
                    },
                   {'&Help':[
                             {'aboutCalibre':['About Better Calibre', 'normal','aboutCalibre.png']}
                             ]
                    }
                   )
        
        i = 1
        j = 1
        for topLevel in topMenu:
            topLevelMenu = wx.Menu()  # Top level
            for k, topLevelItems in topLevel.iteritems():
                items=list()
                for topLevelItem in topLevelItems:
                    for child, childValue in topLevelItem.iteritems():
                        print child, childValue
                        kind_value = None
                        if 'normal' == childValue[1]:
                            kind_value = wx.ITEM_NORMAL
                        elif 'radio' == childValue[1]:
                            kind_value = wx.ITEM_RADIO
                        elif 'check' == childValue[1]:
                            kind_value = wx.ITEM_CHECK
                        
                        item =topLevelMenu.Append(i * 10 + j, childValue[0], childValue[0], kind=kind_value)
                        item.SetBitmap(wx.Bitmap('icons/rectangle.png'))
                        if 'check' == childValue[1]:
                            item.Check()
                        
                        items.append(item)
                    j = j + 1
                self.items.append(items)
#                 topLevelMenu.Append(-1,childMenu)
            menubar.Append(topLevelMenu, k)
            print menubar
            i = i + 1

        print 'items'
        print self.items[4][0]

        self.Bind(wx.EVT_MENU, self.OnQuit, id=13)
        self.Bind(wx.EVT_MENU, self.OnRestart, id=12)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.items[4][0])

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.items[3][0])
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.items[3][1])

        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        if os.path.exists("icons/rectangle.png"):
            self.toolbar.AddLabelTool(1, '', wx.Bitmap('icons/rectangle.png'))
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        # Creating Grid Panel
        self.gridPanel = wx.Panel(self.frmPanel)
        self.grid = wx.grid.Grid(self.gridPanel)
        # self.grid.CreateGrid(25, 8)
        self.grid.SetRowLabelSize(30)
        vBoxGrid = wx.BoxSizer(wx.VERTICAL)
        vBoxGrid.Add(self.grid, 1, wx.EXPAND, 5)
        self.gridPanel.SetSizer(vBoxGrid)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.showPopupMenu)

        # Then we call CreateGrid to set the dimensions of the grid
        numOfRows = 0
        global books
        self.books=books
        print 'printing grid'
        print  self.books
        if self.books:
            numOfRows = len(self.books)
        self.grid.CreateGrid(numOfRows, 10)

        # We can set the sizes of individual rows and columns
        # in pixels
#         self.grid.SetRowSize(0, 80)
#         self.grid.SetColSize(0, 120)
        self.grid.SetColLabelValue(0, "Title")
        self.grid.SetColLabelValue(1, "Author")
        self.grid.SetColLabelValue(2, "isbn-13")
        self.grid.SetColLabelValue(3, "publisher")
        self.grid.SetColLabelValue(4, "size(MB)")
        self.grid.SetColLabelValue(5, "Format")
        self.grid.SetColLabelValue(6, "Path")
        
        # And set grid cell contents as strings
        rowNum = 0
        for book in self.books:
            print book.id
            self.grid.SetCellValue(rowNum, 0, book.bookName)
            self.grid.SetCellValue(rowNum, 1, book.authors[0].authorName)
            self.grid.SetCellValue(rowNum, 2, book.isbn_13)
            self.grid.SetCellValue(rowNum, 3, book.publisher)
            if book.fileSize:
                self.grid.SetCellValue(rowNum, 4, book.fileSize)
            else:
                self.grid.SetCellValue(rowNum, 4, '0')
            self.grid.SetCellValue(rowNum, 5, book.bookFormat)
            self.grid.SetCellValue(rowNum, 6, book.bookPath)
            rowNum = rowNum + 1
            
            
            
        # Add another panel and some buttons
#         self.colourPnl = wx.Panel(self.frmPanel)
#         self.colourPnl.SetBackgroundColour('GRAY')
#         self.redBtn = wx.Button(self.frmPanel, label='Red')
#         self.greenBtn = wx.Button(self.frmPanel, label='Green')
#         self.exitBtn = wx.Button(self.frmPanel, label='Exit')

        self.searchPanel = wx.Panel(self.frmPanel)
        self.searchText = wx.TextCtrl(self.searchPanel, id=100,style=0,value="Enter here your name", name=" Search: ", validator=SearchTextValidator())
        self.searchLabel = wx.StaticText(self.searchPanel, -1, label="Search")
        self.searchButton = wx.Button(self.searchPanel, label="search")
        self.hboxSearchPanel= wx.BoxSizer (wx.HORIZONTAL)
        self.hboxSearchPanel.Add(self.searchLabel, flag=wx.CENTER)
        self.hboxSearchPanel.Add(self.searchText,proportion=1, flag=wx.CENTER)
        self.hboxSearchPanel.Add(self.searchButton, flag=wx.CENTER)
        self.vBoxSearchPanel = wx.BoxSizer(wx.VERTICAL)
        self.vBoxSearchPanel.Add(self.hboxSearchPanel, proportion=1, flag=wx.EXPAND)
        self.searchPanel.SetSizerAndFit(self.vBoxSearchPanel)
        
        self.searchText.SetFocus()
        self.Bind(wx.EVT_TEXT, self.EvtText, self.searchText)
#         self.Bind(wx.EVT_TEXT, self.OnKeyDown, self.searchText)
        
        # Add them to sizer.
        vBox = wx.BoxSizer(wx.VERTICAL)
# #         vBox.Add(self.colourPnl, 1, wx.EXPAND | wx.ALL, 1)
#         vBox.Add(self.hboxSearchPanel, proportion=1, flag=wx.EXPAND)
        vBox.Add(self.searchPanel, .1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(self.gridPanel, 9, wx.EXPAND | wx.ALL, 1)
# 
# 
#         # Add buttons in their own sizer
#         btn_hSizer = wx.BoxSizer(wx.HORIZONTAL)
#         btn_hSizer.AddStretchSpacer()
#         btn_hSizer.Add(self.redBtn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
#         btn_hSizer.Add(self.greenBtn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
#         btn_hSizer.Add(self.exitBtn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
#         btn_hSizer.AddStretchSpacer()
# 
#         # colorPnlAndBtn_vSizer.Add(btn_hSizer, 0, wx.EXPAND | wx.ALL, 5)
# 
#         # SetSizer both sizers in the most senior control that has sizers in it.
        self.frmPanel.SetSizer(vBox)
        self.frmPanel.Layout()

#-----

        # Must call before any event handler is referenced.
#         self.eventsHandler = EventsHandler(self)

#         # Bind event handlers to all controls that have one.
#         self.redBtn.  Bind(wx.EVT_BUTTON, self.eventsHandler.OnRedBtn)
#         self.greenBtn.Bind(wx.EVT_BUTTON, self.eventsHandler.OnGreenBtn)
#         self.exitBtn. Bind(wx.EVT_BUTTON, self.eventsHandler.OnExitBtn)

        # Create more convenient ways to close this app.
        # Adding these makes a total of 5 separate ways to exit.
#         self.frmPanel .Bind(wx.EVT_LEFT_DCLICK, self.eventsHandler.OnExitBtn)
#         self.colourPnl.Bind(wx.EVT_LEFT_DCLICK, self.eventsHandler.OnExitBtn)
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
     
    def gridActivity(self,bookName):
        print 'gridActivity'
        global books
        session = CreateDatabase().creatingDatabase()
#         CreateDatabase().addingData(session)
#         books = CreateDatabase().findAllBook(session)
#         self.grid.AppendRows(1)
        
        books = CreateDatabase().findByBookName(session, bookName)
        self.books=books
        print  self.books
        
        if self.books:
            numOfRows = len(self.books)
        self.grid.CreateGrid(numOfRows, 10)

        # We can set the sizes of individual rows and columns
        # in pixels
#         self.grid.SetRowSize(0, 80)
#         self.grid.SetColSize(0, 120)
        self.grid.SetColLabelValue(0, "Title")
        self.grid.SetColLabelValue(1, "Author")
        self.grid.SetColLabelValue(2, "isbn-13")
        self.grid.SetColLabelValue(3, "publisher")
        self.grid.SetColLabelValue(4, "size(MB)")
        self.grid.SetColLabelValue(5, "Format")
        self.grid.SetColLabelValue(6, "Path")
        
        # And set grid cell contents as strings
        rowNum = 0
        for book in self.books:
            print book.id
            self.grid.SetCellValue(rowNum, 0, book.bookName)
            self.grid.SetCellValue(rowNum, 1, book.authors[0].authorName)
            self.grid.SetCellValue(rowNum, 2, book.isbn_13)
            self.grid.SetCellValue(rowNum, 3, book.publisher)
            if book.fileSize:
                self.grid.SetCellValue(rowNum, 4, book.fileSize)
            else:
                self.grid.SetCellValue(rowNum, 4, '0')
            self.grid.SetCellValue(rowNum, 5, book.bookFormat)
            self.grid.SetCellValue(rowNum, 6, book.bookPath)
            rowNum = rowNum + 1
            
       
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
        
        if self.items[3][0].IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):
        
        if self.items[3][1].IsChecked():
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

    def OnRestart(self, event):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        self.Close()
        self.Destroy()
        self.Show(False)
        time.sleep(5)
        main()
        
    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()
        pass
    
    def OnFind(self, e):
        print 'finding'
        pass     
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
        
        
    def OnKeyDown(self, evt):
        print evt.GetKeyCode() 
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            return 
        
    def EvtText(self, event):
        global books
        t = event.GetEventObject() 
        print t
        key = event.GetKeyCode()
        print key
#         session = CreateDatabase().creatingDatabase()
#         CreateDatabase().addingData(session)
#         books = CreateDatabase().findAllBook(session)
#         self.grid.AppendRows(1)
#         bookName = event.GetString()
#         books = CreateDatabase().findByBookName(session, bookName)
#         print len(books)
        
#         self.gridActivity(bookName)
        logger.info('EvtText: %s\n' % event.GetString())  
        
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
    session = CreateDatabase().creatingDatabase()
#     CreateDatabase().addingData(session)
#     books = CreateDatabase().findAllBook(session)
    bookName = 'Tinkering'
    global books,frame
    books = CreateDatabase().findByBookName(session, bookName)
    print books
    app = wx.App(0)
    frame = MainWindow(None, "My Calibre")
    app.MainLoop()    


if __name__ == '__main__':
    main()
    
