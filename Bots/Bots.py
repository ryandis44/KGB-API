'''

User class

'''


from Database.MySQL import AsyncDatabase
db = AsyncDatabase(__file__)



class Bot:
    
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.access_list: list[dict] = []
    
    
    
    async def ainit(self):
        
        # await self.__fetch_bot_data()
        await self.__fetch_bot_access_list()
    
    
    
    async def __fetch_bot_data(self):
        '''
        Fetch the bot data from the database
        '''
        
        cols = [
            "id"
        ]
        _ = await db.execute(
            f"SELECT * FROM `BOTS` WHERE `id`='{self.bot_id}'",
        )
    
    
    
    async def __fetch_bot_access_list(self):
        '''
        Fetch the bot access list from the database
        '''
        
        __ = {}
        
        
        # First get users with global roles
        users_with_global_roles = await db.execute(
            "SELECT `user_id`, `global_role` FROM `USERS` WHERE "
            "`global_role` IS NOT NULL",
        )
        # ...then add them to the temp access list
        for row in users_with_global_roles:
            __[row[0]] = row[1]
        
        
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
            
            if not __.get(user_id): __[user_id] = role
        
        
        # Finally, convert the temp access list to a list of dicts
        # and assign it to the access list
        self.access_list = [
            {
                "user_id": user_id,
                "role": role
            }
            for user_id, role in __.items()
        ]