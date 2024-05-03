from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Create Flask application instance
app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product(title='{self.title}', price={self.price})"

# Define routes for API endpoints
@app.route('/products', methods=['GET'])
def get_products():
    # Retrieve all products from the database
    products = Product.query.all()
    # Convert products to JSON format and return
    return jsonify([{'id': product.id, 'title': product.title, 'price': product.price} for product in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    # Retrieve a specific product by its ID from the database
    product = Product.query.get_or_404(id)
    # Convert product to JSON format and return
    return jsonify({'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price})

@app.route('/products', methods=['POST'])
def create_product():
    # Extract product data from JSON request
    data = request.get_json()
    # Create a new product instance
    product = Product(title=data['title'], description=data['description'], price=data['price'])
    # Add product to the database session
    db.session.add(product)
    # Commit changes to the database
    db.session.commit()
    # Return success message
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    # Retrieve product by its ID from the database
    product = Product.query.get_or_404(id)
    # Extract updated product data from JSON request
    data = request.get_json()
    # Update product attributes if provided, otherwise keep existing values
    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    # Commit changes to the database
    db.session.commit()
    # Return success message
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    # Retrieve product by its ID from the database
    product = Product.query.get_or_404(id)
    # Delete product from the database session
    db.session.delete(product)
    # Commit changes to the database
    db.session.commit()
    # Return success message
    return jsonify({'message': 'Product deleted successfully'})

# Entry point for running the Flask application
if __name__ == '__main__':
    # Create database tables based on defined models
    db.create_all()
    # Run the Flask application in debug mode
    app.run(debug=True)
