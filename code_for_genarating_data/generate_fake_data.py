from faker import Faker
from sqlalchemy.sql import func
import csv

fake = Faker()

# Lists to store fake data
customers_data = []
items_data = []
sellers_data = []
goods_data = []
orders_data = []

# Define the item categories and their associated products
item_categories = {
    'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Headphones', 'TV', 'Camera', 'Portable charger', 'Gaming console', 'Printer', 'Mouse', 'Keyboard', 'VR headset', 'Battery', 'USB cable', 'Computer speakers', 'Monitor', 'Camera', 'Router', 'External hard drive'],
    'Clothing': ['T-shirt', 'Jeans', 'Jacket', 'Dress', 'Sweater', 'Pants', 'Shirt', 'Hoodie', 'Skirt', 'Blazer', 'Shorts', 'Blouse', 'Hat', 'Coat', 'Underwear', 'Socks', 'Tie', 'Suit', 'Glasses', 'Sportswear'],
    'Beauty and Health': ['Shampoo', 'Face cream', 'Perfume', 'Toothbrush', 'Toothpaste', 'Shower gel', 'Face mask', 'Cleansing oil', 'Cosmetics', 'Razor', 'Deodorant', 'Massager', 'Vitamins', 'Antiseptic', 'Lipstick', 'Sunscreen', 'Body lotion', 'Anti-aging products', 'Hygienic pads', 'Electric toothbrush'],
    'Chemistry': ['Soap', 'Cleaning agent', 'Dishwashing shampoo', 'Floor cleaner', 'Laundry detergent', 'Cleansing powder', 'Dish sponges', 'Window cleaning solution', 'Insect repellent', 'Disinfectant spray', 'Dishwashing liquid', 'Antiseptic gel', 'Stain remover', 'Special dye', 'Air freshener', 'Mold remover', 'Special dishwashing solution', 'Pipe cleaning acid', 'Wet wipes', 'Mosquito aerosol'],
    'Food and Beverages': ['Bread', 'Milk', 'Eggs', 'Vegetable oil', 'Rice', 'Pasta', 'Sugar', 'Coffee', 'Tea', 'Fruits', 'Vegetables', 'Meat', 'Fish', 'Cheese', 'Yogurt', 'Juice', 'Water', 'Canned goods', 'Greens', 'Dessert']
}

count_id = 1
# Generating fake data for items
for category, products in item_categories.items():
    for product in products:
        new_item = {
            'id': count_id,  # Adding 'id' key with a unique identifier
            'item_name': product,
            'item_category': category,
            'weight': fake.random_int(min=100, max=1000)
        }
        items_data.append(new_item)
        count_id += 1

# Generating fake data for sellers
for seller_id in range(1, 201):
    random_item = fake.random_element(elements=items_data)
    new_seller = {
        'id': seller_id,
        'seller_name': fake.company(),
        'seller_city': fake.city(),
        'item_id': random_item['id']  # Assuming 'id' is the key for items
    }
    sellers_data.append(new_seller)

# Generating fake data for goods
for good_id in range(1, 201):
    random_seller = fake.random_element(elements=sellers_data)
    random_item = fake.random_element(elements=items_data)
    new_good = {
        'id': good_id,
        'sellers_id': random_seller['id'],
        'item_id': random_item['id'],
        'item_price': fake.random_int(min=999, max=9999),
    }
    goods_data.append(new_good)

# Generating fake data for customers
for customer_id in range(1, 1001):
    gender = fake.random_element(elements=('male', 'female'))
    if gender == "male":
        new_customer = {
            'id': customer_id,
            'name': fake.first_name_male(),
            'surname': fake.last_name(),
            'male': gender,
            'age': fake.random_int(min=18, max=80),
            'city': fake.city(),
        }
        customers_data.append(new_customer)
    else:
        new_customer = {
            'id': customer_id,
            'name': fake.first_name_female(),
            'surname': fake.last_name(),
            'male': gender,
            'age': fake.random_int(min=18, max=80),
            'city': fake.city(),
        }
        customers_data.append(new_customer)

# Generating fake data for orders
for order_id in range(1, 5001):
    random_customer = fake.random_element(elements=customers_data)
    random_seller = fake.random_element(elements=sellers_data)
    random_item = fake.random_element(elements=items_data)
    random_good = fake.random_element(elements=goods_data)

    payment_types = ['cash payment', 'cashless payment', 'in installments']

    new_order = {
        'id': order_id,
        'customer_id': random_customer['id'],
        'item_id': random_item['id'],
        'seller_id': random_seller['id'],
        'good_id': random_good['id'],
        'seller_raiting': fake.random_int(min=1, max=5),
        'payment_type': fake.random_element(elements=payment_types),
        'bonus': fake.random_int(min=0, max=50),
        'date': fake.date_this_month(),
    }
    orders_data.append(new_order)

# Save data to CSV files
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

save_to_csv(customers_data, 'customers.csv')
save_to_csv(items_data, 'items.csv')
save_to_csv(sellers_data, 'sellers.csv')
save_to_csv(goods_data, 'goods.csv')
save_to_csv(orders_data, 'orders.csv')
