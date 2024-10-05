from django.urls import path, include
from api import views

urlpatterns = [
    path("register/", views.Register.as_view()),
    path("login/", views.Login.as_view()),
    path(
        "products/",
        views.ProductListViewset.as_view(),
        name="products",
    ),
    path(
        "products/<int:pk>/",
        views.ProductDetailViewset.as_view(),
        name="product-detail",
    ),
]
