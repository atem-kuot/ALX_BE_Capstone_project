# Telegram Bot Setup

## 1. Create a Telegram Bot
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow instructions to get your bot token

## 2. Get Chat ID
1. Add your bot to a group or message it directly
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find the chat ID in the response

## 3. Set Webhook (Optional)
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-domain.com/api/alerts/telegram-webhook/"}'