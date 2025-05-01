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
    
    
    async def ainit(self):
        '''
        Initialize the user data
        '''
        
        # Get user data from the database
        self.user_data = await self.db.get_user_data(user_id=self.user_id)