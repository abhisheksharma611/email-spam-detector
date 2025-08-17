"""
Flask Application Factory for Spam Detection System
"""
from flask import Flask, render_template
from config import config

def create_app(config_name='default'):
    """
    Application factory function that creates and configures the Flask app
    """
    
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    # Add context processors for global template variables
    @app.context_processor
    def inject_config():
        return {
            'APP_NAME': app.config['APP_NAME'],
            'VERSION': app.config['VERSION']
        }
    
    return app
