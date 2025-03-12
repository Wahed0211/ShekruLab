from django.urls import path
from .views import SubView, HomeView, CreateOrderView, VerifyPaymentView, UserView

urlpatterns = [
    path('', SubView.as_view(), name='sub'),
    path('user/', UserView.as_view(), name='user'),
    path('home/', HomeView.as_view(), name='home'),
    path('create-order/<str:plan>/', CreateOrderView.as_view(), name='create_order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify_payment'),
]
