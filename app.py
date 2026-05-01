from flask import Flask, request, jsonify
import os
import logging
from datetime import datetime
from uuid import uuid4

# -----------------------------
# App Configuration
# -----------------------------
app = Flask(__name__)

# Environment variables
APP_NAME = os.getenv("APP_NAME", "My Production Python App")
ENV = os.getenv("ENV", "development")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------------
# In-Memory Database (Demo)
# -----------------------------
products = []
orders = []

# -----------------------------
# Utility Functions
# -----------------------------
def generate_id():
    return str(uuid4())

def current_time():
    return datetime.utcnow().isoformat()

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def home():
    return jsonify({
        "message": f"Welcome to {APP_NAME} 🚀",
        "environment": ENV
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "UP",
        "timestamp": current_time()
    })

# -----------------------------
# Product APIs
# -----------------------------

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid input"}), 400

    product = {
        "id": generate_id(),
        "name": data["name"],
        "price": data["price"],
        "created_at": current_time()
    }

    products.append(product)
    logging.info(f"Product added: {product}")

    return jsonify(product), 201

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]

    logging.info(f"Product deleted: {product_id}")
    return jsonify({"message": "Product deleted"})

# -----------------------------
# Order APIs
# -----------------------------

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    if not data or "product_id" not in data:
        return jsonify({"error": "Invalid input"}), 400

    product = next((p for p in products if p["id"] == data["product_id"]), None)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    order = {
        "id": generate_id(),
        "product": product,
        "created_at": current_time()
    }

    orders.append(order)
    logging.info(f"Order created: {order}")

    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

# -----------------------------
# Error Handling
# -----------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server Error: {str(e)}")
    return jsonify({"error": "Internal Server Error"}), 500

# -----------------------------
# Main Entry
# -----------------------------
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
