# Vendor Management System

The Vendor Management System is a Django-based web application designed to manage vendors, purchase orders, and historical performance data.

## Features

Vendor Management: Add, update, and delete vendor information including name, contact details, address, and vendor code.
Purchase Order Management: Create, edit, and delete purchase orders with details such as PO number, order date, delivery date, items, quantity, status, quality rating, issue date, and acknowledgment date.
Performance Metrics: Calculate and store vendor performance metrics including on-time delivery rate, quality rating average, average response time, and fulfillment rate.
API Endpoints: Expose RESTful APIs for CRUD operations on vendors, purchase orders, and historical performance data.

## Installation
### 1. Clone the repository:
git clone <https://github.com/piyushmendhe70/DjangoProject>
### 2. pip install:
pip install django
pip install django_rest_framework

### 3.Run migrations:
python manage.py migrate

### 4. Create a Superuser:
python manage.py createsuperuser

### 5. Start the developement server:
python manage.py runserver

### 6.Access the application at http://localhost:8000/

## Usage
Navigate to the homepage and explore the available functionalities.
Use the provided APIs to interact with the system programmatically.
Customize and extend the application as per your requirements.

## API Endpoints
Vendors: /api/Vendor/
Purchase Orders: /api/PurchaseOrder/
Historical Performances: /api/HistoricalPerformance/
Vendor Performance Metrics: /api/vendor-performance/<vendor_id>/performance/

## Contributing
Contributions are welcome! Please follow the guidelines outlined in CONTRIBUTING.md.

