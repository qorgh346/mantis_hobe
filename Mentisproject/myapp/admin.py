from django.contrib import admin
from .models import *

# Register your models here.

# 유저 DB
@admin.register(User_info)
class User_infoAdmin(admin.ModelAdmin):
    list_display = ('user_id','user_name','user_certification_check')


# 멘티 DB
@admin.register(Menti_info)
class Menti_infoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_info_id', 'contents')
    list_display_links = ('pk', 'user_info_id')

# 캐시 DB
@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ('payer', 'user_id', 'cash_charge', 'cash_at', 'success_true_false')

# 결제 DB
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'payment_at', 'sum')