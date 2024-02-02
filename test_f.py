import random

# Генерация товаров в различных категориях
food_adjectives = ["Fresh", "Organic", "Delicious", "Tasty", "Healthy"]
food_nouns = ["Apples", "Bananas", "Bread", "Cheese", "Tomatoes"]
food_products = [f"{random.choice(food_adjectives)} {random.choice(food_nouns)}" for _ in range(100)]

electronics_adjectives = ["Smart", "High-Tech", "Innovative", "Sleek", "Advanced"]
electronics_nouns = ["Laptops", "Smartphones", "Headphones", "Cameras", "Smartwatches"]
electronics_products = [f"{random.choice(electronics_adjectives)} {random.choice(electronics_nouns)}" for _ in range(100)]

clothing_adjectives = ["Stylish", "Comfortable", "Fashionable", "Trendy", "Cozy"]
clothing_nouns = ["T-Shirts", "Jeans", "Dresses", "Sweaters", "Shoes"]
clothing_products = [f"{random.choice(clothing_adjectives)} {random.choice(clothing_nouns)}" for _ in range(100)]

books_authors = ["John Smith", "Emily Johnson", "Michael Davis", "Jessica Wilson", "Christopher Miller"]
books_titles = ["The Adventure Begins", "Mystery of the Lost Key", "Through the Eyes of Time", "Echoes in the Wind", "Journey to the Unknown"]
books_products = [f"{random.choice(books_authors)} - {random.choice(books_titles)}" for _ in range(100)]

# Вывод первых 5 товаров из каждой категории в качестве примера
print("Food Products:", food_products[:5])
print("\nElectronics Products:", electronics_products[:5])
print("\nClothing Products:", clothing_products[:5])
print("\nBooks Products:", books_products[:5])
