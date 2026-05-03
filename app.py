import os
import sys

# Set environment variables for deployment
os.environ.setdefault('DB_TYPE', 'sqlite')
os.environ.setdefault('DEBUG', 'False')

try:
    from app import create_app
    app = create_app('production')
except Exception as e:
    print(f"Error creating app: {e}")
    sys.exit(1)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
