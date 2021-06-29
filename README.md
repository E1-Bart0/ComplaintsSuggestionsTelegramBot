# TELEGRAM BOT FOR COMPLAINTS AND SUGGESTIONS

python-version: 3.9.0


You or your command can easily ask or suggest or even complain about something in Telegram, and not being afraid of others opinions.

Because of this bot, you can do it anonymously.
Just write your message to the bot, and he will re-sent your message to all SuperUsers from his name.

## How to install

With Docker-Compose:

```shell script
cd <PATH_TO_PROJECT>
# set up your environments variables in .env file

# Create DB in Docker, apply migrations and launch BOT in docker
make run_bot
```

## How to Run Tests

```shell script
cd <PATH_TO_PROJECT>
# set up your environments variables in .env file

# Create TEST DB in Docker
make init_test_db
pytest tests
```
