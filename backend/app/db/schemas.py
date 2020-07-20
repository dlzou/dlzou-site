from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from re import sub


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return sub(r'(?!^)([A-Z]+)', r'_\1', cls.__name__).lower()


article_to_tag = Table('article_to_tag', Base.metadata,
                       Column('article_id', String, ForeignKey('article.id_')),
                       Column('tag_id', String, ForeignKey('tag.id_')))


class Article(Base):
    id_ = Column(String, primary_key=True)
    slug = Column(Text)
    title = Column(Text)
    description = Column(Text)
    body = Column(Text)
    author = Column(String)
    time_posted = Column(DateTime)
    time_updated = Column(DateTime)
    views = Column(Integer)
    tags = relationship('Tag', secondary=article_to_tag)


class Tag(Base):
    id_ = Column(String, primary_key=True)
    label = Column(String)
    count = Column(Integer)
