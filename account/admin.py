from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email','name','division','role','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','name',)
    readonly_fields=('id', 'date_joined', 'last_login')
    ordering = ('name', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)