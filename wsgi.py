import os
from app import create_app

# Set environment variables for deployment
os.environ.setdefault('DB_TYPE', 'sqlite')
os.environ.setdefault('DEBUG', 'False')

# Create the Flask app
app = create_app('production')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
