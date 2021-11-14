# twitch-plays-connect-4
A connect four game allowing multiple users to play against a multi-difficulty level bot, using twitch chat as their input.

Many users can play at once, each choosing a particular column in which they'd like to drop a disc in, the most popular column will be chosen as input by the program.

The bot has three different levels, Easy, Medium and Hard.

##  Setting up the program
####  Complete the following prerequisites to run the program
#####  Installing NumPy
Python as standards comes with the pip package installer, by using pip, NumPy can be 
installed with the command:
pip install numpy

##### Populating a Vars.py file
You must create a file named 'vars.py' in the main directory, which will hold all of the variables for the chatbot. Use the template below.

```
    data = {
        "BOT_USERNAME": "",
        "OAUTH_TOKEN": "",
        "CHANNEL_NAME":"",
        "PORT": 6667
    }
```

- BOT_USERNAME – value must be set to a string containing the username of the bot account
- OAUTH_TOKEN – value must be a string containing the chatbots OAuth key, retrieved on the Twitch developer website
- CHANNEL_NAME – value must be set to a string containing the channel in which the bot will be run (generally the bots channel)
- PORT – value must be set to the integer: 6667

##### On completion of these prerequisites, the bot can be run by opening the Bot.py file.
