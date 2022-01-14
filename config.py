import os
from dotenv import load_dotenv
load_dotenv()


# AUthentication Configuration
USER_NAME = os.environ['USER_NAME']
LOGIN_PASS = os.environ['LOGIN_PASS']

# api key 
API_KYE = 'JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26'
# Slakc web_hook_url
SLACK_WEB_HOOK_URL = os.environ['SLACK_WEB_HOOK_URL']
# postgres
DATABASE_URL = os.environ['DATABASE_URL']