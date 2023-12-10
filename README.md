# StockBrokerProject

This project is a Stock Broker system that allows users to buy and sell stocks.

### 1. Installation
To set up the project locally, follow these steps:

Clone the repository:
```bash
git clone https://github.com/yourusername/stocker-broker.git
```
### 2. Install dependencies:
```bash
pip install -r requirements.txt
```
### 3. Running the server
To run the development server, execute:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
This will start the server at http://localhost:8000/
### 4. Creating users
After verifying that the server is up and running Either stop or open another terminal session to create a superuser and other normal users, who can act as admin and investors.
```bash
python manage.py createsuperuser --username admin --email admin@example.com
```
Use the interface provided by Django for creating normal users(Investors) with 'is_staff'=False
### 5. REST API Endpoints
### Note: Add Basic Auth to all the requests.
#### 1. ```/api/stocks/ (GET, POST)```
Description: List all stocks and create a new stock entry.

Parameters: 
name: str (required) - The name of the stock.
  price: float (required) - The price of the stock.
  quantity: float (optional) - Number of stock units.
```bash
POST: Request body
{
    "name": "Microsoft",
    "price": 1500.00
}
```

#### 2.```/api/stocks/<str:pk>/ (GET, PUT, DELETE)```

Description: Retrieve, update, or delete a specific stock.
```bash 
http://127.0.0.1:8000/api/stocks/Microsoft/
```

#### 3.```/api/market/ (GET, POST)```

Description: List all market entries and create a new market entry.
Parameters: 
stock: name (required) - The ID of the stock associated with the market entry.
price: float (required) - The price value for the market entry.

#### 4.```/api/transactions/ (POST)```

Description: Buy or sell stocks for a user.
Parameters:
stock: int (required) - The ID of the stock.
quantity: int (optional) - The quantity of stocks to buy or sell.
transaction_type: str (required) - The type of transaction ('Buy' or 'Sell').

#### 5.```/api/stocks/<str:pk>/price/ (GET)```

Description: Retrieve the price of a specific stock.

#### 6.```/api/list_all_stocks/ (GET)```

Description: List all stocks owned by an investor. Filter provided by "name" 

#### 7.```/api/investor/holdings/ (GET)```

Description: Retrieve the holdings of an investor.

#### 8.```/api/investor/buy_sell/ (POST)```
Description: Perform buy or sell actions for an investor.
```bash
POST: Request body
{
    "transaction_type": "Buy",
    "quantity": 100,
    "stock": "Microsoft"
}
```



