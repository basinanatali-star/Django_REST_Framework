from django.contrib import admin
from .models import CustomUser, Payment


admin.site.register(CustomUser)

admin.site.register(Payment)