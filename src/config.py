import os
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY")


class ProductConfig(Config):
    DEBUG=False
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_DB=os.getenv("MYSQL_DB")
    EMAIL_USER=os.getenv("EMAIL_USER")
    EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
    EMAIL_HOST=os.getenv("EMAIL_HOST")
    EMAIL_PORT=os.getenv("EMAIL_PORT")

class DevelopConfig(Config):
    DEBUG=True
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_DB=os.getenv("MYSQL_DB")
    EMAIL_USER=os.getenv("EMAIL_USER")
    EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
    EMAIL_HOST=os.getenv("EMAIL_HOST")
    EMAIL_PORT=os.getenv("EMAIL_PORT")
config = {
    "dev" : DevelopConfig,
    "produ" : ProductConfig
}