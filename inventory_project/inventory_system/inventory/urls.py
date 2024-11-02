from django.urls import path
from .views import CreateItemView, ReadItemView

urlpatterns = [
    path('item/', CreateItemView.as_view(), name='create_item'),  # Ensure this name is set correctly
    path('item/<int:id>/', ReadItemView.as_view(), name='read_item'),  # Ensure this name is set correctly
]