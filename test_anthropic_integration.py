import unittest
from unittest import mock
import os
import asyncio
from dotenv import load_dotenv
import anthropic
from main import process_command, discord_client, send_response, MAX_CONCURRENT_REQUESTS

class TestAnthropicAPI(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not cls.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in .env file")
        
        cls.anthropic_client = anthropic.Anthropic(api_key=cls.anthropic_api_key)

    async def test_anthropic_api_access(self):
        test_input = "こんにちは、古代ギリシャから来た吟遊詩人さん。簡単な俳句を一つ詠んでください。"
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.5,
                system="あなたは古代ギリシャから現代日本に転生したフレッシュな発想を持つ吟遊詩人です",
                messages=[{"role": "user", "content": test_input}]
            )
            
            self.assertIsNotNone(response.content)
            self.assertIsInstance(response.content[0].text, str)
            self.assertTrue(len(response.content[0].text) > 0)
            
            print(f"API Response: {response.content[0].text}")
            
        except anthropic.APIError as e:
            self.fail(f"API Error occurred: {str(e)}")
        except Exception as e:
            self.fail(f"Unexpected error occurred: {str(e)}")

    @mock.patch('main.anthropic_client')
    async def test_process_command_integration(self, mock_anthropic_client):
        mock_message = mock.AsyncMock()
        mock_message.content = "$ask 古代ギリシャの詩の特徴を教えてください。"
        mock_message.channel.send = mock.AsyncMock()

        # AsyncMockを使って非同期関数を正しくモック
        mock_response = mock.AsyncMock()
        mock_response.content = [mock.MagicMock(text="古代ギリシャの詩の特徴には...")]
        mock_anthropic_client.messages.create.return_value = asyncio.Future()
        mock_anthropic_client.messages.create.return_value.set_result(mock_response)

        response = await process_command(mock_message, mock_message.content[5:])

        self.assertTrue(mock_message.channel.send.called)
        
        calls = mock_message.channel.send.call_args_list
        sent_message = ' '.join([call.args[0] for call in calls])
        print(f"Sent message: {sent_message}")
        self.assertIn("古代ギリシャ", sent_message)
        self.assertIn("詩", sent_message)

    @mock.patch('main.anthropic_client')
    @mock.patch('main.request_semaphore', asyncio.Semaphore(MAX_CONCURRENT_REQUESTS))
    async def test_concurrent_requests(self, mock_anthropic_client):   
        async def mock_api_call(*args, **kwargs):
            await asyncio.sleep(0.1)  # API呼び出しの遅延をシミュレート
            return mock.AsyncMock(content=[mock.MagicMock(text="テスト応答")])

        mock_anthropic_client.messages.create = mock.AsyncMock(side_effect=mock_api_call)

        mock_messages = [mock.AsyncMock() for _ in range(10)]
        for msg in mock_messages:
            msg.content = "$ask テストクエリ"
            msg.channel.send = mock.AsyncMock()

        start_time = asyncio.get_event_loop().time()
        # 10個の並行リクエストを実行
        await asyncio.gather(*(process_command(msg, msg.content[5:]) for msg in mock_messages))
        end_time = asyncio.get_event_loop().time()

        total_time = end_time - start_time

        # 全てのメッセージが処理されたことを確認
        for msg in mock_messages:
            self.assertTrue(msg.channel.send.called, "channel.send was not called for a message")

        # 総実行時間が予想範囲内であることを確認
        expected_time = 0.2  # MAX_CONCURRENT_REQUESTSが5の場合、2バッチで完了するはず
        self.assertGreaterEqual(total_time, expected_time)
        self.assertLess(total_time, expected_time * 1.5)  # 50%の余裕を持たせる

        print(f"Concurrent requests test completed in {total_time:.2f} seconds")

if __name__ == '__main__':
    unittest.main()
