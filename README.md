# 🛍️ OmniShop AI - Walmart Sparkathon

An intelligent Telegram shopping bot that provides personalized product recommendations, AR previews, and seamless shopping experience.

## 🌟 Features

- **Personalized Recommendations**: AI-powered product suggestions based on user preferences
- **AR Product Preview**: View products in your space before buying
- **Smart Search**: Natural language product search with fuzzy matching
- **Wishlist Management**: Save and manage favorite products
- **Real-time Analytics**: User shopping insights and platform statistics
- **Multi-category Support**: Electronics, Furniture, and more

## 🚀 Demo

- **Live Bot**: [@OmniShopAI_bot](https://t.me/your_bot_username)
- **AR Preview**: [View AR Demo](https://surjeet4146.github.io/OmniShop-AI-Walmart-Sparkathon/ar.html)

## 📱 Screenshots

![Bot Interface](assets/screenshots/bot-interface.png)
![AR Preview](assets/screenshots/ar-preview.png)
![Product Search](assets/screenshots/product-search.png)

## 🛠️ Technology Stack

- **Backend**: Python, pyTelegramBotAPI
- **Frontend**: HTML5, CSS3, JavaScript (AR.js)
- **Database**: JSON (SQLite/PostgreSQL ready)
- **Deployment**: Railway/Heroku/VPS
- **AR Technology**: AR.js, A-Frame

## 📦 Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/surjeet4146/OmniShop-AI-Walmart-Sparkathon.git
cd OmniShop-AI-Walmart-Sparkathon
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your bot token
```

5. Run the bot:
```bash
python bot.py
```

### Production Deployment

#### Option 1: Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/surjeet4146/OmniShop-AI-Walmart-Sparkathon)

#### Option 2: Heroku
```bash
heroku create omnishop-ai-bot
heroku config:set BOT_TOKEN=your_bot_token
git push heroku main
```

#### Option 3: VPS/Docker
```bash
docker-compose up -d
```

## 🎯 Usage

### Basic Commands
- `/start` - Welcome message and main menu
- `/help` - List all available commands
- `/categories` - Browse product categories
- `/wishlist` - View saved products
- `/ar` - Access AR preview
- `/analytics` - View shopping statistics
- `/feedback` - Share feedback

### Search Features
- Type product names: "TV", "laptop", "sofa"
- Natural language queries: "gaming laptop under $600"
- Category browsing with filters

## 🏗️ Architecture

```
User → Telegram → Bot Server → Product Database
                      ↓
              AR.js Web Interface
```

## 🔧 Configuration

### Environment Variables
```bash
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://your-app.railway.app/webhook
DEBUG=false
WALMART_API_KEY=your_walmart_api_key
```

### Bot Settings
- **Inline Mode**: Enabled
- **Group Privacy**: Disabled
- **Allow Groups**: True

## 📊 Analytics & Monitoring

- User engagement metrics
- Product search analytics
- Wishlist conversion rates
- AR preview usage statistics

## 🧪 Testing

Run tests:
```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Surjeet** - [@surjeet4146](https://github.com/surjeet4146)

## 🏆 Acknowledgments

- Walmart Sparkathon 2024
- Telegram Bot API
- AR.js Community
- Open Source Contributors

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/surjeet4146/OmniShop-AI-Walmart-Sparkathon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/surjeet4146/OmniShop-AI-Walmart-Sparkathon/discussions)
- **Email**: your.email@example.com

---

⭐ **Star this repository if you found it helpful!**