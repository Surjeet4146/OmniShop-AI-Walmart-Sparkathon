import telebot
import time
import json
import os
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot token
BOT_TOKEN = "8032821158:AAE4miR8OvLsOorO4cl-gpASYZ4C34LCA9E"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# File for user data persistence
USER_DATA_FILE = "user_data.json"

# User session management (e.g., for feedback)
user_sessions = {}

# Load user data from JSON file
def load_user_data():
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading user data: {e}")
    
    return {
        "default_user": {
            "preferences": ["furniture"],
            "purchase_history": ["Sofa"],
            "wishlist": [],
            "created_at": datetime.now().isoformat()
        }
    }

# Save user data to JSON file
def save_user_data(user_data):
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(user_data, f, indent=2)
    except Exception as e:
        print(f"Error saving user data: {e}")

# Load initial user data
user_data = load_user_data()

# Enhanced product catalog
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
        "category": "furniture",
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

# Get or create user profile
def get_user_profile(user_id):
    user_id = str(user_id)
    if user_id not in user_data:
        user_data[user_id] = {
            "preferences": [],
            "purchase_history": [],
            "wishlist": [],
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat()
        }
        save_user_data(user_data)
    
    user_data[user_id]["last_active"] = datetime.now().isoformat()
    return user_data[user_id]

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    user_profile = get_user_profile(user_id)
    
    welcome_text = f"🛍️ Welcome to OmniShop AI, {message.from_user.first_name}!\n\n"
    if len(user_profile["purchase_history"]) == 0:
        welcome_text += "🎉 First time here? Let's get you started!\n\n"
    else:
        welcome_text += "👋 Welcome back! Ready to discover amazing deals?\n\n"
    
    welcome_text += "What can I help you find today?\n"
    welcome_text += "• Electronics 📱\n• Furniture 🛋️\n\n"
    welcome_text += "Use /help to see all available commands!"
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔍 Browse Products", callback_data="browse_products"),
        InlineKeyboardButton("❤️ My Wishlist", callback_data="view_wishlist")
    )
    markup.row(
        InlineKeyboardButton("📊 Categories", callback_data="show_categories"),
        InlineKeyboardButton("🎯 AR Preview", callback_data="ar_preview")
    )
    
    try:
        with open("welcome.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=markup)
    except Exception as e:
        print(f"Error in start command: {e}")
        bot.reply_to(message, welcome_text, reply_markup=markup)

# Help command
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🤖 **OmniShop AI Commands**

**Main Commands:**
/start - Get started with OmniShop AI
/help - Show this help message
/categories - Browse product categories

**Shopping Features:**
/wishlist - View your wishlist
/ar - AR product preview
/analytics - View shopping analytics

**Support:**
/feedback - Share your feedback

**How to Shop:**
• Type product names (e.g., "TV", "laptop", "sofa")
• Browse by category
• Add items to wishlist
• Get personalized recommendations

**Special Offers:**
Use code **WALMART20** for 20% off your purchase! 🎉
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

# AR preview command
@bot.message_handler(commands=['ar'])
def ar_preview(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📱 View in AR", url="https://surjeet4146.github.io/OmniShop-AI-Walmart-Sparkathon/ar.html")
    )
    
    ar_text = "🎯 **AR Preview Available!**\n\n"
    ar_text += "Experience products in your space before buying:\n"
    ar_text += "• See how furniture fits in your room\n"
    ar_text += "• Check TV size on your wall\n"
    ar_text += "Click the button below to try it out!"
    bot.reply_to(message, ar_text, reply_markup=markup, parse_mode='Markdown')

# Analytics command
@bot.message_handler(commands=['analytics'])
def analytics(message):
    user_id = str(message.from_user.id)
    user_profile = get_user_profile(user_id)
    
    analytics_text = f"📊 **Your Shopping Analytics**\n\n"
    analytics_text += f"🛒 Total Purchases: {len(user_profile['purchase_history'])}\n"
    analytics_text += f"❤️ Wishlist Items: {len(user_profile['wishlist'])}\n"
    analytics_text += f"📅 Member Since: {user_profile['created_at'][:10]}\n\n"
    
    if user_profile['preferences']:
        analytics_text += f"🎯 Favorite Categories: {', '.join(user_profile['preferences'])}\n\n"
    
    analytics_text += "📈 Platform Stats:\n"
    analytics_text += f"• Total Users: {len(user_data)}\n"
    analytics_text += f"• Products Available: {len(products)}\n"
    analytics_text += "• Average Rating: 4.3/5 ⭐"
    bot.reply_to(message, analytics_text, parse_mode='Markdown')

# Feedback command (combined approach)
@bot.message_handler(commands=['feedback'])
def feedback(message):
    print(f"Feedback command triggered by user {message.from_user.id}")  # Debug
    feedback_text = "💬 **We Value Your Feedback!**\n\n"
    feedback_text += "Help us improve OmniShop AI by sharing your thoughts.\n"
    feedback_text += "Reply to this message with your feedback!"
    
    user_sessions[str(message.from_user.id)] = {"awaiting_feedback": True}
    bot.reply_to(message, feedback_text, parse_mode='Markdown')

# Wishlist command
@bot.message_handler(commands=['wishlist'])
def wishlist(message):
    user_id = str(message.from_user.id)
    user_profile = get_user_profile(user_id)
    
    if not user_profile['wishlist']:
        wishlist_text = "❤️ Your wishlist is empty!\n\n"
        wishlist_text += "Start adding products by typing their names or browsing categories."
        bot.reply_to(message, wishlist_text)
        return
    
    wishlist_text = "❤️ **Your Wishlist**\n\n"
    for item_id in user_profile['wishlist']:
        product = next((p for p in products if p['id'] == item_id), None)
        if product:
            discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
            wishlist_text += f"• {product['name']}\n"
            wishlist_text += f"  💰 ${product['price']} (Save {discount:.0f}%)\n"
            wishlist_text += f"  ⭐ {product['rating']}/5\n\n"
    
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🗑️ Clear Wishlist", callback_data="clear_wishlist"))
    bot.reply_to(message, wishlist_text, reply_markup=markup, parse_mode='Markdown')

# Categories command
@bot.message_handler(commands=['categories'])
def categories(message):
    categories_dict = {}
    for product in products:
        category = product['category']
        if category not in categories_dict:
            categories_dict[category] = []
        categories_dict[category].append(product)
    
    category_text = "📂 **Product Categories**\n\n"
    for category, cat_products in categories_dict.items():
        category_text += f"**{category.title()}** ({len(cat_products)} items)\n"
        for product in cat_products[:2]:
            category_text += f"• {product['name']} - ${product['price']}\n"
        if len(cat_products) > 2:
            category_text += f"• ... and {len(cat_products) - 2} more\n"
        category_text += "\n"
    
    markup = InlineKeyboardMarkup()
    for category in categories_dict.keys():
        markup.row(InlineKeyboardButton(f"🔍 Browse {category.title()}", callback_data=f"browse_{category}"))
    bot.reply_to(message, category_text, reply_markup=markup, parse_mode='Markdown')

# Callback query handler for inline buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "browse_products" or call.data == "show_categories":
            categories(call.message)
        elif call.data == "view_wishlist":
            wishlist(call.message)
        elif call.data == "ar_preview":
            ar_preview(call.message)
        elif call.data.startswith("browse_"):
            category = call.data.replace("browse_", "")
            browse_category(call.message, category)
        elif call.data.startswith("add_wishlist_"):
            product_id = int(call.data.replace("add_wishlist_", ""))
            add_to_wishlist(call.message, product_id)
        elif call.data.startswith("product_"):
            product_id = int(call.data.replace("product_", ""))
            show_product_details(call.message, product_id)
        elif call.data == "clear_wishlist":
            user_id = str(call.message.chat.id)
            user_profile = get_user_profile(user_id)
            user_profile['wishlist'] = []
            save_user_data(user_data)
            bot.edit_message_text("❤️ Wishlist cleared!", call.message.chat.id, call.message.message_id)
        
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error handling callback: {e}")
        bot.answer_callback_query(call.id, "Something went wrong!")

# Browse products by category
def browse_category(message, category):
    category_products = [p for p in products if p['category'] == category]
    
    if not category_products:
        bot.reply_to(message, f"No products found in {category} category.")
        return
    
    response_text = f"🔍 **{category.title()} Products**\n\n"
    markup = InlineKeyboardMarkup()
    
    for product in category_products:
        discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
        response_text += f"**{product['name']}**\n"
        response_text += f"💰 ${product['price']} ~~${product['original_price']}~~ (Save {discount:.0f}%)\n"
        response_text += f"⭐ {product['rating']}/5 | 📦 {product['stock']} in stock\n\n"
        
        markup.row(
            InlineKeyboardButton(f"👀 View {product['name'][:20]}...", callback_data=f"product_{product['id']}"),
            InlineKeyboardButton("❤️ Add to Wishlist", callback_data=f"add_wishlist_{product['id']}")
        )
    
    bot.edit_message_text(response_text, message.chat.id, message.message_id, reply_markup=markup, parse_mode='Markdown')

# Show product details
def show_product_details(message, product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        bot.reply_to(message, "Product not found.")
        return
    
    discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
    
    details_text = f"🛍️ **{product['name']}**\n\n"
    details_text += f"📝 {product['description']}\n\n"
    details_text += f"💰 **Price:** ${product['price']} ~~${product['original_price']}~~\n"
    details_text += f"💸 **You Save:** {discount:.0f}% (${product['original_price'] - product['price']})\n"
    details_text += f"⭐ **Rating:** {product['rating']}/5\n"
    details_text += f"📦 **Stock:** {product['stock']} available\n"
    details_text += f"🏷️ **Category:** {product['category'].title()}\n\n"
    details_text += "💎 **Special Offer:** Use code WALMART20 for additional 20% off!"
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("❤️ Add to Wishlist", callback_data=f"add_wishlist_{product_id}"),
        InlineKeyboardButton("🎯 View in AR", callback_data="ar_preview")
    )
    markup.row(InlineKeyboardButton("🔙 Back to Category", callback_data=f"browse_{product['category']}"))
    
    bot.edit_message_text(details_text, message.chat.id, message.message_id, reply_markup=markup, parse_mode='Markdown')

# Add product to wishlist
def add_to_wishlist(message, product_id):
    user_id = str(message.chat.id)
    user_profile = get_user_profile(user_id)
    
    if product_id not in user_profile['wishlist']:
        user_profile['wishlist'].append(product_id)
        save_user_data(user_data)
        
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            bot.answer_callback_query(message.message_id, f"❤️ {product['name']} added to your wishlist!")
    else:
        bot.answer_callback_query(message.message_id, "This item is already in your wishlist!")

# Handle text messages (queries and feedback replies)
@bot.message_handler(content_types=['text'])
def handle_message(message):
    user_id = str(message.from_user.id)
    
    # Check if the message is a reply to the feedback prompt
    if message.reply_to_message and message.reply_to_message.text.startswith("💬 **We Value Your Feedback!**"):
        feedback_text = "✅ **Thank you for your feedback!**\n\n"
        feedback_text += "Your input helps us improve OmniShop AI."
        bot.reply_to(message, feedback_text, parse_mode='Markdown')
        if user_id in user_sessions:
            del user_sessions[user_id]
        return
    
    # Check if user is providing feedback (additional check using user_sessions)
    if user_id in user_sessions and user_sessions[user_id].get("awaiting_feedback"):
        feedback_text = "✅ **Thank you for your feedback!**\n\n"
        feedback_text += "Your input helps us improve OmniShop AI."
        bot.reply_to(message, feedback_text, parse_mode='Markdown')
        del user_sessions[user_id]
        return
    
    # Handle regular queries
    user_profile = get_user_profile(user_id)
    query = message.text.lower().strip()
    
    # Product matching
    matched_products = []
    for product in products:
        if (query in product["name"].lower() or 
            query in product["category"].lower() or
            any(word in product["name"].lower() for word in query.split())):
            matched_products.append(product)
    
    if matched_products:
        if len(matched_products) == 1:
            product = matched_products[0]
            discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
            
            if user_profile.get('preferences') and product['category'] in user_profile['preferences']:
                response = f"🎯 **Perfect match for you!** (Based on your {product['category']} preference)\n\n"
            else:
                response = f"🔍 **Found this for you:**\n\n"
            
            response += f"**{product['name']}**\n"
            response += f"📝 {product['description']}\n\n"
            response += f"💰 ${product['price']} ~~${product['original_price']}~~ (Save {discount:.0f}%)\n"
            response += f"⭐ {product['rating']}/5 | 📦 {product['stock']} in stock\n\n"
            response += "💎 Use code **WALMART20** for additional 20% off!"
            
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton("❤️ Add to Wishlist", callback_data=f"add_wishlist_{product['id']}"),
                InlineKeyboardButton("🎯 View in AR", callback_data="ar_preview")
            )
            bot.reply_to(message, response, reply_markup=markup, parse_mode='Markdown')
        else:
            response = f"🔍 **Found {len(matched_products)} products:**\n\n"
            markup = InlineKeyboardMarkup()
            
            for product in matched_products[:5]:
                discount = ((product['original_price'] - product['price']) / product['original_price']) * 100
                response += f"• **{product['name']}** - ${product['price']} (Save {discount:.0f}%)\n"
                
                markup.row(
                    InlineKeyboardButton(f"👀 {product['name'][:20]}...", callback_data=f"product_{product['id']}"),
                    InlineKeyboardButton("❤️", callback_data=f"add_wishlist_{product['id']}")
                )
            
            bot.reply_to(message, response, reply_markup=markup, parse_mode='Markdown')
    else:
        response = f"🤔 No exact matches found for '{query}'\n\n"
        response += "**Try searching for:**\n"
        response += "• Electronics\n• Furniture\n\n"
        response += "**Popular products:**\n"
        for product in sorted(products, key=lambda x: x['rating'], reverse=True)[:2]:
            response += f"• {product['name']} ⭐{product['rating']}\n"
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("📂 Browse Categories", callback_data="show_categories"),
            InlineKeyboardButton("🎯 AR Preview", callback_data="ar_preview")
        )
        bot.reply_to(message, response, reply_markup=markup, parse_mode='Markdown')

# Run the bot
print("Starting OmniShop AI Bot... (Final Version with Feedback Fix)")
while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        print(f"Bot error: {e}")
        time.sleep(10)
        print("Restarting bot...")