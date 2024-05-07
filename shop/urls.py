from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from products.views import (home_page, single_product, MyFormView, MyLoginFormView, logout_view, LogoutTemplate,
                            search_products,category_page,add_product_to_cart,user_cart,add_to_favorites,liked_items)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('search', search_products),
    path('product/<int:id>', single_product),
    path('category/<int:id>', category_page),
    path('register', MyFormView.as_view()),#class
    path('login', MyLoginFormView.as_view()), #class
    path('logout', logout_view),
    path('sure-logout', LogoutTemplate.as_view()),#class
    path('add_to_cart/<int:id>', add_product_to_cart),
    path('user_cart/', user_cart),
    path('add_to_favorites/<int:id>',add_to_favorites),
    path('favorites',liked_items),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)