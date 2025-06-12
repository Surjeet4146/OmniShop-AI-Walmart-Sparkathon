```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN', '8032821158:AAE4miR8OvLsOorO4cl-gpASYZ4C34LCA9E')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database (for future use)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # External APIs
    WALMART_API_KEY = os.getenv('WALMART_API_KEY')
    
    # File paths
    USER_DATA_FILE = "data/user_data.json"
    FEEDBACK_FILE = "data/feedback.json"
    PRODUCTS_FILE = "data/products.json"
```