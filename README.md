# What's this?
A Discord bot I originally made to log my pinned notes & shopping lists (for personal use). You can use this bot to handle server pins.

This project is open to suggestions and improvements; feel free to make a pull request!
# Features
Trashpin responds to pinned messages and various slash commands...

#### Pinned messages are logged if they were sent after the bot's most recent startup.
<!-- TODO: Denote the most recent startup and other stats. -->

## Commands
```/enable [channel]```

> Enables pin archiving for the specified channel.

```/disable```

> If pin archiving is enabled, this command disables it.

```/ping```

> Returns the bot's latency.

```/help```

> Returns a guide on how to use the bot.

<!-- TODO: Add images of usage. -->
# Usage
You can either [invite the bot](https://discord.com/api/oauth2/authorize?client_id=1133351003803091094&permissions=414464732352&scope=bot) or run it locally...
## Running it locally
First, install the module requirements:
```bash
pip install -r requirements.txt
```
Make sure the `trashpin` folder is the directory of the following commands...

Then, run `main.py`..
```bash
python main.py
```
or run the script but hide the terminal:
```bash
pythonw main.py
```
> However you run the Python file does not matter. At the moment, I run the script from Visual Studio Code on the Raspberry Pi I have under my piano lol.

##### Alternatively, you can run the `trashpin.bat` if your computer allows. This will run the script without showing the terminal, but you'll still have to download the Python requirements.
> As a possible use for this file, you can set the `trashpin.bat` file to run on startup.