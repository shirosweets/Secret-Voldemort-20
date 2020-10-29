from fastapi import FastAPI, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    username: str = Field(...,min_length=1)
    password: str = Field(...,min_length=1)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.post('/login',status_code=200)
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != 'test' or user.password != 'test':
        raise HTTPException(status_code=401,detail='Bad username or password')

    # identity must be between string or integer
    access_token = Authorize.create_access_token(identity=user.username)
    return {"access_token": access_token}

@app.get('/protected',status_code=200)
def protected(Authorize: AuthJWT = Depends()):
    # Protect an endpoint with jwt_required, which requires a valid access token
    # in the request to access.
    Authorize.jwt_required()

    # Access the identity of the current user with get_jwt_identity
    current_user = Authorize.get_jwt_identity()
    return {"logged_in_as": current_user}

# Returns the JTI (unique identifier) of an encoded JWT
@app.get('/get-jti',status_code=200)
def get_jti(Authorize: AuthJWT = Depends()):
    access_token = Authorize.create_access_token(identity='test')
    return Authorize.get_jti(encoded_token=access_token)

# this will return the identity of the JWT that is accessing this endpoint.
# If no JWT is present, `None` is returned instead.
@app.get('/get-jwt-identity',status_code=200)
def get_jwt_identity(Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()

    current_user = Authorize.get_jwt_identity()
    return {"logged_in_as": current_user}

# this will return the python dictionary which has all
# of the claims of the JWT that is accessing the endpoint.
# If no JWT is currently present, return None instead
@app.get('/get-raw-jwt',status_code=200)
def get_raw_jwt(Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()

    token = Authorize.get_raw_jwt()
    return {"token": token}