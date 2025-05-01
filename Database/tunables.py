'''
This file is responsible for handling tunables, which are variables that can be changed without needing to restart the bot
These tunables are stored in a database table, and are loaded into memory when the bot starts up
The tunables can be refreshed at any time, and the bot will automatically update the values in memory
The tunables are used to configure the bot's behavior, and can be used to enable or disable certain features
The tunables are also used to store information about guild profiles, which are used to configure the bot's behavior on a per-guild basis
The tunables are stored in a dictionary, with the variable name as the key, and the value as the value
'''



import logging

from Database.MySQL import Database, AsyncDatabase
from json import loads
db = AsyncDatabase(__file__)
LOGGER = logging.getLogger()

TUNABLES = {}
def tunables(s):
    try: return TUNABLES[s]
    except Exception as e:
        LOGGER.error(f"TUNABLES ERROR: Could not find '{s}' | {e}")
        return None

def all_tunable_keys() -> list: return [*TUNABLES]

def tunables_init(): # Initial call cannot be async
    assign_tunables(
        val=Database("TUNABLES INITIALIZATION").db_executor(
            "SELECT * FROM TUNABLES "
            "ORDER BY variable ASC"
        )
    )

async def tunables_refresh():
    assign_tunables(await db.execute(
        "SELECT * FROM TUNABLES "
        "ORDER BY variable ASC"
    ))

def assign_tunables(val):
    global TUNABLES
    TUNABLES = {}
    for tunable in val:
        try:
            if tunable[1] == "TRUE": TUNABLES[tunable[0]] = True # Assign boolean values
            if tunable[1] == "FALSE": TUNABLES[tunable[0]] = False # Assign boolean values
            if tunable[1][0:2] == "0x": TUNABLES[tunable[0]] = int(tunable[1], 16) # Assign hex values
            elif tunable[1] not in ["TRUE", "FALSE"]:
                if tunable[1] is not None and tunable[1].isdigit(): TUNABLES[tunable[0]] = int(tunable[1]) # Assign int values if possible
                else: TUNABLES[tunable[0]] = tunable[1] # Assign value as-is (string)
        except Exception as e: LOGGER.error(f"TUNABLES ERROR: (({e})) Could not ASSIGN: {tunable}")
    configure_tunables()

def configure_tunables() -> None: pass # Placeholder for future use