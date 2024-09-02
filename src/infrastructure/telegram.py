from aiogram import Bot
from aiogram.types import ForumTopic, Message

from src.application.common.telegram import TelegramTopic
from src.infrastructure.config import BotSettings


class TelegramTopicManager(TelegramTopic):
    def __init__(self, bot: Bot, config: BotSettings):
        self.bot = bot
        self.config = config

    async def create_topic(self, name: str) -> ForumTopic:
        return await self.bot.create_forum_topic(
            chat_id=self.config.orders_group_id,
            name=name,
        )
    
    async def send_topic_message(self, thread_id: int, message: str) -> Message:
        return await self.bot.send_message(
            chat_id=self.config.orders_group_id,
            text=message,
            message_thread_id=thread_id,
        )
    