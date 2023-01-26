from telethon import TelegramClient
from collections import defaultdict


class Channel:
    """
    Get posts and comments of Telegram channel(s).
    
    Example:
    >>> from channel import Channel
    >>> channel = Channel(api_id=123, api_hash='123abc')
    >>> channel.get_posts(channels=['channel_name'])
    {'djangoex': [{'post_id': 1, 'post_text': 'Post 1', 'comments': [{'comment_id': 2, 'comment_text': 'Comment 1', 'comment_author': 1}, {'comment_id': 3, 'comment_text': 'Comment 2', 'comment_author': 1}]}, {'post_id': 4, 'post_text': 'Post 2', 'comments': [{'comment_id': 5, 'comment_text': 'Comment 3', 'comment_author': 1}, {'comment_id': 6, 'comment_text': 'Comment 4', 'comment_author': 1}]}]}
    """

    def __init__(self, api_id: int, api_hash: str):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.client.start()

    async def _get_posts(self,
                         channel: str,
                         limit_posts: int = 10,
                         limit_comments: int = 10) -> dict:
        res = []
        channel_entity = await self.client.get_entity(channel)
        posts = await self.client.get_messages(channel_entity,
                                               limit=limit_posts)
        for post in posts:
            comments = await self.client.get_messages(channel_entity,
                                                      reply_to=post.id,
                                                      limit=limit_comments)

            res.append({
                "post_id":
                post.id,
                "post_text":
                post.message,
                "comments": [{
                    "comment_id": comment.id,
                    "comment_text": comment.message,
                    "comment_author": comment.sender_id
                } for comment in comments]
            })
        return res

    def get_posts(self,
                  channels: list,
                  limit_posts: int = 10,
                  limit_comments: int = 10):
        """
        Get posts and comments of Telegram channel(s).
        :param channels: channel name(s)
        :param limit_posts: limit of posts
        :param limit_comments: limit of comments
        :return: posts and comments of Telegram channel(s)
        """
        posts = defaultdict(list)
        for channel in channels:
            posts[channel] = self.client.loop.run_until_complete(
                self._get_posts(channel, limit_posts, limit_comments))
        return posts
