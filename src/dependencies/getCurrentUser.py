import os
from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import authenticate_request, AuthenticateRequestOptions
from src.config import CLERK_SECRET_KEY, CLERK_AUTHROIZ_DOMAIN

security = HTTPBearer()

async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)
    try:
        request_state = authenticate_request(
            sdk,
            request,
            options=AuthenticateRequestOptions(
                authorized_parties=str(CLERK_AUTHROIZ_DOMAIN).split(",")
            ),
        )
        user_id = request_state.payload.get("sub")
        if not request_state.is_signed_in or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return user_id
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Authentication Error: ", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")