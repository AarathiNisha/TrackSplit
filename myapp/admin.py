from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Expense,MyCircle,Category,Motivation

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'user', 'category', 'circle', 'date')  # Shows these columns
    list_filter = ('category', 'circle', 'user') # Adds filters in the right sidebar

admin.site.register(CustomUser,UserAdmin)
admin.site.register(Expense)
admin.site.register(MyCircle)
admin.site.register(Category)
admin.site.register(Motivation)
