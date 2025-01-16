import os
from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import authenticate_request, AuthenticateRequestOptions
from src.config import CLERK_SECRET_KEY, CLERK_AUTHORIZED_DOMAIN

security = HTTPBearer()

async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:

        clent = Clerk(bearer_auth="sk_test_4udgHjcN8C2sn1woLPRtqgtXWavWXjI0UtBKlXEFkT")
        request_state = authenticate_request(
            clent,
            request,
            options=AuthenticateRequestOptions(
                authorized_parties= CLERK_AUTHORIZED_DOMAIN.split(",") if CLERK_AUTHORIZED_DOMAIN else []
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
