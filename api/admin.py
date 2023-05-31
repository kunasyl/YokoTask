from django.contrib import admin

from . import models


class VisitInline(admin.TabularInline):
    model = models.Visit
    extra = 1


class OrderInline(admin.TabularInline):
    model = models.Order
    extra = 1


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id')
    list_filter = ('employee_id', )
    search_fields = ('name',)
    inlines = (VisitInline, OrderInline,)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')
    list_filter = ('store_id',)
    search_fields = ('name', 'phone_number')
    inlines = (VisitInline, OrderInline,)


admin.site.register(models.Order)
admin.site.register(models.Visit)
admin.site.register(models.Customer)

admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
