'''

User class

'''


from Database.MySQL import AsyncDatabase
db = AsyncDatabase(__file__)



class User:
    '''
    User class
    '''
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.access_list: list[dict] = []
    
    
    async def ainit(self):
        
        # await self.__fetch_user_data()
        await self.__fetch_global_roles()
        await self.__fetch_user_access_list()
    
    
    
    async def __fetch_user_data(self):
        '''
        Fetch the user data from the database
        '''
        
        cols = [
            "id"
        ]
        _ = await db.execute(
            f"SELECT * FROM `USERS` WHERE `id`='{self.user_id}'",
        )
    
    
    
    async def __fetch_global_roles(self) -> None:
        '''
        Fetch the global roles from the database
        '''
        
        _ = await db.execute(
            "SELECT `bot_id`, `global_role` FROM `USERS` WHERE "
            f"`global_role` IS NOT NULL AND `user_id`='{self.user_id}'",
        )
        
        for row in _:
            self.access_list.append({
                "bot_id": row[0],
                "role": row[1]
            })
    
    
    
    async def __fetch_user_access_list(self) -> None:
        '''
        Fetch the user access list from the database
        '''
        
        _ = await db.execute(
            "SELECT `bot_id`, `role` FROM `BOT_ACCESS_LISTS` WHERE "
            f"`user_id`='{self.user_id}'",
        )
        
        for row in _:
            self.access_list.append({
                "bot_id": row[0],
                "role": row[1],
            })