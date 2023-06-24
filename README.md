# fpl_reg_chaser

This script checks how many total players are registered. If less than 1 million then the new season has opened for registration and an email is sent to myself along with a message. The reason is to be able to get a low team ID for the season.

The .env file contains my gmail address and the app password (not the same as account password, google it).

I have added three types of messages:
1. normal
2. ping
3. error

Normal message is __the message__ that is supposed to get me to stop everything i'm doing and rush to the app to register the team.

Ping message is sent to verify that the server is up and running and the script works as intended. A ping message is sent when adding a random sys argument to the script.

The error message simply adds the api response code followed by the response text.

I have two crontab jobs - one that runs every minute during certain hours and one ping run a day to ensure everything is working.