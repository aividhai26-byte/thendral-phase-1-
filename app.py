import os

# Set environment variables for deployment
os.environ.setdefault('DB_TYPE', 'sqlite')
os.environ.setdefault('DEBUG', 'False')

from app import create_app

# Create the Flask app
app = create_app('production')
