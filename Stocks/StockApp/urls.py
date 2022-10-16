from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('userlogin/', views.userlogin),
    path('adminhome/', views.adminhome),
    path('userhome/', views.userhome),
    path('userregister/', views.userregister),
    path('profile/',views.profile),
    path('updateprofile/',views.updateprofile),
    path('logout/', views.logout_req),
    path('user_details/', views.user_details),
    path('delete/<str:pk>/', views.delete),
    path('stocks/', views.stocks),
    path('addStock/', views.addStock),
    path('deleteStock/<int:pk>/', views.deleteStock),
    path('stockData/<int:pk>/', views.stockData),
    path('addStockData/<int:pk>/', views.addStockData),
    path('buyStocks/', views.buyStocks),
    path('viewStocksData/<int:pk>/', views.viewStocksData),
    path('userStocks/', views.userStocks),
    path('buy/<int:pk>/', views.buy),
]