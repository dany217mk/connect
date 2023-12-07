import os
def required_env(name):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"Environment variable {name} is required")
    return value
DB_HOST = required_env("DB_HOST")
DB_USER = required_env("DB_USER")
DB_PASSWORD = required_env("DB_PASSWORD")
DB_NAME = required_env("DB_NAME")


DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
JWT_SECRET_KEY = required_env("JWT_SECRET_KEY")
JWT_EXPIRE_HOURS = 24 * 30 # 30 days

# DB_HOST = "localhost"
# DB_PORT = "5432"
# DB_USER = "postgres"
# DB_PAS = "12345"
# DB_NAME = "connect"
#     # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PAS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"