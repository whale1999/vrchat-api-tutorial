import requests
from urllib.parse import quote
from config import USER_NAME, LOGIN_PASS, API_KYE

data = {'apiKey': API_KYE}
headers  = {'User-Agent': 'SunaFH/1.0.5'}

# get authToken
def authenticate():

    try:
        response = requests.get('https://api.vrchat.cloud/api/1/auth/user', data=data, headers=headers, auth=(USER_NAME, LOGIN_PASS))
    except:
        print('You can not login')
        
    authToken = response.cookies['auth']

    return authToken


def online_friends_list():

    authToken = authenticate()
    response = requests.get('https://api.vrchat.cloud/api/1/auth/user/friends', data=data, headers=headers, params={"authToken": authToken})
    moderations = response.json()
    print(moderations)

online_friends_list()