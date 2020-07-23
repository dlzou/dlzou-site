from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text, DateTime, event
from sqlalchemy.orm import Session, relationship, attributes
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from re import sub


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return sub(r'(?!^)([A-Z]+)', r'_\1', cls.__name__).lower()


class Article(Base):
    id_ = Column(Integer, primary_key=True, nullable=False)
    title = Column(Text, nullable=False)
    author = Column(String)
    description = Column(Text)
    body = Column(Text, nullable=False)
    time_created = Column(DateTime, nullable=False)
    time_updated = Column(DateTime)
    views = Column(Integer)
    tags = relationship('Tag',
                        secondary='article_to_tag',
                        back_populates='articles')


class Tag(Base):
    id_ = Column(Integer, primary_key=True, nullable=False)
    label = Column(String, nullable=False)
    count = Column(Integer)


class ArticleToTag(Base):
    article_id = Column(Integer, ForeignKey('article.id_'))
    tag_id = Column(Integer, ForeignKey('tag.id_'))
    articles = relationship('Article', secondary='article_to_tag')


# shamelessly stolen from @zzzeek
@event.listens_for(Session, 'after_flush')
def delete_tag_orphans(db: Session, ctx) -> None:
    # optional: look through Session state to see if we want to emit a DELETE for orphan Tags
    flag = False

    for instance in db.dirty:
        if isinstance(instance, Article) and \
                attributes.get_history(instance, 'tags').deleted:
            flag = True
            break
    for instance in db.deleted:
        if isinstance(instance, Article):
            flag = True
            break

    # emit a DELETE for all orphan Tags. This is safe to emit regardless of "flag", if a less
    # verbose approach is desired.
    if flag:
        db.query(Tag).filter(~Tag.entries.any()).delete(synchronize_session=False)
