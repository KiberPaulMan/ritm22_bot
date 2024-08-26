import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

white_users_id = [
    int(os.getenv('ANNA_TG_ID')),
    int(os.getenv('ALENA_TG_ID')),
    int(os.getenv('PAVEL_TG_ID')),
]
