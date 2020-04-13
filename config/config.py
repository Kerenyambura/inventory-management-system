import secrets
class Config():
    DEBUG= True
    SECRET_KEY = 'secrets.token_hex(16)'

class Development(Config):
    # database://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Goodmand254@localhost:5432/inventory_management_system'

class Production(Config):
    pass

