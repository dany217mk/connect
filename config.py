DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PAS = "koval2107"
DB_NAME = "connect"
SQLALCHEMY_ECHO = True


def DATABASE_URL_asyncpg():
    return f"postgresql+asyncpg://{DB_USER}:{DB_PAS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"