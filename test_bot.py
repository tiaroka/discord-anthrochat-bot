import unittest
from unittest.mock import AsyncMock, patch
import os
import main  # あなたのメインbotファイル

class TestDiscordBot(unittest.TestCase):
    def setUp(self):
        self.bot = main.discord_client

    @patch.dict(os.environ, {'DISCORD_BOT_TOKEN': 'dummy_token'})
    @patch('discord.Client.login')
    @patch('discord.Client.connect')
    async def test_bot_startup(self, mock_connect, mock_login):
        # ボットの起動をテスト
        await self.bot.start('dummy_token')
        mock_login.assert_called_once()
        mock_connect.assert_called_once()

    # ここに他のテストケースを追加

if __name__ == '__main__':
    unittest.main()
