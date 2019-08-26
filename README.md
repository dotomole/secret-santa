
# Secret Santa - Email Script

This Python script generates Secret Santa by reading a .csv file of people and emailing everyone with their randomly assigned person to whom they must buy a gift for.

## Usage
You require a .csv file in the following format:

`firstname,lastname,email` to be saved as **people.csv** (Example in folder)

<br>
Then run script (with Python installed) as: `py secretsanta.py`  

You will then be prompted for your email login for where the emails will send from. Once entered the program will begin assigning random variables to people and send out all the emails.

## Notes
At the moment it's only set up for Gmail accounts to send from, thus you'll need to login with a Gmail account.