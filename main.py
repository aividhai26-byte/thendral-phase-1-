import os
from flask import Flask, render_template

# Set environment variables for deployment
os.environ.setdefault('DB_TYPE', 'sqlite')
os.environ.setdefault('DEBUG', 'False')

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    
    # Production-ready configuration for Render
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'thendral-city-dev-secret-key-2024')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database configuration - SQLite for Render deployment
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thendral_construction.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Static file configuration
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    @app.route('/')
    def index():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Thendral City Developers</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; text-align: center; }
                .success { color: #28a745; font-size: 24px; }
                .info { color: #17a2b8; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1 class="success">🎉 Thendral City Developers</h1>
            <p class="info">Successfully deployed on Render!</p>
            <p>Application is running correctly.</p>
            <p><a href="/health">Health Check</a></p>
        </body>
        </html>
        """
    
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "service": "thendral-construction"}
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    # Initialize database on startup
    with app.app_context():
        try:
            from flask_sqlalchemy import SQLAlchemy
            db = SQLAlchemy(app)
            
            # Import models to ensure they're registered
            from app.models import project, admin
            db.create_all()
        except ImportError:
            # Models not available, continue without database
            pass
    
    return app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
