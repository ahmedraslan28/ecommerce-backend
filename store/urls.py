from django.urls import path
from .views import (ProductList, ProductDetail, CollectionList,
                    CollectionDetail, ProductReviewList, ProductReviewDetail)
urlpatterns = [
    path('products/', ProductList.as_view(), name="product-list"),
    path('products/<int:pk>/', ProductDetail.as_view(), name="product-detail"),

    path('collections/', CollectionList.as_view(), name="collection-list"),
    path('collections/<int:pk>/', CollectionDetail.as_view(),
         name="collection-detail"),

    path('products/<int:pk>/reviews/',
         ProductReviewList.as_view(), name="product-review-list"),
    path('products/<int:pk>/reviews/<int:review_pk>/',
         ProductReviewDetail.as_view(), name="product-review-detail"),
]
