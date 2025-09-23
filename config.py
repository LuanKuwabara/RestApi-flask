import os


class DevConfig:
    MONGODB_SETTINGS = {
        "db": os.getenv("MONGODB_DB", "users"),
        "host": os.getenv("MONGODB_HOST", "mongo"),
        "port": int(os.getenv("MONGODB_PORT", 27017)),
        "username": os.getenv("MONGODB_USER", "admin"),
        "password": os.getenv("MONGODB_PASSWORD", "admin"),
        "authentication_source": "admin"
    }


class MockConfig:
    MONGODB_SETTINGS = {
        "db": "users",
        "host": 'mongomock://localhost'
    }
