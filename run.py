"""
Main application entry point for the Spam Detection Flask App
"""
import os
from app import create_app

# Create the Flask application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # Get port from environment variable (required for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
