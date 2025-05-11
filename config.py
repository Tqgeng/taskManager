from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

class AuthJWT(BaseSettings):
    algorithm: str = 'RS256'
    private_key_path: Path = BASE_DIR / 'cert' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'cert' / 'jwt-public.pem'
    access_token_expire_minutes: int = 3

class Settings(BaseSettings):

    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()

print(f"BASE_DIR: {BASE_DIR}")
