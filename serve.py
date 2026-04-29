
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

print("--- Start: Reading Configuration ---")
PORT = int(os.getenv('PORT', 5000)) 
print(f"--- Config Read: PORT={PORT} ---")

if __name__ == '__main__':
    print("--- Start: Application Initialization ---")
    print("--- End: Application Initialization ---")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)
    print("--- End: Server Started ---")