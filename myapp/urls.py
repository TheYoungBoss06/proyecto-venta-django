from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),
    path('products/', views.view_products, name='view_products'), # Changed to 'products/' for better URL structure
    path('products/category/<slug:category_slug>/', views.view_products, name='view_products_by_category'), # Added for category filtering
    path('contact/',views.contact, name='contact'),
    path('about_us/',views.about_us, name='about_us'),
    path('view_blog/',views.view_blog, name='view_blog'),
    path('view_product_details/<int:product_id>/',views.view_product_details, name='view_product_details'),
    path('register',views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('view_shopping_cart/',views.view_shopping_cart, name='view_shopping_cart'),
    path('remove_cart_item/<int:item_id>/',views.remove_cart_item, name='remove_cart_item'),
    path('add_review/<int:product_id>/',views.add_review, name='add_review'),
    path('search/',views.search_products, name='search_products'),
    path('buynow/<int:item_id>/',views.buynow, name='buynow'),
    path('handle_payment/', views.handle_payment, name='handle_payment'),
    path('invoice/<int:order_id>/', views.view_invoice, name='view_invoice'), # Added URL for invoice view
    path('my_invoices/', views.view_all_invoices, name='view_all_invoices'), # Added URL for viewing all invoices
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'), # Added for coupon application
    path('warehouse/orders/', views.warehouse_order_list, name='warehouse_order_list'), # Added for warehouse order list
    path('warehouse/orders/<int:order_id>/', views.warehouse_order_detail, name='warehouse_order_detail'), # Added for warehouse order detail
    path('warehouse/orders/<int:order_id>/dispatch/', views.dispatch_order, name='dispatch_order'), # Added for dispatching orders
    path('dispatch/success/<int:order_id>/', views.dispatch_success_message, name='dispatch_success_message'), # Added for dispatch success message
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
