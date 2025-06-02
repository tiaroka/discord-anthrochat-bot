import discord
import os
import time
from collections import deque
from dotenv import load_dotenv
import asyncio
import anthropic

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からトークンとAPIキーを取得
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

ASK_COMMAND_EN = '$ask'
ASK_COMMAND_JA = '$質問'

# 同時実行数の制限
MAX_CONCURRENT_REQUESTS = 5

# Discord Clientの設定
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

# Anthropic Clientの設定
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# セマフォの設定
request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# メッセージ履歴を保持するリスト（最大10件）
message_history = deque(maxlen=10)

# メッセージの有効期限（秒）
MESSAGE_EXPIRATION_TIME = 3600  # 1時間

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith(ASK_COMMAND_EN) or message.content.startswith(ASK_COMMAND_JA):
        user_input = message.content[len(ASK_COMMAND_EN):].strip() if message.content.startswith(ASK_COMMAND_EN) else message.content[len(ASK_COMMAND_JA):].strip()
        current_time = time.time()
        
        # メッセージ履歴にユーザーのメッセージを追加
        message_history.append({"role": "user", "content": f"{message.author.name}: {user_input}", "timestamp": current_time})
        
        # 古いメッセージを削除
        while message_history and current_time - message_history[0]["timestamp"] > MESSAGE_EXPIRATION_TIME:
            message_history.popleft()
        
        async with request_semaphore:
            try:
                # Claude APIに問い合わせ
                response = anthropic_client.messages.create(
                    model="claude-opus-4-20250514",
                    max_tokens=1000,
                    temperature=0.5,
                    system="あなたは古代ギリシャから現代日本に転生したフレッシュな発想を持つ吟遊詩人です",
                    messages=[{"role": msg["role"], "content": msg["content"]} for msg in message_history]
                )
                
                # レスポンスからテキストを抽出
                response_text = response.content[0].text
                
                # メッセージ履歴にClaudeの応答を追加
                message_history.append({"role": "assistant", "content": response_text, "timestamp": current_time})
                
                # Discordに応答を送信
                await message.channel.send(response_text)
            except Exception as e:
                await message.channel.send(f"Error: {e}")

# Discord Botを実行
discord_client.run(DISCORD_BOT_TOKEN)