from django.contrib import admin
from procData.models import breachStructure, dbQueriedUsers


@admin.register(breachStructure)
class breachStructureAdmin(admin.ModelAdmin):
    list_fields = ['email','handle','userId']


@admin.register(dbQueriedUsers)
class dbQueriedUsersAdmin(admin.ModelAdmin):
    list_fields = ['user']
