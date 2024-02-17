Logging and printing code for a telegram bot that records user reactions to each message.

## Requirements

- Python>=3.8
- Python libraries: `pandas`, `python-telegram-bot`

Install the required libraries with

```bash
python3 -m pip install pandas python-telegram-bot
```

## Usage

Using BotFather, create a bot and give it permissions to access group messages. Add it **as administrator** to any groups you want to monitor.

To start logging, run:

```bash
python3 bot.py [TELEGRAM-BOT-TOKEN]
```

The data will be saved in the files `messages.csv` and `reactions.csv` while the code is running. In order to print the logged data, use the command

```bash
python3 summary.py
```
