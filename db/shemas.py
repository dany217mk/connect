from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
import datetime


created = Annotated[datetime.datetime, mapped_column(server_default=text("now()"))]
modified = Annotated[datetime.datetime, mapped_column(
        server_default=text("now()"),
        onupdate=datetime.datetime.now
    )]
is_deleted = Annotated[int, mapped_column(
    server_default=text("0")
)]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str | None] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    img_url: Mapped[str | None]
    about: Mapped[str | None]
    created: Mapped[created]
    modified: Mapped[modified]
    is_deleted: Mapped[is_deleted]
    post: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    like: Mapped[list["Like"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    comment: Mapped[list["Comment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"User(id={self.id!r}, login={self.login!r}, post={self.post!r}, like={self.like!r}, comment={self.comment!r})"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column(String(256))
    text: Mapped[str | None]
    created: Mapped[created]
    modified: Mapped[modified]
    is_deleted: Mapped[is_deleted]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="post")
    post_image: Mapped[list["PostImage"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )
    like: Mapped[list["Like"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )
    comment: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, text={self.text!r}, post_image={self.post_image!r})"


class PostImage(Base):
    __tablename__ = "post_image"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    ratio: Mapped[str | None]
    created: Mapped[created]
    modified: Mapped[modified]
    is_deleted: Mapped[is_deleted]
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="post_image")

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"PostImage(id={self.id!r}, url={self.url!r}, ratio={self.ratio!r})"


class Like(Base):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="like")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="like")
    created: Mapped[created]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"Post(id={self.id!r}, user_id={self.user_id!r}, post_id={self.post_id!r})"


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(4096), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comment")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="comment")
    created: Mapped[created]
    modified: Mapped[modified]
    is_deleted: Mapped[is_deleted]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return f"Comment(id={self.id!r}, user_id={self.user_id!r}, post_id={self.post_id!r}, text={self.text!r})"