# Notify me when a friend logs in VRChat.

"vrchat-api-tutorial" can be used when you don't want to have to check every single time to see if your VRChat friend has logged in or not. Friends here is a "special friend".

***

## Specifications
 
**On Heroku, after running app.py periodically, use slack to receive notifications. Postgres is used to record the friends login status and names of friends you want to monitor.**
***
## Usage
**First**, you need to set "USER_NAME"(VRChathat), "LOGIN_PASS"(VRChat), "SLACK_WEB_HOOK_URL"(Slack), and "DATABASE_URL(Postgres)" as environment variables on heroku console.

**Next**, create a table to record the names of friends who are logged in at the moment and a table to record the names of friends you want to monitor. I use the table names "loggined_friends" and "monitoring_friends". This can be any name you want, but you will need to modify some of the code in app.py.

 

    Table "loggined_friends"
 
    name | character varying(150) 

    Table "public.monitoring_friends"
 
    name   | character varying(150)


## Finally, if you are not me, please do not use this code. Do not trust it.
