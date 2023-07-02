from django.urls import path
from . import views
app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    # path('store/page/<int:page>/', views.store, name='store_page'),
    path('search',views.search,name='search'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('view_by_category/<int:id>', views.view_by_category, name='view_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('wishlist/add/<int:product_id>/',views.wishlist_add, name='wishlist_add'),
    path('wishlist',views.view_wishlist,name='view_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.wishlist_remove, name='wishlist_remove'),
 
]