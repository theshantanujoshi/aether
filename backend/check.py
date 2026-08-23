import os
from dotenv import load_dotenv

def check_setup():
    load_dotenv()
    print("Checking RocketRide setup...")
    
    rocketride_key = os.getenv("ROCKETRIDE_APIKEY")
    if not rocketride_key:
        print("WARNING: ROCKETRIDE_APIKEY is not set in .env")
    else:
        print("ROCKETRIDE_APIKEY is set.")
        
    openai_key = os.getenv("ROCKETRIDE_OPENAI_KEY")
    if not openai_key:
        print("WARNING: ROCKETRIDE_OPENAI_KEY is not set in .env (needed for LLM components)")
    else:
        print("ROCKETRIDE_OPENAI_KEY is set.")
        
    qdrant = os.getenv("ROCKETRIDE_QDRANT_HOST")
    if not qdrant:
        print("WARNING: ROCKETRIDE_QDRANT_HOST is not set in .env")
    else:
        print("ROCKETRIDE_QDRANT_HOST is set.")
        
    print("\nSetup check complete. Please ensure Qdrant is running locally if using local vector DB.")

if __name__ == "__main__":
    check_setup()
