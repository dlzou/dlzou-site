from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, Text, DateTime, event
from sqlalchemy.orm import Session, object_session, relationship, attributes
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func, select
from re import sub


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return sub(r'(?!^)([A-Z]+)', r'_\1', cls.__name__).lower()


class Article(Base):
    id_ = Column(Integer, primary_key=True, nullable=False)
    title = Column(Text, unique=True, nullable=False)
    author = Column(String, nullable=False)
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
    label = Column(String, unique=True, nullable=False)

    # shook down @van for these
    @hybrid_property
    def count(self):
        return object_session(self).query(ArticleToTag).with_parent(self).count()

    @count.expression
    def _count_exp(cls):
        q = select([func.count(ArticleToTag.tag_id)]) \
            .where(ArticleToTag.tag_id == cls.id_) \
            .label('count')
        return q


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


class Admin(Base):
    email = Column(String, primary_key=True, nullable=False)
    password_hash = Column(String, nullable=False)
