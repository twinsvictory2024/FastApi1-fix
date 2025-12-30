from models import ORM_CLS, ORM_OBJ

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException


async def get_ad_by_id( session: AsyncSession, orm_cls: ORM_CLS, ad_id: int ) -> ORM_OBJ:
    orm_obj = await session.get( orm_cls, ad_id )
    if orm_obj is None:
        raise HTTPException( 404, "Advertisement not found" )
    return orm_obj

async def search_ad( session: AsyncSession, orm_cls: ORM_CLS, queryparams: dict | None = None) -> list[ORM_OBJ]:
    query = select(orm_cls)
    limit: int = 100
    offset: int = 0

    if queryparams:
        conditions = []
        if "title" in queryparams:
            conditions.append( orm_cls.title.ilike( f"%{ queryparams['title'] }" ) )
        if "description" in queryparams:
            conditions.append( orm_cls.description.ilike( f"%{ queryparams['description'] }" ) )
        if "author" in queryparams:
            conditions.append( orm_cls.author.ilike( f"%{ queryparams['author'] }" ) )
        if "price" in queryparams:
            conditions.append( orm_cls.price == queryparams['price'] )
        if "limit" in queryparams:
            limit = queryparams['limit']
        if "offset" in queryparams:
            limit = queryparams['offset']

        if conditions:
            query = query.where( and_( *conditions ) ).limit(limit).offset(offset)

    result = await session.execute(query)
    return result.scalars().all()

async def create_ad( session: AsyncSession, ad_item: ORM_OBJ ):
    # try:
        session.add( ad_item )
        await session.commit()
        return ad_item
    # except IntegrityError:
        # raise HTTPException( 409, "Advertisement already exist" )

async def update_ad( session: AsyncSession, orm_cls: ORM_CLS, ad_id: int, updated_item: dict ):
    ad = await session.get( orm_cls, ad_id )
    if not ad:
        raise HTTPException( 404, "Advertisement not found" )

    for key, value in updated_item:
        if value is not None:
            setattr( ad, key, value )
 
    await session.commit()
    return ad



async def delete_ad( session: AsyncSession, orm_cls: ORM_CLS, ad_id: int):
    ad = await session.get( orm_cls, ad_id )
    if not ad:
        raise HTTPException( 404, "Advertisement not found" )
    
    await session.delete(ad)
    await session.commit()
    return {"deleted_id": ad_id}

