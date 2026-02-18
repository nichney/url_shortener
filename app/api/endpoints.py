from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.api.schemas import CreateAliasIn, CreateAliasResponse, ErrorResponse
from app.repositories.link_repo import LinkRepository
from app.dependencies import get_link_repo

from app.logic.link_generator import generate_new_short_link


router = APIRouter()


@router.get(
    "/{alias_url}",
    response_class=RedirectResponse,
    status_code=302
    )
async def redirect_from_alias_to_url(alias_url: str, repo: LinkRepository = Depends(get_link_repo)):
    original_url = await repo.get_url_by_alias(alias_url)
    if not original_url:
        raise HTTPException(status_code=404, detail="Alias not found")

    # TODO: cache

    return RedirectResponse(url=original_url)


@router.post(
    "/create",
    response_model=CreateAliasResponse
    )
async def create_short_link(payload: CreateAliasIn, repo: LinkRepository = Depends(get_link_repo)):
    alias = await generate_new_short_link(repo, payload.url, payload.custom_alias)
    return CreateAliasResponse(url=payload.url, alias=alias)
