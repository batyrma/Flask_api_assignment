from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from sqlalchemy.sql.expression import func
from sqlalchemy import text
import pandas as pd
from decimal import Decimal



fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Zz123456@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Base = db.Model
api = Api(app)
migrate = Migrate(app, db)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    male = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_category = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_name = db.Column(db.String(100), nullable=False)
    seller_city = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'), nullable=False)
    seller_raiting = db.Column(db.Integer, nullable=False)
    payment_type = db.Column(db.String(100), nullable=False)
    bonus = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sellers_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item_price = db.Column(db.Integer, nullable=False)



class CustomerResource(Resource):
    def get(self, id):
        customer = Customer.query.get_or_404(id)
        return {
            'id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'male': customer.male,
            'age': customer.age,
            'city': customer.city,
        }

    def put(self, id):
        customer = Customer.query.get_or_404(id)
        data = request.get_json()
        customer.name = data['name']
        customer.surname = data.get('surname', '')
        customer.male = data.get('male', '')
        customer.age = data.get('age', 0)
        customer.city = data.get('city', '')
        db.session.commit()
        return {'message': 'Customer data updated successfully'}

    def delete(self, id):
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Customer deleted successfully'}


class CustomerListResource(Resource):
    def get(self):
        customers = Customer.query.all()
        return [{'id': customer.id, 'name': customer.name, 'surname': customer.surname, 'male': customer.male, 'age': customer.age, 'city': customer.city} for customer in customers]

    def post(self):
        data = request.get_json()
        new_customer = Customer(name=data['name'], surname=data.get('surname', ''), male=data.get('male', ''), age=data.get('age', 0), city=data.get('city', ''))
        db.session.add(new_customer)
        db.session.commit()
        return {'message': 'User created successfully', 'id': new_customer.id}

class ItemResource(Resource):
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return {'id': item.id, 'item_name': item.item_name, 'item_category': item.item_category, 'weight': item.weight}

    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        item.item_name = data['item_name', '']
        item.item_category = data['item_category', '']
        item.weight = data.get('weight', 0)
        db.session.commit()
        return {'message': 'Item data updated successfully'}

    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully'}

class ItemListResource(Resource):
    def get(self):
        items = Item.query.all()
        return [{'id': item.id, 'item_name': item.item_name, 'item_category': item.item_category, 'weight': item.weight} for item in items]

    def post(self):
        data = request.get_json()
        new_item = Item(item_name=data['item_name', ''], item_category = data['item_category', ''], weight=data.get('weight', 0))
        db.session.add(new_item)
        db.session.commit()
        return {'message': 'Item created successfully', 'id': new_item.id}

class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)
        return {'id': order.id, 'customer_id': order.customer_id, 'item_id': order.item_id, 'seller_id': order.seller_id, 'good_id ': order.good_id, 'payment_type': order.payment_type, 'bonus ': order.bonus, 'date': order.date }

    def put(self, order_id):
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        order.customer_id = data['customer_id']
        order.item_id = data['item_id']
        order.seller_id = data['seller_id']
        order.good_id = data['good_id']
        order.seller_raiting = data['seller_raiting']
        order.payment_type = data['payment_type']
        order.bonus = data['bonus']
        order.date = data['date']

        db.session.commit()
        return {'message': 'Order data updated successfully'}

    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully'}

class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [{'id': order.id, 'customer_id': order.customer_id, 'item_id': order.item_id, 'seller_id': order.seller_id, 'good_id ': order.good_id, 'payment_type': order.payment_type, 'bonus ': order.bonus, 'date': order.date} for order in orders]

    def post(self):
        data = request.get_json()
        new_order = Order(customer_id=data['customer_id'], item_id=data['item_id'], seller_id=data['seller_id'], good_id=data['good_id'], seller_raiting=data['seller_raiting'], payment_type=data['payment_type'], bonus=data['bonus'], date=data['date'])
        db.session.add(new_order)
        db.session.commit()
        return {'message': 'Order created successfully', 'id': new_order.id}

class SellerResource(Resource):
    def get(self, seller_id):
        seller = Seller.query.get_or_404(seller_id)
        return {'id': seller.id, 'seller_name': seller.seller_name, 'seller_city': seller.seller_city}

    def put(self, seller_id):
        seller = Seller.query.get_or_404(seller_id)
        data = request.get_json()
        seller.seller_name = data['seller_name']
        seller.seller_city = data['seller_city']
        db.session.commit()
        return {'message': 'Seller data updated successfully'}

    def delete(self, seller_id):
        seller = Seller.query.get_or_404(seller_id)
        db.session.delete(seller)
        db.session.commit()
        return {'message': 'Seller deleted successfully'}

class SellerListResource(Resource):
    def get(self):
        sellers = Seller.query.all()
        return [{'id': seller.id, 'seller_name': seller.seller_name, 'seller_city': seller.seller_city} for seller in sellers]

    def post(self):
        data = request.get_json()
        new_seller = Seller(seller_name=data['seller_name'], seller_city=data['seller_city'])
        db.session.add(new_seller)
        db.session.commit()
        return {'message': 'Seller created successfully', 'id': new_seller.id}

class AnalyticsResource1(Resource):
    def get(self):
        query = text("""
        SELECT
            i.item_name,
            COUNT(o.id) AS order_count,
            COUNT(DISTINCT s.id) AS seller_count,
            COUNT(CASE WHEN c.male = 'male' THEN 1 END) AS male_order_count,
            COUNT(CASE WHEN c.male = 'female' THEN 1 END) AS female_order_count,
            (COUNT(CASE WHEN c.male = 'male' THEN 1 END)::float / COUNT(DISTINCT c.id) * 100) AS male_percentage,
            (COUNT(CASE WHEN c.male = 'female' THEN 1 END)::float / COUNT(DISTINCT c.id) * 100) AS female_percentage,
            AVG(g.item_price) AS avg_price,
            MIN(g.item_price) AS min_price,
            MAX(g.item_price) AS max_price
        FROM
            "order" o
        JOIN
            "item" i ON o.item_id = i.id
        JOIN
            "customer" c ON o.customer_id = c.id
        JOIN
            "seller" s ON o.seller_id = s.id
        JOIN 
            "good" g ON o.good_id = g.id
        GROUP BY
            i.item_name
        ORDER BY
            order_count DESC
        LIMIT 5;
        """)

        result = db.session.execute(query)

        data = [
            {
                'item_name': row[0],
                'order_count': row[1],
                'seller_count': row[2],
                'male_order_count': row[3],
                'female_order_count': row[4],
                'male_percentage': float(row[5]),
                'female_percentage': float(row[6]),
                'avg_price': float(row[7]),
                'min_price': float(row[8]),
                'max_price': float(row[9]),
            }
            for row in result
        ]

        return data



class AnalyticsListResource1(Resource):
    def get(self):
        analytics_resource = AnalyticsResource()
        analytics_data = analytics_resource.get()

        return analytics_data

class AnalyticsResource2(Resource):
    def get(self):
        query = text("""WITH AgeGroups AS (
            SELECT
                CASE
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 45 THEN '36-45'
                    WHEN age BETWEEN 46 AND 55 THEN '46-55'
                    ELSE '56+'
                END AS age_group,
                i.item_name,
                COUNT(o.id) AS purchase_count,
                ROW_NUMBER() OVER (PARTITION BY CASE WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                                   WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                                   WHEN age BETWEEN 36 AND 45 THEN '36-45'
                                                   WHEN age BETWEEN 46 AND 55 THEN '46-55'
                                                   ELSE '56+' END
                                  ORDER BY COUNT(o.id) DESC) AS item_rank
            FROM
                "customer" c
            JOIN
                "order" o ON c.id = o.customer_id
            JOIN
                "item" i ON o.item_id = i.id
            GROUP BY
                age_group, i.item_name
        )

        SELECT
            age_group,
            item_name,
            purchase_count
        FROM
            AgeGroups
        WHERE
            item_rank = 1
        ORDER BY
            age_group;


        """)


        result = db.session.execute(query)

        data = [
            {
                'age_group': row[0],
                'item_name': row[1],
                'purchase_count': row[2],
            }
            for row in result
        ]

        return data



class AnalyticsListResource2(Resource):
    def get(self):
        analytics_resource = AnalyticsResource()
        analytics_data = analytics_resource.get()

        return analytics_data


class AnalyticsResource3(Resource):
    def get(self):
        query = text("""WITH PriceCategories AS (
            SELECT
                item_name,
                CASE
                    WHEN item_price < 1500 THEN '0-1500'
                    WHEN item_price BETWEEN 1500 AND 2999 THEN '1000-2999'
                    WHEN item_price BETWEEN 3000 AND 999 THEN '3000-5999'
                    WHEN item_price BETWEEN 6000 AND 8999 THEN '6000-8999'
                    ELSE '9000+'
                END AS price_category,
                g.item_price,
                COUNT(o.id) AS sales_count
            FROM
                "item" i
            JOIN
                "order" o ON i.id = o.item_id
            JOIN 
                "good" g ON g.id = o.good_id
            GROUP BY
                i.id, item_name, price_category, item_price
        )

        SELECT
            price_category,
            AVG(item_price) AS average_price,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY item_price) AS median_price,
            SUM(sales_count) AS total_sales
        FROM
            PriceCategories
        GROUP BY
            price_category
        ORDER BY
            price_category;
        """)

        result = db.session.execute(query)

        data = [
            {
                'price_category': row[0],
                'average_price': float(row[1]),
                'median_price': float(row[2]),
                'total_sales': float(row[3]),
            }
            for row in result
        ]

        return data



class AnalyticsListResource3(Resource):
    def get(self):
        analytics_resource = AnalyticsResource()
        analytics_data = analytics_resource.get()

        return analytics_data


class AnalyticsResource4(Resource):
    def get(self):
        query = text("""WITH AgeCategories AS (
            SELECT
                c.id AS customer_id,
                CASE
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 45 THEN '36-45'
                    WHEN age BETWEEN 46 AND 55 THEN '46-55'
                    ELSE '56+'
                END AS age_category
            FROM
                "customer" c
        )

        SELECT
            age_category,
            popular_item_category,
            order_count
        FROM (
            SELECT
                ac.age_category,
                i.item_category AS popular_item_category,
                COUNT(o.id) AS order_count,
                ROW_NUMBER() OVER (PARTITION BY ac.age_category ORDER BY COUNT(o.id) DESC) AS rnk
            FROM
                "order" o
            JOIN
                AgeCategories ac ON o.customer_id = ac.customer_id
            JOIN
                "item" i ON o.item_id = i.id
            WHERE
                ac.age_category IS NOT NULL  -- Exclude "56+" category
            GROUP BY
                ac.age_category, i.item_category
        ) ranked
        WHERE
            rnk <= 3 
        ORDER BY
            age_category, rnk;
        """)


        result = db.session.execute(query)

        data = [
            {
                'age_category': row[0],
                'popular_item_category': row[1],
                'order_count': row[2],
                'total_sales': row[3],
            }
            for row in result
        ]

        return data

class AnalyticsListResource4(Resource):
    def get(self):
        analytics_resource = AnalyticsResource()
        analytics_data = analytics_resource.get()

        return analytics_data

#Анилитика Товар, кол продаж, скольско продавцов продает товар,	сколько женьщин и мужчин купили + в процентах,	средняя цена, минимальная и максимальная цена
api.add_resource(AnalyticsListResource, '/analytics/1')
#Поделен на возрастные группы и потом какой товар популярен и сколько раз его покупали
api.add_resource(AnalyticsListResource, '/analytics/2')
#Поделен на ценовые группы и средняя цена, медиана цен, количесвтво продаж
api.add_resource(AnalyticsListResource, '/analytics/3')
#Поделен на ценовые группы и средняя цена, медиана цен, количесвтво продаж
api.add_resource(AnalyticsListResource, '/analytics/4')


api.add_resource(CustomerListResource, '/customers')
api.add_resource(ItemListResource, '/items')
api.add_resource(ItemResource, '/items/<int:item_id>')
api.add_resource(OrderListResource, '/orders')
api.add_resource(OrderResource, '/orders/<int:order_id>')
api.add_resource(SellerListResource, '/sellers')
api.add_resource(SellerResource, '/sellers/<int:seller_id>')



if __name__ == '__main__':
    app.run(debug=True)