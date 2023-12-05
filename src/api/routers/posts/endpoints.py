from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.posts.models import PostAdd, PostResponse, PostsListResponse
from src.api.security import access_policy
from src.api.sessions import get_db_session
from src.db.crud import get_posts, get_post_by_id, add_post_with_images

router = APIRouter(
    prefix='/post',
    tags=["posts"],
    dependencies=[Depends(access_policy)]
)


@router.get("/latests", response_model=PostsListResponse)
async def get_posts_list(session: AsyncSession = Depends(get_db_session), page: int = Query(1, ge=1),
                         per_page: int = Query(100, ge=0)):
    limit = per_page * page
    offset = (page - 1) * per_page
    res = await get_posts(session, limit, offset)
    return res


@router.get("/{id:int}", response_model=PostResponse)
async def get_post(id: int, session: AsyncSession = Depends(get_db_session)):
    res = await get_post_by_id(session, id)
    return res


@router.post("/add", response_model=PostResponse)
async def add_post(post: PostAdd, session: AsyncSession = Depends(get_db_session), credentials=Depends(access_policy)):
    if not post.images:
        res = await add_post_with_images(session, credentials.subject['id'], post.title, post.text)
    else:
        res = await add_post_with_images(session, credentials.subject['id'], post.title, post.text, post.images)
    return res
