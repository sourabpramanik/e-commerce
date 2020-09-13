from django.contrib import admin
from .models import  User, Listings, Bid, Comment, Category
from django.contrib.auth.admin import UserAdmin
# Register your models here.


admin.site.register(Listings)
admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)