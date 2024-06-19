```markdown
# Discord Anthrochat Bot

このプロジェクトは、AnthropicのAPIを使用してユーザーの入力に基づいた応答を生成するDiscordボットです。このボットはPythonで構築されており、`discord.py`と`anthropic`ライブラリを利用しています。

## 機能

- AnthropicのAPIを使用してユーザーの入力に応答します。
- `$ask`と`$質問`の2つのコマンドをサポートしています。
- エラーを適切に処理し、ユーザーにわかりやすいエラーメッセージを提供します。

## 必要条件

- Python 3.9以上
- Docker（オプション）

## インストール

1. リポジトリをクローンします：
   ```
   git clone https://github.com/your-username/discord-anthrochat-bot.git
   ```

2. 必要な依存関係をインストールします：
   ```
   pip install -r requirements.txt
   ```

3. プロジェクトのルートディレクトリに`.env`ファイルを作成し、DiscordボットのトークンとAnthropicのAPIキーを追加します：
   ```
   DISCORD_BOT_TOKEN=your-discord-bot-token
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

## 使用方法

1. ボットを実行します：
   ```
   python main.py
   ```

2. ボットをDiscordサーバーに招待します。

3. 以下のコマンドを使用してボットとやり取りします：
   - `$ask <メッセージ>`：提供されたメッセージに基づいて応答を生成します。
   - `$質問 <メッセージ>`：提供されたメッセージに基づいて応答を生成します（日本語）。

## Docker

Dockerを使用してボットを実行することもできます。以下の手順に従ってください：

1. Dockerイメージをビルドします：
   ```
   docker build -t discord-anthrochat-bot .
   ```

2. Dockerコンテナを実行します：
   ```
   docker run -d --name anthrochat-bot discord-anthrochat-bot
   ```

## 貢献

contributions大歓迎です！問題を見つけたり、改善の提案がある場合は、issueを開いたりpull requestを送ったりしてください。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で提供されています。
```

```markdown
# Discord Anthrochat Bot

This is a Discord bot that uses the Anthropic API to generate responses based on user input. The bot is built using Python and utilizes the `discord.py` and `anthropic` libraries.

## Features

- Responds to user input using the Anthropic API
- Supports two commands: `$ask` and `$質問`
- Handles errors gracefully and provides user-friendly error messages

## Prerequisites

- Python 3.9 or higher
- Docker (optional)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/discord-anthrochat-bot.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Discord bot token and Anthropic API key:
   ```
   DISCORD_BOT_TOKEN=your-discord-bot-token
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

## Usage

1. Run the bot:
   ```
   python main.py
   ```

2. Invite the bot to your Discord server.

3. Use the following commands to interact with the bot:
   - `$ask <message>`: Generate a response based on the provided message.
   - `$質問 <message>`: Generate a response based on the provided message (in Japanese).

## Docker

You can also run the bot using Docker. To do so, follow these steps:

1. Build the Docker image:
   ```
   docker build -t discord-anthrochat-bot .
   ```

2. Run the Docker container:
   ```
   docker run -d --name anthrochat-bot discord-anthrochat-bot
   ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```
