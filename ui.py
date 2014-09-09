#!/usr/bin/python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from wx.html import HtmlWindow, HW_DEFAULT_STYLE
import json
import logging
import math
import os
import sys
import time
import wx.grid
import wx.lib.agw.aui as aui
import wx.lib.mixins.gridlabelrenderer as glr
import wx
import wx.webkit
import wx.html
 
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
# tell the handler to use this format
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
    subTitle = Column('sub_title', String)  # Title
    isbn_10 = Column(String)  # isbn_10
    isbn_13 = Column(String)  # isbn_13
    series = Column(String)  # series
    dimension = Column(String)  # dimension
    customerReview = Column('customer_review', String)  # customerReview
    bookDescription = Column('book_description', String)  # bookDescription
    editionNo = Column('edition_no', String)  # editionNo
    publisher = Column(String)  # publisher
    bookFormat = Column("book_format", String)  # bookFormat
    fileSize = Column('file_size', String)  # fileSize
    numberOfPages = Column('number_of_pages', String)  # numberOfPages
    inLanguage = Column('in_language', String)  # inLanguage
    publishedOn = Column('published_on', DateTime, default=func.now())
    hasCover = Column('has_cover', String)  # hasCover
    hasCode = Column('has_code', String)  # hasCode
    bookPath = Column('book_path', String)  # bookPath
    rating = Column('rating', String)  # rating
    uuid = Column('uuid', String)  # uuid
    createdOn = Column('created_on', DateTime, default=func.now())
    authors = relationship(
        'Author',
        secondary='author_book_link', lazy='joined'
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
        engine = create_engine('sqlite:///calibre.sqlite', echo=False)
        session = sessionmaker()
        
        
        session.configure(bind=engine)
        Base.metadata.drop_all(engine)
        
        Base.metadata.create_all(engine)
#         metadata = Base.metadata
#         for t in metadata.sorted_tables:
#             print t.name
#         pass
        return session
        
    def addingData(self, session):
#         directory_name = '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books'
        directory_name = os.path.join(os.getcwd(), 'books')
        os.chdir(directory_name)
#         os.mkdir(os.path.join( os.getcwd(),'books'))
        print directory_name
        listOfDir = [ name for name in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, name)) ]
        print listOfDir
        if listOfDir:
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
                
            print rep
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
        query = session().query(Book).filter(Book.bookName.like('%' + bookName + '%'))
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
        return True  # Prevent wxDialog from complaining.
    
    
    def TransferFromWindow(self):
        """ Transfer data from window to validator.
    
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True  # Prevent wxDialog from complaining.
    

aboutText = """<p>Sorry, there is no information about this program. It is
running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>"""
 
class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>",
            style=wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME | wx.RESIZE_BORDER | 
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(600, 400))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

########################################################################
class TabPanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    def _init_ctrls(self, prnt):
        wx.Panel.__init__(self, style=wx.TAB_TRAVERSAL | wx.NO_BORDER, name='', parent=prnt, pos=(0, 0), size=wx.Size(200, 100))

#     def __init__(self, parent, id, pos, size, style, name):
#         self._init_ctrls(parent)
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        # list containing notebook images:
        # .ico seem to be more OS portable 
    
     
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        
    def addItems(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid = MainGrid(self)

        vbox.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(vbox)
        pass
    
    def addHtml(self):
        self.html = wx.html.HtmlWindow(self)
        self.html.SetPage("Here is some <b>formatted</b> <i><u>text</u></i> "
            "loaded from a <font color=\"red\">string</font>.")
        pass
########################################################################
class MainBookTab(aui.AuiNotebook):
    """
    Notebook class
    """
    DEFAULT_STYLE = aui.AUI_NB_MIDDLE_CLICK_CLOSE | \
                   aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | \
                   aui.AUI_NB_SCROLL_BUTTONS | \
                   aui.AUI_NB_TAB_MOVE | \
                   aui.AUI_NB_TAB_SPLIT | \
                   aui.AUI_NB_TOP | \
                   wx.NO_BORDER
    
    directory_name = os.path.join(os.getcwd(), 'books', '1', 'book.jpg')
    print directory_name
    defaultPage = ''' 
    <!DOCTYPE html>
<html>
    
    <body>
            <a target="_blank" href="klematis_big.htm"><img src="''' + directory_name + '''" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200" ></a>
            <a target="_blank" href="klematis2_big.htm"><img src="''' + directory_name + '''" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200" ></a>
            <a target="_blank" href="klematis3_big.htm"><img src="''' + directory_name + '''" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200" ></a>
            <a target="_blank" href="klematis4_big.htm"><img src="''' + directory_name + '''" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200" ></a>

    </body>
</html>

    '''
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        aui.AuiNotebook.__init__(self, parent=parent)
        self.default_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self.SetWindowStyleFlag(self.default_style)
        
        # Create the first tab and add it to the notebook
        self.gallery = TabPanel(self)
        
        html = wx.html.HtmlWindow(self.gallery, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(800, 800), style=HW_DEFAULT_STYLE)
        self.gallery.SetDoubleBuffered(True)
#         self.t = wx.StaticText(self.tabTwo , -1, "This is a PageOne object", (20,20))
#         html = wx.html.HtmlWindow(self.tabTwo, pos=(20,20))
        html.SetPage(self.defaultPage)
        html.GetBestSize()
        
        
        self.tabOne = TabPanel(self)
        self.tabOne.addItems()
#         tabOne.SetBackgroundColour("Gray")
        self.AddPage(self.tabOne, "Books")
        page_bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER,
                                                wx.Size(16, 16))
        self.AddPage(self.gallery, "Gallery", False, page_bmp)
        style = self.DEFAULT_STYLE    

        self.SetWindowStyleFlag(style)
        self.SetArtProvider(aui.AuiDefaultTabArt())

        pass
  

class MainGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
#         self.grid = wx.grid.Grid(self)
        global books
        self.books = books
        numOfRows = 0
        if self.books:
            numOfRows = len(self.books)
            print 'numOfRows:', numOfRows
        self.CreateGrid(numOfRows, 10)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.showPopupMenu)
        self.SetColSize(0, 320)
        self.SetColSize(1, 220)
        self.SetColLabelValue(0, "Title")
        self.SetColLabelValue(1, "Author")
        self.SetColLabelValue(2, "publisher")
        self.SetColLabelValue(3, "isbn-13")
        self.SetColLabelValue(4, "size(MB)")
        self.SetColLabelValue(5, "Format")
        self.SetColLabelValue(6, "Path")
#         self.SetColLabelRenderer(0, MyCornerLabelRenderer(self))
        
        color = 'light gray'
        attr = self.cellAttr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(color)
        rowNum = 0
        for book in self.books:
            if rowNum % 2 == 0:
                for i in range(7):
                    self.SetAttr(rowNum, i, attr)
#             self.SetCellRenderer(rowNum, i,)
            self.SetCellValue(rowNum, 0, book.bookName)
            self.SetCellValue(rowNum, 1, book.authors[0].authorName)
            self.SetCellValue(rowNum, 2, book.publisher)
            self.SetCellValue(rowNum, 3, book.isbn_13)
            if book.fileSize:
                self.SetCellValue(rowNum, 4, book.fileSize)
            else:
                self.SetCellValue(rowNum, 4, '0')
            self.SetCellValue(rowNum, 5, book.bookFormat)
            self.SetCellValue(rowNum, 6, book.bookPath)
            rowNum = rowNum + 1
        
    def showPopupMenu(self, event):
        """
        Create and display a popup menu on right-click event
        """
        self.rowSelected = event.Row
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            # make a menu
            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnOpen, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OpenBook, id=self.popupID5)
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "Open book detail in New Tab.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_MENU, (16,16)))
        menu.AppendItem(item)
        
        item = wx.MenuItem(menu, self.popupID2, "Open containing folder.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU, (16,16)))
        menu.AppendItem(item)
        
        item = wx.MenuItem(menu, self.popupID3, "Search similar books.")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU, (16,16)))
        menu.AppendItem(item)
        
        item = wx.MenuItem(menu, self.popupID4,"Properties." )
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU, (16,16)))
        menu.AppendItem(item)
        
        item = wx.MenuItem(menu, self.popupID5,  "Open Book")
        item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, wx.ART_MENU, (16,16)))
        menu.AppendItem(item)
        
#         menu.Append(self.popupID2, "Open containing folder.")
#         menu.Append(self.popupID3, "Search similar books.")
#         menu.Append(self.popupID4, "Properties.")
#         menu.Append(self.popupID5, "Open Book")
 
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
 
    

    def OnPopupOne(self, event):
        logger.info("Popup one\n")
        tabTitle = self.Parent.grid.GetCellValue(self.rowSelected, 0)
        path = self.Parent.grid.GetCellValue(self.rowSelected, 6)
        listOfDirPath = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
        self.path = ''
        for sName in listOfDirPath:
            if 'jpg' == sName.split('.')[-1:][0]:
                self.path = path + '/' + sName
                print self.path
                
        self.page = '''
            <html>
                <body>
            
                    <div>
                        
                            <h1>Professional Java for Web Applications</h1>
            
                            <div>
                                <img src="''' + self.path + '''" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200"  />
                                <h3>Book Description</h3>
                                <p>
                                    This guide shows Java software developers and software engineers how to build complex web applications in an enterprise environment. You'll begin with an introduction to the Java Enterprise Edition and the basic web application, then set up a development application server environment, learn about the tools used in the development process, and explore numerous Java technologies and practices. The book covers industry-standard tools and technologies, specific technologies, and underlying programming concepts.
                                </p>
                            </div>
                            
                        </div>
                </body>
            </html>
            ''' 


        self.tabTwo = TabPanel(self.Parent.Parent)
        html = wx.html.HtmlWindow(self.tabTwo, id=wx.ID_ANY, pos=(0, 0), size=wx.DisplaySize())
        
#         html =  wx.webkit.web(self.tabTwo, id=wx.ID_ANY, pos=(0,0), size=(802,610))
        if 'gtk2' in wx.PlatformInfo:
            html.SetStandardFonts() 
        self.tabTwo.SetDoubleBuffered(True)
#         self.t = wx.StaticText(self.tabTwo , -1, "This is a PageOne object", (20,20))
#         html = wx.html.HtmlWindow(self.tabTwo, pos=(20,20))
        html.SetPage(self.page)
#         self.tabTwo.addHtml()
        self.Parent.Parent.AddPage(self.tabTwo, tabTitle)
        print 'tab creating'
    
    def OpenBook(self, event):
        logger.info("OpenBook\n")
        print self.rowSelected
#         self.grid=self.mainBookTab.tabOne.grid  
        FILE_NAME = ''
        FILE_NAME = "/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3082/Tinkering.pdf"
        # self.
        os.spawnlp(os.P_NOWAIT, 'evince', 'evince', FILE_NAME)

    def OnOpen(self, event):
        
        logger.info("Popup two\n")
        if sys.platform == 'win32':
            pass
#         import _winreg
#         path= r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon')
#         for root in (_winreg.HKEY_CURRENT_USER, _winreg.HKEY_LOCAL_MACHINE):
#             try:
#                 with _winreg.OpenKey(root, path) as k:
#                     value, regtype= _winreg.QueryValueEx(k, 'Shell')
#             except WindowsError:
#                 pass
#             else:
#                 if regtype in (_winreg.REG_SZ, _winreg.REG_EXPAND_SZ):
#                     shell= value
#                 break
#         else:grid
#             shell= 'Explorer.exe'
#         subprocess.Popen([shell, d])
        
        
    def OnPopupThree(self, event):
        logger.info("Popup three\n")

    def OnPopupFour(self, event):
        FILE_NAME = "/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3082/Tinkering.pdf"
#         import subprocess
#         subprocess.call(('cmd', '/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/3082', 'start', '', "Tinkering.pdf"))
        os.spawnlp(os.P_NOWAIT, 'evince', 'evince', FILE_NAME)
        logger.info("Popup four\n")


class MyCornerLabelRenderer(glr.GridLabelRenderer):
    def __init__(self):
        self._bmp = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_OTHER, (16, 16))
 
    def Draw(self, grid, dc, rect, rc):
        x = rect.left + (rect.width - self._bmp.GetWidth()) / 2
        y = rect.top + (rect.height - self._bmp.GetHeight()) / 2
        dc.DrawBitmap(self._bmp, x, y, True)

class MainWindow(wx.Frame):

    def __init__(self, parent, title, *args, **kwargs):
        super(MainWindow, self).__init__(parent, title=title, size=wx.DisplaySize())
        self.frmPanel = wx.Panel(self)
        global books
        self.books = books
#         self.PhotoMaxSize = 240
#         self.frmPanel.SetBackgroundColour('sky blue')
        self.InitUI()
        
    def InitUI(self):    
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.items = list()
        menubar = wx.MenuBar()
        topMenu = (
                   {'&File':[
                                 {'addBooks':['Add a book(s)', 'normal', 'addBooks.png'] },
                                 {'restart':['Restart', 'normal', 'restart.png']},
                                 {'quite':['&Quit\tCtrl+Q', 'normal', 'quite.png']}
                             ]
                    },
                   {'&Edit':[
                             {'undo':['Undo', 'normal', 'undo.png']},
                             {'redo':['Redo', 'normal', 'redo.png']},
                             {'editBook':['Edit a book info', 'normal', 'editBook.png']},
                             {'editBooks':['Edit a book info in bulk', 'normal', 'editBooks.png']}
                             ]
                    },
                   {'Preferences':[]
                    },
                   {'&View':[
                             {'statusBar':['Show status bar', 'check', 'statusBar.png']},
                             {'toolbar':['Show toolbar', 'check', 'toolbar.png']}
                             ]
                    },
                   {'&Help':[
                             {'aboutCalibre':['About Better Calibre', 'normal', 'aboutCalibre.png']}
                             ]
                    }
                   )
        
        i = 1
        j = 1
        for topLevel in topMenu:
            topLevelMenu = wx.Menu()  # Top level
            for k, topLevelItems in topLevel.iteritems():
                items = list()
                for topLevelItem in topLevelItems:
                    for child, childValue in topLevelItem.iteritems():
                        kind_value = None
                        if 'normal' == childValue[1]:
                            kind_value = wx.ITEM_NORMAL
                        elif 'radio' == childValue[1]:
                            kind_value = wx.ITEM_RADIO
                        elif 'check' == childValue[1]:
                            kind_value = wx.ITEM_CHECK
                        item = topLevelMenu.Append(i * 10 + j, childValue[0], childValue[0], kind=kind_value)
                        bmp = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_OTHER, (16, 16))
                        item.SetBitmap(bmp)
                        if 'check' == childValue[1]:
                            item.Check()
                        
                        items.append(item)
                    j = j + 1
                self.items.append(items)
#                 topLevelMenu.Append(-1,childMenu)
            menubar.Append(topLevelMenu, k)
            i = i + 1


        self.Bind(wx.EVT_MENU, self.OnQuit, id=13)
        self.Bind(wx.EVT_MENU, self.OnRestart, id=12)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.items[4][0])

        self.Bind(wx.EVT_MENU, self.OnAdd, self.items[0][0])
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.items[3][0])
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.items[3][1])

        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(1, '', wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16)))
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        # Creating Grid Panel
        self.mainBookPanel = wx.Panel(self.frmPanel)

        
        self.searchPanel = wx.Panel(self.frmPanel, id=11)
        # add a bitmap on the left side
        self.searchTextPanel = wx.Panel(self.searchPanel, style=wx.SUNKEN_BORDER)
        bmp = wx.ArtProvider_GetBitmap(wx.ART_FIND, wx.ART_OTHER, (16, 16))
        self.staticbmp = wx.StaticBitmap(self.searchTextPanel, -1, bmp, pos=(1, 0))
#         w, h = self.staticbmp.GetSize()
        self.searchText = wx.TextCtrl(self.searchTextPanel, id=100, style=wx.TE_PROCESS_ENTER | wx.NO_BORDER, value="", name=" Search: ", validator=SearchTextValidator())
        self.searchText.SetToolTipString('Search your book here.')
        self.hbox_searchText = wx.BoxSizer (wx.HORIZONTAL)
        self.hbox_searchText.Add(self.staticbmp, flag=wx.CENTER)
        self.hbox_searchText.Add(self.searchText, proportion=1, flag=wx.CENTER)
        
        self.vbox_searchText = wx.BoxSizer(wx.VERTICAL)
        self.vbox_searchText.Add(self.hbox_searchText, proportion=1, flag=wx.EXPAND)
        self.searchTextPanel.SetSizerAndFit(self.vbox_searchText)
        
        self.searchLabel = wx.StaticText(self.searchPanel, -1, label="Search")
        self.searchButton = wx.Button(self.searchPanel, label="search")
        self.hboxSearchPanel = wx.BoxSizer (wx.HORIZONTAL)
        self.hboxSearchPanel.Add(self.searchLabel, flag=wx.CENTER)
        self.hboxSearchPanel.Add(self.searchTextPanel, 1, flag=wx.CENTER)
        self.hboxSearchPanel.Add(self.searchButton, flag=wx.CENTER)
        self.vBoxSearchPanel = wx.BoxSizer(wx.VERTICAL)
        self.vBoxSearchPanel.Add(self.hboxSearchPanel, proportion=1, flag=wx.EXPAND)
        self.searchPanel.SetSizerAndFit(self.vBoxSearchPanel)
        
        self.searchText.SetFocus()
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.EvtText)
        
      
        self.mainBookTab = MainBookTab(self.mainBookPanel)
        vbox_noteBook = wx.BoxSizer(wx.VERTICAL)
        vbox_noteBook.Add(self.mainBookTab, 1, wx.ALL | wx.EXPAND, 5)
#         vbox_noteBook.Add(self.gridPanel, 1, wx.ALL|wx.EXPAND, 5)
        self.mainBookPanel.SetSizer(vbox_noteBook)
        
        # Add them to sizer.
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(self.searchPanel, .1, wx.EXPAND | wx.ALL, 1)
        vBox.Add(self.mainBookPanel, 9, wx.EXPAND | wx.ALL, 1)

        

        self.frmPanel.SetSizer(vBox)
        self.frmPanel.Layout()
        x, y = wx.DisplaySize()
        self.SetSize((x, y - 40))
        
        self.SetTitle('Better Calibre')
        self.Centre()
        self.Show(True)
     
    def gridActivity(self, bookName=None, books=None):
        print self.mainBookTab  
        self.grid = self.mainBookTab.tabOne.grid      
        print 'updating'
        
        print "1", self.grid.GetChildren()
        print "2", self.grid.GetCellValue(0, 0)
        self.grid.ForceRefresh()
        availableRows = self.grid.GetNumberRows()
        totalRows = len(books)
        self.grid.ClearGrid()
        self.grid.ForceRefresh()
        self.grid.ClearGrid
        if totalRows > availableRows :
            try:
                self.grid.AppendRows(totalRows - availableRows)
            except:
                print 'one'
                
        elif totalRows < availableRows:
            print 'one_1'
            try:
                self.grid.BeginBatch()
                self.grid.DeleteRows(0, availableRows - totalRows, True)
                self.grid.EndBatch()
            except:
                print 'exception one_1'
        else:
            print 'one_2_'
            self.grid.DeleteRows(0, availableRows, True)
            self.grid.AppendRows(totalRows)
        rowNum = 0
#         color = (100,100,255)
        color = 'light gray'
        attr = self.cellAttr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(color)
        print 'totalRows', totalRows
        print 'availableRows', availableRows
        
        for book in books:
            if rowNum % 2 == 0:
                for i in range(10):
                    self.grid.SetAttr(rowNum, i, attr)
            self.grid.SetCellValue(rowNum, 0, book.bookName)
            self.grid.SetCellValue(rowNum, 1, book.authors[0].authorName)
            self.grid.SetCellValue(rowNum, 2, book.publisher)
            self.grid.SetCellValue(rowNum, 3, book.isbn_13)
            if book.fileSize:
                self.grid.SetCellValue(rowNum, 4, book.fileSize)
            else:
                self.grid.SetCellValue(rowNum, 4, '0')
            self.grid.SetCellValue(rowNum, 5, book.bookFormat)
            self.grid.SetCellValue(rowNum, 6, book.bookPath)
            rowNum = rowNum + 1
    pass
       
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
        
    def OnAdd(self, event):
        """ 
        Browse for file
        
        """
        
        # This is how you pre-establish a file filter so that the dialog
        # only shows the extension(s) you want it to.
        wildcard = "PDF Book source (*.pdf)|*.pdf|" \
                    "TXT Book source (*.txt)|*.txt|"\
                    "All Book source (*.*)|*.*"
        
        dlg = wx.FileDialog(None, message="Choose a Python file", defaultDir=os.getcwd(),
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns the file that was selected
            path = dlg.GetPath()

            # Open the file as read-only and slurp its content
            fid = open(path, 'rt')
            text = fid.read()
            fid.close()

            # Create the notebook page as a wx.TextCtrl and
            # add it as a page of the wx.Notebook
            text_ctrl = wx.TextCtrl(self.notebook, style=wx.TE_MULTILINE)
            text_ctrl.SetValue(text)

            filename = os.path.split(os.path.splitext(path)[0])[1]
            self.notebook.AddPage(text_ctrl, filename, select=True)

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

        
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
   
        
        
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            return 
        
    def EvtText(self, event):
        global books
        engine = create_engine('sqlite:///calibre.sqlite', echo=True)
        session = sessionmaker()
        session.configure(bind=engine)
        bookName = event.GetString()
        self.books = CreateDatabase().findByBookName(session, bookName)
        books = self.books
        self.gridActivity(bookName, self.books)
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
    global books, frame
    session = CreateDatabase().creatingDatabase()
    CreateDatabase().addingData(session)
    books = CreateDatabase().findAllBook(session)
    bookName = 'A Peek at Computer Electronics'
    books = CreateDatabase().findByBookName(session, bookName)
    app = wx.App(0)
    frame = MainWindow(None, "My Calibre")
    app.MainLoop()    


if __name__ == '__main__':
    main()
    
