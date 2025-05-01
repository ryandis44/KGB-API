import os

# :: Authentication ::
from Database.tunables import tunables
from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from keycloak import KeycloakOpenID, KeycloakAdmin
from dotenv import load_dotenv
load_dotenv()



v1_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    description="Keycloak token for authentication"
)



# :: Check API Token ::
# This function checks the API token against the environment variable
# and rejects the request if the token is invalid.
def v1_check_api_token(api_token: str = Header(..., description="API token required on all queries")) -> bool:
    if api_token != os.getenv('API_TOKEN'):
        raise HTTPException(status_code=403, detail="Error: Invalid API Token")
    return True