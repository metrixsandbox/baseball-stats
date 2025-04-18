import os

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///baseball_stats.db')
    API_KEY = os.getenv('API_KEY', 'your_api_key_here')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test_baseball_stats.db')

class ProductionConfig(Config):
    """Production configuration."""
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///baseball_stats.db')