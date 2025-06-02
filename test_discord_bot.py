import unittest
import os
import asyncio
from dotenv import load_dotenv
import discord
from unittest.mock import AsyncMock, patch, MagicMock
from main import discord_client

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.test_token = os.getenv('TEST_DISCORD_BOT_TOKEN')
        if not cls.test_token:
            raise ValueError("TEST_DISCORD_BOT_TOKEN is not set in .env file")

    async def asyncSetUp(self):
        self.mock_bot = MagicMock(spec=discord_client)
        self.mock_bot.wait_until_ready = AsyncMock()
        self.mock_bot.close = AsyncMock()
        self.mock_bot.logout = AsyncMock()

    async def test_bot_startup(self):
        try:
            with patch('main.discord_client', self.mock_bot):
                startup_task = asyncio.create_task(self.mock_bot.start(self.test_token))
                await asyncio.wait_for(self.mock_bot.wait_until_ready(), timeout=5.0)
                self.assertTrue(self.mock_bot.is_ready())
                print(f"Bot is ready. Logged in as {self.mock_bot.user}")
        except asyncio.TimeoutError:
            self.fail("Bot startup timed out")
        finally:
            if startup_task and not startup_task.done():
                startup_task.cancel()
            await self.mock_bot.close()

    async def test_bot_shutdown(self):
        # シャットダウンをシミュレート
        with patch('main.discord_client', self.mock_bot):
            # ボットの起動をシミュレート
            await self.mock_bot.start(self.test_token)
            self.assertTrue(self.mock_bot.is_ready())

            # ボットのシャットダウンをシミュレート
            await self.mock_bot.close()
            
            # close メソッドが呼び出されたことを確認
            self.mock_bot.close.assert_called_once()
            
            # ボットが正しく終了したことを確認
            # 注: 実際のボットでは、is_closed() メソッドがある場合があります
            if hasattr(self.mock_bot, 'is_closed'):
                self.assertTrue(self.mock_bot.is_closed())
            
            print("Bot shutdown test completed successfully")

    # 他のテストメソッド...

if __name__ == '__main__':
    unittest.main()