from django.urls import path
from .views import (
    StockListCreateView,
    StockDetailView,
    TransactionListView,
    StockPriceView,
    InvestorStockListView,
    InvestorHoldingsView,
    BuySellStockView,
    MarketDetailView,
)


urlpatterns = [
    path("stocks/", StockListCreateView.as_view(), name="stock-list-create"),
    path("stocks/<str:pk>/", StockDetailView.as_view(), name="stock-detail"),
    path("market/", MarketDetailView.as_view(), name="market-detail"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("stocks/<str:pk>/price/", StockPriceView.as_view(), name="stock-price"),
    path("list_all_stocks/", InvestorStockListView.as_view(), name="investor-stock-list"),
    path("investor/holdings/", InvestorHoldingsView.as_view(), name="investor-holdings"),
    path("investor/buy_sell/", BuySellStockView.as_view(), name="investor-buy-sell"),
]
