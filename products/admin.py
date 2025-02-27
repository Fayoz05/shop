from django.contrib import admin

from .models import CategoryModel, ProductsModel ,MyUserModel, CartModel,LikeModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    search_fields = ['category_name','id','created_at']
    list_filter = ['created_at']
    list_display = ['id','category_name','created_at']
    ordering = ['-id',]


@admin.register(ProductsModel)
class ProductsModelAdmin(admin.ModelAdmin):
    search_fields = ['product_name','id','created_at']
    list_filter = ['created_at']
    list_display = ['id','product_name','created_at']
    ordering = ['-id',]

# admin.site.register(ProductsModel)


@admin.register(MyUserModel)
class MyUserModelAdmin(admin.ModelAdmin):
    search_fields = ['username','id']
    list_display = ['username','id','phone_number','email']
    ordering = ['-id']

admin.site.register(CartModel)
admin.site.register(LikeModel)