# telegram-crawler
Collecting posts and comments of Telegram channel(s).

## Installation
1. Install Python 3.6 or higher.
2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage
1. Create a Telegram app and get the API ID and API hash from [here](https://my.telegram.org/apps).
2. Create a python file and write the following code:
```python
from telegram_crawler import Channel

channel = Channel(api_id=123456, api_hash='0123456789abcdef0123456789abcdef')
posts = channel.get_posts('channel_name') # Return dictionary(key: channel_name, value: list of posts(dict))
```