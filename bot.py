import os
import telebot
from telebot import types
from datetime import datetime

# Get the token from Railway environment variable
BOT_TOKEN = os.getenv("8032821158:AAE4miR8OvLsOorO4cl-gpASYZ4C34LCA9E")
bot = telebot.TeleBot(BOT_TOKEN)

# Store user sessions (temporary, not persistent)
user_sessions = {}

# Enhanced product catalog (from your previous version)
products = [
    {
        "id": 1,
        "name": "Samsung 43-inch 4K Smart TV",
        "category": "electronics",
        "price": 299,
        "original_price": 399,
        "rating": 4.5,
        "stock": 15,
        "description": "Crystal clear 4K display with smart features"
    },
    {
        "id": 2,
        "name": "Premium Wooden Sofa Set",
        "category": "home",
        "price": 499,
        "original_price": 649,
        "rating": 4.2,
        "stock": 8,
        "description": "Comfortable 3-seater with premium wood finish"
    },
    {
        "id": 3,
        "name": "HP Pavilion 15 Gaming Laptop",
        "category": "electronics",
        "price": 599,
        "original_price": 799,
        "rating": 4.3,
        "stock": 12,
        "description": "High-performance laptop for gaming and work"
    }
]

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_sessions[user_id] = {'wishlist': [], 'awaiting_feedback': False}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛍️ Browse Categories", "🔍 Search Products")
    markup.add("🧾 View Wishlist", "📦 Orders")
    markup.add("📞 Feedback", "🎯 AR Preview")

    welcome_text = (
        "👋 Welcome to *OmniShop AI*! Your smart shopping assistant on Telegram.\n\n"
        "Use the menu below to get started ⬇️"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# /feedback command handler
@bot.message_handler(commands=['feedback'])
def feedback(message):
    user_id = message.from_user.id
    user_sessions[user_id]['awaiting_feedback'] = True
    feedback_text = "💬 **We Value Your Feedback!**\n\n"
    feedback_text += "Help us improve OmniShop AI by sharing your thoughts.\n"
    feedback_text += "Reply to this message with your feedback!"
    bot.reply_to(message, feedback_text, parse_mode='Markdown')

# /ar command handler
@bot.message_handler(commands=['ar'])
def ar_preview(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📱 View in AR", url="https://surjeet4146.github.io/OmniShop-AI-Walmart-Sparkathon/ar.html")
    )
    ar_text = "🎯 **AR Preview Available!**\n\n"
    ar_text += "Experience products in your space before buying:\n"
    ar_text += "• See how furniture fits in your room\n"
    ar_text += "• Check TV size on your wall\n"
    ar_text += "Click the button below to try it out!"
    bot.reply_to(message, ar_text, reply_markup=markup, parse_mode='Markdown')

# Handle menu selections
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Check if the message is a reply to the feedback prompt
    if message.reply_to_message and message.reply_to_message.text.startswith("💬 **We Value Your Feedback!**"):
        feedback_text = "✅ **Thank you for your feedback!**\n\n"
        feedback_text += "Your input helps us improve OmniShop AI."
        bot.reply_to(message, feedback_text, parse_mode='Markdown')
        user_sessions[user_id]['awaiting_feedback'] = False
        return

    # Check if user is providing feedback (additional check using user_sessions)
    if user_sessions.get(user_id, {}).get('awaiting_feedback', False):
        feedback_text = "✅ **Thank you for your feedback!**\n\n"
        feedback_text += "Your input helps us improve OmniShop AI."
        bot.reply_to(message, feedback_text, parse_mode='Markdown')
        user_sessions[user_id]['awaiting_feedback'] = False
        return

    # Handle menu options
    if "browse" in text:
        handle_browse(message)
    elif "search" in text:
        bot.send_message(message.chat.id, "🔍 Enter the product name to search:")
        bot.register_next_step_handler(message, handle_search)
    elif "wishlist" in text:
        wishlist = user_sessions.get(user_id, {}).get('wishlist', [])
        if wishlist:
            wishlist_text = "🧾 Your wishlist:\n" + "\n".join(f"• {item}" for item in wishlist)
        else:
            wishlist_text = "🧾 Your wishlist is empty."
        bot.send_message(message.chat.id, wishlist_text)
    elif "orders" in text:
        bot.send_message(message.chat.id, "📦 You have no orders yet.")
    elif "feedback" in text:
        feedback(message)
    elif "ar preview" in text:
        ar_preview(message)
    else:
        bot.send_message(message.chat.id, "❓ I didn't understand that. Use the menu options.")

# Browse Categories
def handle_browse(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("👕 Clothes", callback_data="cat_clothes"),
        types.InlineKeyboardButton("📱 Electronics", callback_data="cat_electronics"),
    )
    markup.add(
        types.InlineKeyboardButton("🍎 Groceries", callback_data="cat_groceries"),
        types.InlineKeyboardButton("🏠 Home", callback_data="cat_home")
    )
    bot.send_message(message.chat.id, "🛍️ Choose a category:", reply_markup=markup)

# Handle search input
def handle_search(message):
    query = message.text.strip().lower()
    user_id = message.from_user.id

    # Search products
    matched_products = []
    for product in products:
        if (query in product["name"].lower() or 
            query in product["category"].lower() or
            any(word in product["name"].lower() for word in query.split())):
            matched_products.append(product)

    if matched_products:
        product = matched_products[0]  # Take the first match
        discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
        response = f"🔍 **Found this for you:**\n\n"
        response += f"**{product['name']}**\n"
        response += f"📝 {product['description']}\n\n"
        response += f"💰 ${product['price']} ~~${product['original_price']}~~ (Save {discount:.0f}%)\n"
        response += f"⭐ {product['rating']}/5 | 📦 {product['stock']} in stock\n\n"
        response += "💎 Use code **WALMART20** for additional 20% off!"

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🛒 Add to Wishlist", callback_data=f"add_{product['name']}"),
            types.InlineKeyboardButton("🎯 View in AR", url="https://surjeet4146.github.io/OmniShop-AI-Walmart-Sparkathon/ar.html")
        )
        bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f"🤔 No products found for '{query}'. Try another search!")

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id

    if call.data.startswith("cat_"):
        category = call.data.split("_", 1)[1]
        bot.answer_callback_query(call.id, f"Selected {category.title()}")
        matched_products = [p for p in products if p['category'] == category]
        
        if matched_products:
            product = matched_products[0]
            discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
            response = f"🔎 **Top Product in {category.title()}**\n\n"
            response += f"**{product['name']}**\n"
            response += f"📝 {product['description']}\n\n"
            response += f"💰 ${product['price']} ~~${product['original_price']}~~ (Save {discount:.0f}%)\n"
            response += f"⭐ {product['rating']}/5 | 📦 {product['stock']} in stock\n\n"
            response += "💎 Use code **WALMART20** for additional 20% off!"

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("🛒 Add to Wishlist", callback_data=f"add_{product['name']}"),
                types.InlineKeyboardButton("🎯 View in AR", url="https://surjeet4146.github.io/OmniShop-AI-Walmart-Sparkathon/ar.html")
            )
            bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, f"No products found in {category.title()} category.")

    elif call.data.startswith("add_"):
        product = call.data.split("_", 1)[1]
        session = user_sessions.setdefault(user_id, {'wishlist': [], 'awaiting_feedback': False})
        if product not in session['wishlist']:
            session['wishlist'].append(product)
            bot.answer_callback_query(call.id, f"Added {product.title()} to wishlist!")
            bot.send_message(call.message.chat.id, f"✅ *{product.title()}* added to your wishlist!", parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "Already in your wishlist!")

# Keep bot running
if __name__ == "__main__":
    print("🤖 OmniShop AI is running...")
    bot.infinity_polling(timeout=60, long_polling_timeout=10)