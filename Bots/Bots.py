'''

User class

'''


from Database.MySQL import AsyncDatabase
db = AsyncDatabase(__file__)



class Bot:
    
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
    
    
    
    async def ainit(self):
        
        await self.__fetch_bot_data()
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
        
        cols = [
            "id"
        ]
        _ = await db.execute(
            f"SELECT * FROM `BOT_ACCESS_LISTS` WHERE `id`='{self.bot_id}'",
        )