from django.urls import path, include

from . import views

urlpatterns = [
    path('orders/', views.OrderView.as_view()),
    path('orders/create/', views.OrderView.as_view()),
    path('orders/<int:pk>/update/', views.OrderView.as_view()),

    path('visits/', views.VisitView.as_view()),
    path('visits/create/', views.VisitView.as_view()),

    path('stores/', views.StoreView.as_view())
]
