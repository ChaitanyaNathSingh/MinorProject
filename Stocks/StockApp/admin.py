from django.contrib import admin
from .models import Profile, Stock, StockData, UserStocks
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    resource_class = Profile
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone', 'gender', 'dob', 'location')
    list_filter = ('gender', 'location')
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__profile__phone']
    ordering = ['user__username', 'gender', ]
    save_as = True
    save_on_top = True

    def email(self, obj):
        return obj.user.email

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


admin.site.register(Profile, ProfileAdmin)

class StockAdmin(admin.ModelAdmin):
    list_display = ('Stock_id', 'Stock_name', 'Stock_type', 'Stock_about', 'Company_name')
    list_filter = ('Stock_type', 'Company_name')
    search_fields = ['Stock_name', 'Stock_type', 'Company_name']
    save_as = True    
    save_on_top = True

admin.site.register(Stock, StockAdmin)

class  StockDataAdmin(ImportExportModelAdmin,  admin.ModelAdmin):
    list_display = ('id', 'stock_name', 'company_name', 'stock_type', 'Stock_price', 'Stock_date')
    list_filter = ('Stock_id__Company_name', 'Stock_id__Stock_type', 'Stock_id__Stock_name')
    search_fields = ['Stock_id__Stock_name', 'Stock_id__Company_name', 'Stock_id__Stock_type', 'Stock_price', 'Stock_date']
    save_as = True    
    save_on_top = True

    def stock_name(self, obj):
        return obj.Stock_id.Stock_name
    
    def company_name(self, obj):
        return obj.Stock_id.Company_name
    
    def stock_type(self, obj):
        return obj.Stock_id.Stock_type

admin.site.register(StockData, StockDataAdmin)

class UserStocksAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone', 'Stock_name', 'Stock_type', 'Stock_about', 'Company_name', 'Stock_date', 'Stock_price')

    def email(self, obj):
        return obj.user.email

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name
    
    def phone(self, obj):
        return obj.user.profile.phone

    def Stock_name(self, obj):
        return obj.Stock_id.Stock_name
    
    def Stock_type(self, obj):
        return obj.Stock_id.Stock_type
    
    def Stock_about(self, obj):
        return obj.Stock_id.Stock_about
    
    def Company_name(self, obj):
        return obj.Stock_id.Company_name

admin.site.register(UserStocks, UserStocksAdmin)