from django.contrib import admin
from .models import Store,Department,Aisle,Product,Price_product_history

admin.site.register(Store)
admin.site.register(Department)
admin.site.register(Aisle)
admin.site.register(Product)
admin.site.register(Price_product_history)