'''
Users v1 endpoint
'''



import logging

from Bots.Bots import Bot # Bot class
from Database.MySQL import AsyncDatabase # Database connection
from fastapi import APIRouter, HTTPException, Depends, Header
from Users.User import User # User class

v1 = APIRouter(
    prefix="/v1",
    # tags=["v1"]
)

db = AsyncDatabase(__file__)
LOGGER = logging.getLogger()



###########################################################################################################################



'''
Users
'''



@v1.get(
    path="/users/{user_id}",
    summary="Request user data",
    name="Users Object Endpoint",
    tags=["Users"]
)
async def get_bot(
    
    # User ID
    user_id: int,

    # Auth
    api_token: bool = Depends(v1_check_api_token)

) -> dict:
    
    '''
    
    To retrieve user data, the user must be authenticated.
    To authenticate, the user must provide:
    api-token':          a valid API token (Bearer token) in the request header.
    
    '''
    
    user = User(user_id=user_id)
    await user.ainit()
    
    response = {
        "id": None,
    }
    
    return response



###########################################################################################################################



'''
Users
'''



@v1.get(
    path="/bots/{bot_id}",
    summary="Request bot data",
    name="Bots Object Endpoint",
    tags=["Bots"]
)
async def get_bot(
    
    # Bot ID
    bot_id: int,

    # Auth
    api_token: bool = Depends(v1_check_api_token)
    
) -> dict:
    
    '''
    
    To retrieve user data, the user must be authenticated.
    To authenticate, the user must provide:
        - 'api-token':          a valid API token (Bearer token) in the request header.
    
    '''
    
    bot = Bot(bot_id=bot_id)
    await bot.ainit()
    
    response = {
        "bot_id": bot.bot_id,
        "access_list": bot.access_list
    }
    
    return response