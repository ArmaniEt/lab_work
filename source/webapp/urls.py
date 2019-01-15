from django.urls import path

from webapp.views import FoodListView, FoodCreateView, FoodUpdateView, FoodDeleteView, \
    OrderCreateView, OrderListView, OrderUpdateView, OrderDataUpdateView, \
    delete_view, canceled_view, delivery_view, OrderCreateFoodView, OrderDetailView


from django.conf.urls.static import static
from django.conf import settings

app_name = 'webapp'

urlpatterns = [
    path('', FoodListView.as_view(), name='index'),
    path('food/create', FoodCreateView.as_view(), name='food_create'),
    path('food/<int:pk>/update', FoodUpdateView.as_view(), name='food_update'),
    path('food/<int:pk>/delete', FoodDeleteView.as_view(), name='food_delete'),


    path('order/create', OrderCreateView.as_view(), name='order_create'),
    path('orders', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/view', OrderDetailView.as_view(), name='order_detail'),


    path('order/<int:pk>', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/data/update', OrderDataUpdateView.as_view(), name='order_data_update'),
    path('order/food/<int:food_pk>/delete', delete_view, name='order_delete_food'),


    path('order/<int:order_pk>/cancel', canceled_view, name='canceled_order'),
    path('order/<int:order_pk>/delivery', delivery_view, name='delivery_order'),
    path('order/<int:pk>/create_food', OrderCreateFoodView.as_view(), name='order_food_create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)