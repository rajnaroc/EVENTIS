import os
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","b47c300f604a119bbafd524c8a5e8e47")


class ProductConfig(Config):
    DEBUG=False
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_DB=os.getenv("MYSQL_DB")
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")
    

class DevelopConfig(Config):
    DEBUG=True
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_DB=os.getenv("MYSQL_DB")
    JWT_SECRET = os.getenv("JWT_SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")

config = {
    "dev" : DevelopConfig,
    "produ" : ProductConfig
}