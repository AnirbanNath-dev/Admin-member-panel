import os
from dotenv import load_dotenv

load_dotenv()

try:
    USERNAME = os.environ.get('NAME')
    PASSWORD = os.environ.get('PASSWORD')
except:
    USERNAME = 'ExampleUser'
    PASSWORD = 'ExamplePassword'

