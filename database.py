from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import os
from sqlalchemy.sql.schema import MetaData, UniqueConstraint
from sqlalchemy.sql import schema

 
 
Base = declarative_base()


class Book(Base):
    """A Book class is an entity having database table."""
    
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bookName = Column('book_name',String(46), nullable=False)  # Title
    isbn_10 = Column(String)  # Title
    isbn_13 = Column(String)  # Title
    series = Column(String)  # Title
    dimension = Column(String)  # Title
    customerReview = Column('customer_review',String)  # Title
    bookDescription = Column('book_description',String)  # Title
    editionNo = Column('edition_no',String)  # Title
    publisher = Column(String)  # Title
    format = Column(String)  # Title
    fileSize = Column('file_size',String)  # Title
    numberOfPages = Column('number_of_pages',String)  # Title
    inLanguage = Column('in_language',String)  # Title
    publishedOn = Column('published_on',DateTime, default=func.now())
    hasCover = Column('has_cover',String)  # Title
    bookPath = Column('book_path',String)  # Title
    rating = Column(String)  # Title
    uuid = Column('rating',String)  # Title
    createdOn = Column('created_on',DateTime, default=func.now())
    authors = relationship(
        'Author',
        secondary='author_book_link'
    )
 
 
class Author(Base):
    """A Author class is an entity having database table."""
    
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    authorName = Column('author_name',String(46), nullable=False, autoincrement=True)
    aboutAuthor = Column('about_author',String)
    email = Column(String, unique=True)
    created_on = Column(DateTime, default=func.now())
    
    books = relationship(
        Book,
        secondary='author_book_link'
    )
 
 
class AuthorBookLink(Base):
    """A AuthorBookLink class is an entity having database table. This class is for many to many association between Author and Book."""
    
    __tablename__ = 'author_book_link'
    id=Column(Integer, primary_key=True)
    authorId = Column('book_id',Integer, ForeignKey('author.id'))
    bookId = Column('author_id',Integer, ForeignKey('book.id'))
    extra_data = Column(String(256))
    author = relationship(Author, backref=backref("book_assoc"))
    book = relationship(Book, backref=backref("dauthor_assoc"))

    
engine = create_engine('sqlite:///calibre.sqlite', echo=True)
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
metadata = Base.metadata
for t in metadata.sorted_tables:
    print t.name
