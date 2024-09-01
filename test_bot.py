import unittest
from unittest.mock import AsyncMock, patch
import os
from dotenv import load_dotenv
import main  # あなたのメインbotファイル

class TestDiscordBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()  # .envファイルから環境変数を読み込む
        cls.bot = main.discord_client

    @patch('discord.Client.login')
    @patch('discord.Client.connect')
    async def test_bot_startup(self, mock_connect, mock_login):
        # ボットの起動をテスト
        test_token = os.getenv('TEST_DISCORD_BOT_TOKEN')
        self.assertIsNotNone(test_token, "TEST_DISCORD_BOT_TOKEN is not set in .env file")
        await self.bot.start(test_token)
        mock_login.assert_called_once()
        mock_connect.assert_called_once()

    # ここに他のテストケースを追加

if __name__ == '__main__':
    unittest.main()
