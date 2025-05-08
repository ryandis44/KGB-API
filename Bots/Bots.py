'''

User class

'''


from Database.MySQL import AsyncDatabase
from fastapi import HTTPException
db = AsyncDatabase(__file__)



class Bot:
    
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.access_list: dict = {}
    
    
    
    async def ainit(self):
        
        await self.__fetch_bot_data()
        await self.__fetch_bot_access_list()
    
    
    
    async def __fetch_bot_data(self):
        '''
        Fetch the bot data from the database
        
        TODO wishlist safety picks
        '''
        
        cols = [
            "id"
        ]
        _ = await db.execute(
            f"SELECT * FROM `BOTS` WHERE `bot_id`='{self.bot_id}'",
        )
        
        if _ in [None, []]: raise HTTPException(status_code=404, detail=f"Error: Bot with ID '{self.bot_id}' not found.")
    
    
    
    async def __fetch_bot_access_list(self):
        '''
        Fetch the bot access list from the database
        '''
        
        # First get users with global roles
        users_with_global_roles = await db.execute(
            "SELECT `user_id`, `global_role` FROM `USERS` WHERE "
            "`global_role` IS NOT NULL",
        )
        # ...then add them to the temp access list
        for row in users_with_global_roles:
            self.access_list[row[0]] = row[1]
        
        
        # Then get users with bot-specific roles
        users_with_bot_specific_roles = await db.execute(
            f"SELECT `user_id`, `role` FROM `BOT_ACCESS_LISTS` "
            f"WHERE `bot_id`='{self.bot_id}'",
        )
        
        
        # ...and add them to the temp access list but only
        # if they don't already exist in the temp access list
        # (i.e. if they don't have a global role)
        for row in users_with_bot_specific_roles:
            user_id = row[0]
            role = row[1]
            
            if not self.access_list.get(user_id): self.access_list[user_id] = role