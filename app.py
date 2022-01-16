import datetime
import requests

from config import USER_NAME, LOGIN_PASS, API_KYE, LOGGINED_FRIENDS, MONITORING_FRIENDS
from psql import insert_loggined_friends, load_table, delete_table_contents
from slack import send_slack_message

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
present_time = now.strftime('%x %X')

data = {'apiKey': API_KYE}
headers  = {'User-Agent': 'SunaFH/1.0.5'}


# get authToken
def authenticate():

    try:
        response = requests.get('https://api.vrchat.cloud/api/1/auth/user', data=data, headers=headers, auth=(USER_NAME, LOGIN_PASS))
        authToken = response.cookies['auth']
        return authToken
    except:
        print('You can not login')
        # Send notifications with slack
        send_slack_message('An authentication error has occurred.')


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
        temp_list.append(present_time)
        moderations_filtered.append(temp_list)

    return moderations_filtered


def update_online_friends_status(online_friends):

    # Delete the data in the table once for updating.
    delete_table_contents(LOGGINED_FRIENDS)
    # Only the name is registered in the database.
    online_friends_name = [x[0] for x in online_friends]
    insert_loggined_friends(online_friends_name)



def main():

    # Prepare the data retrieved from the database
    regsitered_online_friends = load_table(LOGGINED_FRIENDS)
    regsitered_online_friends = [x for row in regsitered_online_friends for x in row]
    monitoring_friends = load_table(MONITORING_FRIENDS)
    monitoring_friends = [x for row in monitoring_friends for x in row]
    now_online_friends = online_friends_list()
    now_online_friends_name = [x[0] for x in now_online_friends]
    
    # Detect the difference between the last online friend registered and the new online friend acquired.
    new_detected_online_friends = list(set(now_online_friends_name) - set(regsitered_online_friends))
    
    
    for name in monitoring_friends:
        # Send a notification to Slack when a monitored friend is detected
        if name in new_detected_online_friends:
            detected_monitoring_frind_name = now_online_friends[now_online_friends_name.index(name)]
            send_slack_message(detected_monitoring_frind_name)

            # Send a notification via slack when a monitored friend logs out.
        if name in regsitered_online_friends and name not in now_online_friends_name:
            print(name + ' has logged out at ' + present_time)

    # update Database now online friends list
    update_online_friends_status(now_online_friends)



if __name__ == "__main__":
    main()