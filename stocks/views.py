from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models.query import QuerySet

from .models import Stock, Transaction, Investor, Market
from .serializers import (
    StockSerializer, 
    TransactionSerializer, 
    InvestorSerializer, 
    MarketSerializer
)

from typing import List, Dict, Any

class StockListCreateView(generics.ListCreateAPIView):
    """
    API View for handling stock data including retrieval and creation.

    Methods:
    - GET: Retrieve a list of stocks along with their latest prices.
    - POST: Create a new stock entry.

    GET Parameters:
    - None

    POST Parameters:
    - 'name': str (required) - The name of the stock.
    - 'price': float (required) - The price of the stock.
    - 'quantity': float (optional) - No. of stocks units

    Permissions:
    - Requires admin privileges for both retrieving and creating stocks.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    market_serializer = MarketSerializer
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        stocks = self.get_queryset()
        serialized_stocks = self.get_serializer(stocks, many=True).data

        for stock_data in serialized_stocks:
            stock = Stock.objects.get(pk=stock_data['name'])
            if Market.objects.filter(stock=stock).exists():
                latest_price = Market.objects.filter(stock=stock).order_by('-timestamp').first().price
                stock_data['latest_price'] = latest_price
            else:
                stock_data['latest_price'] = Stock.objects.get(pk=stock_data['name']).price
        
        return Response(serialized_stocks)
    

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View to retrieve, update, or delete a specific stock entry.

    Methods:
    - GET: Retrieve details of a specific stock.
    - PUT: Update details of a specific stock.
    - DELETE: Delete a specific stock entry.

    GET Parameters:
    - None

    PUT Parameters:
    - 'name': str (optional) - The updated name of the stock.
    - 'price': float (optional) - The updated price of the stock.

    DELETE Parameters:
    - None

    Permissions:
    - Requires admin privileges for retrieving, updating, or deleting stock entries.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminUser]


class MarketDetailView(generics.ListCreateAPIView):
    """
    API View to list and create market entries.

    Methods:
    - GET: Retrieve a list of market entries.
    - POST: Create a new market entry.

    GET Parameters:
    - None

    POST Parameters:
    - 'stock': str (required) - The name of the stock associated with the market entry.
    - 'timestamp': datetime (required) - Currently not taking datetime.now() and manually adding for ease of puprose
    - 'price': float (required) - The price value for the market entry.

    Permissions:
    - Requires admin privileges for both retrieving and creating market entries.
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [IsAdminUser]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(generics.ListAPIView):
    """
    API View to retrieve a list of transactions.

    Methods:
    - GET: Retrieve a list of transactions.

    GET Parameters:
    - None

    Permissions:
    - Requires user authentication to access transaction data.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class StockPriceView(generics.RetrieveAPIView):
    """
    API View to retrieve the price details of a specific stock.

    Methods:
    - GET: Retrieve the details of a specific stock, including the latest price.

    GET Parameters:
    - None

    Permissions:
    - None (Assuming public access, adjust permissions as needed)
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve details of a specific stock including the latest price.

        Returns:
        - Serialized data of the stock with the latest_price field included if available.
        - If the stock does not exist, returns a 404 NOT FOUND response.
        """
        stock_name = self.kwargs['pk']

        try:
            stock = Stock.objects.get(pk=stock_name)
        except Stock.DoesNotExist:
            return Response({'Detail': 'Stock not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        stocks = self.queryset.get(pk=stock_name)
        serialized_stocks = self.get_serializer(stocks).data
        
        stock = Stock.objects.get(pk=stock_name)
        latest_price = Market.objects.filter(stock=stock).order_by('-timestamp').first().price
        serialized_stocks['latest_price'] = latest_price
        return Response(serialized_stocks)


class InvestorStockListView(generics.ListAPIView):
    """
    API View to retrieve a list of stocks available for investors.

    Methods:
    - GET: Retrieve a list of stocks. Optionally, filter stocks by name.

    GET Parameters:
    - 'name': str (optional) - Filter stocks by name (case insensitive).

    Permissions:
    - Requires user authentication to access the list of stocks available for investors.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')

        if name:
            stocks = queryset.filter(name__icontains=name)
        else:
            stocks = self.get_queryset()
        
        serialized_stocks = self.get_serializer(stocks, many=True).data

        for stock_data in serialized_stocks:
            stock = Stock.objects.get(pk=stock_data['name'])
            if Market.objects.filter(stock=stock).exists():
                latest_price = Market.objects.filter(stock=stock).order_by('-timestamp').first().price
                stock_data['latest_price'] = latest_price
            else:
                stock_data['latest_price'] = Stock.objects.get(pk=stock_data['name']).price
        
        return Response(serialized_stocks)


class InvestorHoldingsView(generics.ListAPIView):
    """
    API View to retrieve holdings of a specific investor.

    Methods:
    - GET: Retrieve holdings of the authenticated investor.

    GET Parameters:
    - None

    Permissions:
    - Requires authentication to retrieve holdings for the authenticated user.

    Returns:
    - List of serialized holdings for the authenticated investor.
    """
    serializer_class = InvestorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        user = self.request.user.id
        return Investor.objects.filter(name=user)


class BuySellStockView(generics.CreateAPIView):
    """
    API View to buy or sell stocks for a user.

    Methods:
    - POST: Create a transaction to buy or sell stocks.

    POST Parameters:
    - 'stock': str (required) - The name of the stock.
    - 'quantity': int (required) - The quantity of stocks to buy or sell.
    - 'transaction_type': str (required) - The type of transaction ('Buy' or 'Sell').

    Permissions:
    - Requires user authentication.

    Response Codes:
    - 201 Created: Successful buy or sell transaction.
    - 400 Bad Request: Invalid transaction type.
    - 404 Not Found: If the specified stock does not exist.
    - 406 Not Acceptable: If the requested quantity of stocks is not available for selling.
    """
    serializer_class = TransactionSerializer
    inv_serializer = InvestorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: Any) -> None:
        serializer.save(investor=self.request.user)


    def create(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        stock_name = data.get('stock')
        stock_quantity = data.get('quantity', 0)
        stock_type = data.get('transaction_type')
        available_units = Stock.objects.get(pk=stock_name).quantity

        try:
            stock = Stock.objects.get(pk=stock_name)
        except Stock.DoesNotExist:
            return Response({'detail': 'Stock not found.'}, 
                            status=status.HTTP_404_NOT_FOUND)

        try:
            investor_current_shares = Investor.objects \
                .get(name=request.user, stock=stock) \
                .purchased_shares
        except:
            Investor.objects.create(
                name = self.request.user, 
                stock = stock, 
                purchased_shares = stock_quantity)
            
            investor_current_shares = Investor.objects \
                .get(name = request.user, stock = stock) \
                .purchased_shares

        if stock_type == 'Buy':
            Stock.objects \
                .filter(pk = stock_name) \
                .update(quantity = (available_units - stock_quantity))
            
            Investor.objects \
                .filter(name = request.user, stock=stock) \
                .update(purchased_shares=investor_current_shares+stock_quantity)
            
            Transaction.objects.create(
                stock = stock, 
                investor = request.user, 
                quantity = stock_quantity, 
                transaction_type = 'Buy'
            )
            
            return Response({'detail': 'Stock bought successfully.'}, 
                            status=status.HTTP_201_CREATED)

        elif stock_type == 'Sell':   
            if stock_quantity <= available_units:
                Investor.objects \
                    .filter(name = request.user, stock = stock) \
                    .update(purchased_shares = investor_current_shares - stock_quantity)
                
                Transaction.objects.create(
                    stock = stock, 
                    investor = request.user, 
                    quantity = stock_quantity, 
                    transaction_type = 'Sell'
                )
                
                return Response({'detail': 'Stock sold successfully.'}, 
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Invalid no of stocks'}, 
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'detail': 'Invalid transaction type.'},
                             status=status.HTTP_400_BAD_REQUEST)