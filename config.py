"""
Configuration settings for the Spam Detection Application
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Application settings
    APP_NAME = "Email Spam Detection & Classification System"
    VERSION = "1.0.0"
    
    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_DIR = os.path.join(DATA_DIR, 'trained_models')
    
    # Email classification categories
    EMAIL_CATEGORIES = [
        'spam', 'ham', 'promotional', 'phishing', 'newsletter', 'social'
    ]
    
    # Spam detection thresholds
    SPAM_THRESHOLD = 0.7
    PHISHING_THRESHOLD = 0.8
    
    # Model settings
    MODEL_FILENAME = 'spam_classifier.pkl'
    VECTORIZER_FILENAME = 'tfidf_vectorizer.pkl'
    
    # Session timeout
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
