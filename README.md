## What kind of project is this?
This is my trial telegram bot with mini-games and a randomizer.

## What did I use to create?
- Python
  - telebot
  - dotenv
- sqlite3

To create a bot, I use the telebot, as well as the python programming language, and to store a local database, I used sqlite3.

### Structure project
```
Telebot-Krep
├── .env
├── .example.env
├── .gitignore
├── README.md
├── data            # Data for bot
│   ├── database    # Local database (sqlite3)
│   └── photo
├── requirements.txt
└── src
    ├── config
    │   └── config.py      # Init config param
    ├── database           # Classes for database
    │   └── user.py        # Classes for user db
    ├── handler            # All handlers_messages
    │   ├── help.py
    │   ├── info.py
    │   ├── other.py
    │   ├── random_val.py
    │   ├── roulette.py
    │   └── start.py
    ├── main.py            # Entry point
    └── utils              # All utilites
        ├── check_format.py
        ├── random_val_mode.py
        └── roulette_casino.py

```

## What was this project created for?
This project was created for the purpose of training the creation of telegram bots.
