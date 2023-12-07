from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete, func, Select, text
from sqlalchemy.orm import selectinload, joinedload

from src.db.schemas import User, Post, PostImage, Like, Comment, ProfileImage

async def paginate(session: AsyncSession, query: Select, limit: int, offset: int) -> dict:
    return {
        'count': await session.scalar(select(func.count()).select_from(query.subquery())),
        'items': [record for record in await session.scalars(query.limit(limit).offset(offset))]
    }


# users:
async def add_user(session: AsyncSession,login: str, name: str, password: str) -> User:
    user = User(login=login, name=name, password=password)
    session.add(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession, id: int, name: str | None = None,
                      about: str | None = None, img_url: str | None = None) -> User:
    user = await session.get(User, id)
    if name is not None:
        user.name = name
    if about is not None:
        user.about = about
    if img_url is not None:
        profileImage = ProfileImage(user_id=id, img_url=img_url)
        session.add(profileImage)
    await session.commit()
    return user


async def get_users(session: AsyncSession, limit, offset):
    stmt = select(User).where(User.is_deleted == 0)
    res = await paginate(session, stmt, limit, offset)
    return res


async def get_user_by_id(session: AsyncSession, id: int):
    stmt = select(User).where(User.id == id).options(
        selectinload(User.profile_image)
    )
    user = await session.scalar(stmt)
    return user


async def get_user_by_login(session: AsyncSession, login: str):
    stmt = select(User).where(User.login == login)
    user = await session.scalar(stmt)
    return user


# posts:
async def add_post(session: AsyncSession, user: User, title: str = "", text: str = ""):
    user.post += [Post(title=title, text=text)]
    await session.commit()
    return user.post




async def get_post_by_id(session: AsyncSession, id: int):
    stmt = select(Post).where(Post.id == id).options(
        selectinload(Post.like),
        selectinload(Post.comment),
    )
    post = await session.scalar(stmt)
    return post


async def get_posts_in_days(session: AsyncSession, day_limit: int):
    stmt = select(Post).where(Post.is_deleted == 0, Post.modified_time >= text("NOW() - INTERVAL '7 DAY'")).options(
        joinedload(Post.user),
        selectinload(Post.like),
        selectinload(Post.comment),
    ).order_by(Post.created_time.desc())
    res = [record for record in await session.scalars(stmt)]
    return res

async def get_posts(session: AsyncSession, limit, offset):
    stmt = select(Post).where(Post.is_deleted == 0).options(
        joinedload(Post.user),
        selectinload(Post.like),
        selectinload(Post.comment),
    ).order_by(Post.created_time.desc())
    res = await paginate(session, stmt, limit, offset)
    return res


async def delete_post(session: AsyncSession, id: int):
    post = await session.get(Post, id)
    stmt = update(PostImage).where(PostImage.post_id == id).values(is_deleted=1)
    await session.execute(stmt)
    stmt = update(Comment).where(Comment.post_id == id).values(is_deleted=1)
    await session.execute(stmt)
    post.is_deleted = 1
    await session.commit()


# likes
async def set_like(session: AsyncSession, user_id: int, post_id: int):
    like = Like(
        user_id=user_id,
        post_id=post_id,
    )
    session.add(like)
    await session.commit()


async def delete_like(session: AsyncSession, user_id: int, post_id: int):
    stmt = delete(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    await session.execute(stmt)
    await session.commit()


async def get_count_likes(session: AsyncSession,  post_id: int):
    count = await session.scalar(select(func.count())
                                 .select_from(select(Like).where(Like.post_id == post_id).subquery()))
    return count


# comments:
async def get_comments(session: AsyncSession, post_id, limit, offset):
    stmt = select(Comment).where(Comment.post_id == post_id, Comment.is_deleted == 0)
    res = await paginate(session, stmt, limit, offset)
    return res


async def get_count_comments(session: AsyncSession,  post_id: int):
    count = await session.scalar(select(func.count()).select_from(select(Comment).where(Comment.post_id == post_id, Comment.is_deleted == 0).subquery()))
    return count


async def add_comment(session: AsyncSession, user_id: int, post_id: int, text: str):
    comment = Comment(
        user_id=user_id,
        post_id=post_id,
        text=text
    )
    session.add(comment)
    await session.commit()


async def get_comment_by_id(session: AsyncSession, id: int):
    stmt = select(Comment).where(Comment.id == id)
    comment = await session.scalar(stmt)
    return comment


async def update_comment(session: AsyncSession, comment_id: int, text: str | None = None):
    comment = await session.get(Comment, comment_id)
    comment.text = text
    if text is not None:
        comment.text = text
    await session.commit()


async def delete_comment(session: AsyncSession, comment_id: int):
    comment = await session.get(Comment, comment_id)
    comment.is_deleted = 1
    await session.commit()
