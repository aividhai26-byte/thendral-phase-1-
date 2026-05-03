"""
Application Entry Point
Run this file to start the Flask development server
"""

from app import create_app
import os

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Get debug mode from environment variable
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Get host from environment variable or default to localhost
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"\n{'='*50}")
    print(f"Thendral City Developers Website")
    print(f"{'='*50}")
    print(f"Starting server on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*50}\n")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)
