class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_admin.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
