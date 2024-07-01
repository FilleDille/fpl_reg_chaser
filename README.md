# FPL Registration Chaser

This script aims to alert the users when the fpl registration has opened, with the goal to let the users get low players id's. The script checks if less than 1 million are registered as active players at the moment and if any news article has been released with information about the registration being open. If any of these two checks validate then an email is sent to each of the users in the env file. The frequency of the checks is determined by the user. I run the script with crontab on a raspberry pi.

## Table of Contents
- [Setup and Installation](#setup-and-installation)
- [Instructions](#instructions)

## Setup and Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/FilleDille/fpl_reg_chaser.git
   cd fpl_reg_chaser
   ```
2. **Create a virtual environment:**
    ```sh
   python3.12 -m venv venv
   source venv/bin/activate
   ```
3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
 
4. **Set up the env file:**
    ```sh
    echo -e "APP_PW=abcdefg\nEMAIL_FROM=mail@example.com\nEMAIL_ADMIN=admin@example.com\nEMAIL_SENT=false\nEMAIL_TO=recipient@example.com,another_recipient@example.com" > .env
    ```
    This assumes the sender uses gmail and has created an app password (google how to set one up)

## Instructions	
To run a check, run the following command:
```sh
python main.py
```

To ping the server and see if the service is available, run the following command:
```sh
python main.py --ping
```

To reset the EMAIL_SENT variable (if it triggers by mistake), run the following command:
```sh
python main.py --reset
```


I have two crontab jobs - one that runs every minute during certain hours and one ping run a day to ensure everything is working.
