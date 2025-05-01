'''

API for the KGB bot project

'''


import logging # logger
import os # environment variables, file paths, et al.

from contextlib import asynccontextmanager
from Database.MySQL import check_pool, conn_check # establish database connection
from Database.tunables import tunables_init # tunables initialization
# from Database.tunables import tunables_init # tunables initialization
from dotenv import load_dotenv # load environment variables from .env file
from fastapi import FastAPI, Depends, HTTPException # API
from fastapi.middleware.cors import CORSMiddleware

# v1
from routers.v1 import v1

LOGGER = logging.getLogger()



# Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    conn_check()
    tunables_init()
    await check_pool()
    yield # Code after yield is executed on shutdown
    pass



###########################################################################################################################



'''
Set up logger and load variables
'''

log_level = os.getenv('LOG_LEVEL', 20)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.WARNING if log_level is None else int(log_level)) # default log level is WARNING
handler = logging.FileHandler(filename='log.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)s: %(message)s'))
LOGGER.addHandler(handler)

# tunables_init()
load_dotenv() # load environment variables from .env file



###########################################################################################################################



# FastAPI instance and routing
app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "docExpansion": "none",
    },
    title=f"KGB API",
    version="1.0-BETA"
)

# v1
app.include_router(v1)

# Kubernetes Integration
# app.include_router(healthz)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH"],
    allow_headers=["*"],
)