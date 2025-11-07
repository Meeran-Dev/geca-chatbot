
import os
from waitress import serve
from index import app # or wherever your WSGI app object is

print("--- Start: Reading Configuration ---")
PORT = int(os.environ.get('PORT', 5000)) 
print(f"--- Config Read: PORT={PORT} ---")

if __name__ == '__main__':
    print("--- Start: Application Initialization ---")
    
    print("--- End: Application Initialization ---")
    serve(app, host='0.0.0.0', port=PORT, threads=4)
    print("--- End: Server Started ---")