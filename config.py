from dotenv import load_dotenv,find_dotenv

load_dotenv(verbose=True)

import os 
print(os.getenv("TOKEN"))