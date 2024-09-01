import anthropic
import discord
import os
import asyncio
from dotenv import load_dotenv


# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からトークンとAPIキーを取得
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

ASK_COMMAND_EN = '$ask'
ASK_COMMAND_JA = '$質問'


# Discord Clientの設定
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

# Anthropic Clientの設定
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')

async def process_command(message, command, user_input):
    try:
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.5,
            system="あなたは古代ギリシャから現代日本に転生したフレッシュな発想を持つ吟遊詩人です",
            messages=[{"role": "user", "content": user_input}]
        )
        return response
    except anthropic.exceptions.APIError:
        return "申し訳ありません。APIの呼び出し中にエラーが発生しました。"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "申し訳ありません。予期しないエラーが発生しました。"

async def send_response(message, response):
    if hasattr(response, 'content'):
        text_blocks = response.content
        cleaned_texts = [block.text.replace('\\n', '\n').replace('\\u3000', '　').replace('\\t', '\t')
                            for block in text_blocks if hasattr(block, 'text')]

        for cleaned_text in cleaned_texts:
            await message.channel.send(cleaned_text)
    else:
        await message.channel.send("申し訳ありません。応答の処理中にエラーが発生しました。")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith((ASK_COMMAND_EN, ASK_COMMAND_JA)):
        command = ASK_COMMAND_EN if message.content.startswith(ASK_COMMAND_EN) else ASK_COMMAND_JA
        command_length = len(command + ' ')
        user_input = message.content[command_length:]
        response = await process_command(message, command, user_input)
        await send_response(message, response)

async def process_messages():
    while True:
        messages = await discord_client.wait_for('message', check=lambda m: m.content.startswith((ASK_COMMAND_EN, ASK_COMMAND_JA)))
        tasks = []
        for message in [messages]:  # Wrap messages in a list to handle single message case
            command = ASK_COMMAND_EN if message.content.startswith(ASK_COMMAND_EN) else ASK_COMMAND_JA
            command_length = len(command + ' ')
            user_input = message.content[command_length:]
            tasks.append(process_command(message, command, user_input))
        responses = await asyncio.gather(*tasks)
        for message, response in zip([messages], responses):  # Wrap messages in a list to handle single message case
            await send_response(message, response)

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')
    discord_client.loop.create_task(process_messages())

# Discord Botを実行
discord_client.run(DISCORD_BOT_TOKEN)
