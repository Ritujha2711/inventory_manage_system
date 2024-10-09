from django.urls import path
from inventory_app.views import CreateItemView, RetrieveItemView, UpdateItemView, DeleteItemView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('items/', CreateItemView.as_view(), name='create_item'),
    path('items/<int:pk>/', RetrieveItemView.as_view(), name='retrieve_item'),
    path('items/<int:pk>/update/', UpdateItemView.as_view(), name='update_item'),
    path('items/<int:pk>/delete/', DeleteItemView.as_view(), name='delete_item'),
]
