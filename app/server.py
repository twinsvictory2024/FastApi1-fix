from fastapi import FastAPI, Query
from typing import Annotated

from lifespan import lifespan
from dependency import SessionDependency

from schema import AdCreate, AdResponse, AdUpdate
from models import AdsBase



import crud

app = FastAPI(
    title="FastAPI_Homework_1",
    description="Part 1 of FastAPI homework",
    lifespan=lifespan
)

@app.post('/advertisement', response_model=AdResponse)
async def create_adv( session: SessionDependency, ad_item: AdCreate ):
    ad = AdsBase(
        title = ad_item.title,
        description = ad_item.description,
        price = ad_item.price,
        author = ad_item.author,
    )
    resp_ad = await crud.create_ad( session, ad )
    return resp_ad

@app.get('/advertisement/{ad_id}', response_model=AdResponse)
async def get_ad( session: SessionDependency, ad_id: int ):
    ad = await crud.get_ad_by_id( session, AdsBase, ad_id )
    return ad


@app.get('/advertisement/', response_model= list[ AdResponse ] )
async def search_adv( session: SessionDependency, 
                    title:  str | None = None,
                    description:  str | None = None,
                    price:  float | None = None,
                    author: str | None = None,
                    limit: int = 100,
                    offset: int = 0
                    ):
    search_params = {}
    if title:
        search_params["title"] = title
    if description:
        search_params["description"] = description
    if price:
        search_params["price"] = price
    if author:
        search_params["author"] = author
    if limit:
        search_params["limit"] = limit
    if offset:
        search_params["offset"] = offset


    ads = await crud.search_ad( session, AdsBase, search_params )
    return ads

@app.patch('/advertisement/{ad_id}', response_model=AdResponse)
async def update_adv( session: SessionDependency, ad_id: int, update_item: AdUpdate):
    ad = await crud.update_ad( session, AdsBase, ad_id, update_item )
    return ad

@app.delete('/advertisement/{ad_id}')
async def delete_adv( session: SessionDependency, ad_id: int ):
    msg = await crud.delete_ad( session, AdsBase, ad_id )
    return msg
