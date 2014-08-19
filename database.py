from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import os

 
 
Base = declarative_base()
 
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    bookName = Column(String)# Title
    isbn_10 = Column(String)# Title
    isbn_13 = Column(String)# Title
    series = Column(String)# Title
    dimension = Column(String)# Title
    customerReview = Column(String)# Title
    bookDescription = Column(String)# Title
    editionNo = Column(String)# Title
    publisher = Column(String)# Title
    format = Column(String)# Title
    fileSize = Column(String)# Title
    numberOfPages = Column(String)# Title
    inLanguage = Column(String)# Title
    published_on = Column(DateTime, default=func.now())
    authors = relationship(
        'Author',
        secondary='author_book_link'
    )
 
 
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    authorName = Column(String)
    aboutAuthor = Column(String)
    
    books = relationship(
        Book,
        secondary='author_book_link'
    )
 
 
class AuthorBookLink(Base):
    __tablename__ = 'author_book_link'
    authorId = Column(Integer, ForeignKey('author.id'), primary_key=True)
    bookId = Column(Integer, ForeignKey('book.id'), primary_key=True)
    extra_data = Column(String(256))
    author = relationship(Author, backref=backref("book_assoc"))
    book = relationship(Book, backref=backref("dauthor_assoc"))

    
engine = create_engine('sqlite:///calibre.sqlite')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
