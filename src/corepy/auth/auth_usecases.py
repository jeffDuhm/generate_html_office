from corepy.auth.auth_schemas import TokenSchema
from corepy.auth.auth_tokens import create_access_token
from corepy.user.user_schemas import UserAuthSchema
from corepy.user.user_usecases import UserUsecases

class AuthUsecases:
    
    def login(self, credentials: UserAuthSchema) -> TokenSchema:
        db_user = UserUsecases().authenticate(credentials)
        token = create_access_token(db_user.id)
        return TokenSchema(access_token=token)