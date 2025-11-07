
import os
from waitress import serve
from index import app # or wherever your WSGI app object is

# Render uses the PORT environment variable, defaulting to 5000 or 10000
# We will use os.environ.get('PORT', '5000') to be safe.
PORT = int(os.environ.get('PORT', 5000)) 

if __name__ == '__main__':
    print(f"Starting Waitress server on http://0.0.0.0:{PORT}")
    # Host must be 0.0.0.0 to listen on all public interfaces
    serve(app, host='0.0.0.0', port=PORT, threads=4)