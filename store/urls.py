from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name="product-list"),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name="product-detail"),
    path('products/<int:pk>/reviews/',
         views.ProductReviewList.as_view(), name="product-review-list"),
    path('products/<int:product_id>/reviews/<int:pk>/',
         views.ProductReviewDetail.as_view(), name="product-review-detail"),
    path('products/<int:pk>/images/', views.ProductImagesList.as_view(),
         name="product-images-list"),
    path('products/<int:product_pk>/images/<int:pk>/', views.ProductImageDetail.as_view(),
         name="product-images-detail"),

    path('collections/', views.CollectionList.as_view(), name="collection-list"),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(),
         name="collection-detail"),

    path('cart/', views.CartCreate.as_view(), name="cart-create"),
    path('cart/<str:pk>/', views.CartRetrieve.as_view(), name="cart-detail"),

    path('cart/<str:pk>/items/', views.CartItemsList.as_view(), name='cartitem-list'),
    path('cart/<str:cart_id>/items/<int:pk>',
         views.CartItemDetail.as_view(), name='cartitem-detail'),

    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/me', views.UserProfile.as_view(), name='user-profile'),

    path('customers/', views.CustomerList.as_view(), name='customer-create'),
    path('customers/<int:pk>/', views.CustomerDetail.as_view(),
         name='customer-detail'),
    path('customers/me/', views.CustomerProfile.as_view(),
         name='customer-profile'),

    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', views.UserRegister.as_view(), name='user_register'),
    path('auth/reset-password/',
         views.PasswordReset.as_view(), name='password_reset'),
    path('auth/reset-password/<uidb64>/<token>/', views.PasswordResetConfirmation.as_view(),
         name='password_reset-confirmation'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
