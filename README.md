## Installation
1. run `pip install -r requirements.txt`
2. create `src/config.py` wich should contain:
```
BOT_TOKEN = "your telegram bot token"
PROVERKA_CHECKA_TOKEN = "your personal token to access proverkachecka api"
SPREADSHEET_KEY = "the key part of your spreadsheet's url"
```
3. run `python3 src/bot.py`

## Useful resources:
- https://proverkacheka.com/
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [gspread guide](https://docs.gspread.org/en/latest/oauth2.html)