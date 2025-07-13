from django.urls import path
# from .views import login_redirect_view,home,register_view,admin_product_list
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('redirect-after-login/',views.login_redirect_view, name='login-redirect'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('profile/', views.user_profile, name='user_profile'),

    path('admin-1/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/edit/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    path('admin/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin/product/create/', views.add_product, name='add_product'),


    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('payment/', views.payment, name='payment') ,  

]
