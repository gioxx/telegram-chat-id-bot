# Telegram Group/Channel ID Bot

A simple Telegram bot that sends you the ID of any group or channel when you add it.

> [!NOTE]  
> I have started a demo container so you can try out the bot. You can find it on Telegram: [@gwall_chatid_bot](https://t.me/@gwall_chatid_bot). Feel free to launch it and use it.  
> Heads-up: this is hosted on a Raspberry Pi at home (best-effort availability).
> It may be temporarily unreachable, please don’t rely on it for production.

## Features

- Automatically detects when added to a group or channel
- Sends a private message with the chat ID to the user who added it
- Works with both groups and channels
- Simple `/start` command for instructions

## Commands

- `/start` - Get bot instructions
- `/getid` - Get the current chat ID (works in groups, channels, and private chats)

## Setup

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Copy the bot token
3. Create `.env` file with your token:

```
TELEGRAM_BOT_TOKEN=your_token_here
```

## Running with Docker

```
docker-compose up -d
```

## Important Notes

**Privacy Requirement**: Users must start the bot privately with `/start` before adding it to a group. Otherwise, Telegram will block the bot from sending private messages.

**Recommended Workflow**:
1. User starts bot with `/start` command
2. User adds bot to group/channel
3. Bot sends group/channel ID via private message

## Usage

1. Start the bot with `/start` command in private chat
2. Add the bot to any group or channel
3. Receive the group/channel ID in your private chat with the bot
