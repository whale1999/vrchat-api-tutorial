import datetime
import requests

from config import USER_NAME, LOGIN_PASS, API_KYE
from psql import insert_loggined_friends, load_table, delete_table_contents
from slack import send_slack_message

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

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

    moderations_filtered =  []
    for i in (list(moderations)):

        temp_list = []
        temp_list.append(i['displayName'])
        temp_list.append(i['status'])
        temp_list.append(i['location'])
        temp_list.append(now.strftime('%x %X'))
        moderations_filtered.append(temp_list)

    return moderations_filtered


def update_online_friends_status(online_friends):

    # Delete the data in the table once for updating.
    delete_table_contents('loggined_friends')
    # Only the name is registered in the database.
    online_friends_name = [x[0] for x in online_friends]
    insert_loggined_friends(online_friends_name)



def main():

    # Prepare the data retrieved from the database
    regsitered_online_friends = load_table('loggined_friends')
    regsitered_online_friends = [x for row in regsitered_online_friends for x in row]
    monitoring_friends = load_table('monitoring_friends')
    monitoring_friends = [x for row in monitoring_friends for x in row]
    now_online_friends = online_friends_list()
    now_online_friends_name = [x[0] for x in now_online_friends]
    
    # Detect the difference between the last online friend registered and the new online friend acquired.
    new_detected_online_friends = list(set(now_online_friends_name) - set(regsitered_online_friends))
    
    # Send a notification to Slack when a monitored friend is detected
    for name in monitoring_friends:
        if  name in new_detected_online_friends:
            detected_monitoring_frind = now_online_friends[now_online_friends_name.index(name)]
            send_slack_message(detected_monitoring_frind)

    # update Database now online friends
    update_online_friends_status(now_online_friends)



if __name__ == "__main__":
    main()