import unittest
from unittest.mock import AsyncMock, patch
import os
import asyncio
from dotenv import load_dotenv
import main  # あなたのメインbotファイル

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()  # .envファイルから環境変数を読み込む
        cls.bot = main.discord_client

    async def asyncSetUp(self):
        self.test_token = os.getenv('TEST_DISCORD_BOT_TOKEN')
        self.assertIsNotNone(self.test_token, "TEST_DISCORD_BOT_TOKEN is not set in .env file")

    async def asyncTearDown(self):
        await self.bot.close()

    @patch('discord.Client.login')
    @patch('discord.Client.connect')
    async def test_bot_startup(self, mock_connect, mock_login):
        # ボットの起動をテスト
        try:
            await asyncio.wait_for(self.bot.start(self.test_token), timeout=5.0)
        except asyncio.TimeoutError:
            self.fail("Bot startup timed out")
        
        mock_login.assert_called_once()
        mock_connect.assert_called_once()

    # ここに他のテストケースを追加

if __name__ == '__main__':
    unittest.main()
