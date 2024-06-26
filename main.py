import anthropic
import discord
import os
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

        await send_response(message, response)

    except anthropic.exceptions.APIError:
        await message.channel.send("申し訳ありません。APIの呼び出し中にエラーが発生しました。")
    except Exception as e:
        await message.channel.send("申し訳ありません。予期しないエラーが発生しました。")
        print(f"An error occurred: {e}")

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

    if message.content.startswith(ASK_COMMAND_EN):
        command_length = len(ASK_COMMAND_EN + ' ')
        user_input = message.content[command_length:]
        await process_command(message, ASK_COMMAND_EN, user_input)
    elif message.content.startswith(ASK_COMMAND_JA):
        command_length = len(ASK_COMMAND_JA + ' ')
        user_input = message.content[command_length:]
        await process_command(message, ASK_COMMAND_JA, user_input)

# Discord Botを実行
discord_client.run(DISCORD_BOT_TOKEN)