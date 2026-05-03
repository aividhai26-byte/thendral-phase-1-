import os
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Set environment variables for deployment
os.environ.setdefault('DB_TYPE', 'sqlite')
os.environ.setdefault('DEBUG', 'False')

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    
    # Basic configuration for Render deployment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database configuration
    if os.getenv('DB_TYPE', 'sqlite') == 'mysql':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///thendral_construction.db')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thendral_construction.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Upload configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please login to access this page.'
    login_manager.login_message_category = 'warning'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return None  # Simplified for deployment
    
    # Create main blueprint
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        return "<h1>Thendral City Developers - Deployment Test</h1><p>App is working on Render!</p>"
    
    # Register blueprint
    app.register_blueprint(main_bp)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
