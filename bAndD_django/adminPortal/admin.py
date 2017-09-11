from django.contrib import admin
from .models import Store_item, Store_item_request

# Register your models here.
admin.site.register(Store_item)
admin.site.register(Store_item_request)