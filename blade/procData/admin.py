from django.contrib import admin
from procData.models import breachStructure


@admin.register(breachStructure)
class breachStructureAdmin(admin.ModelAdmin):
	list_fields = ['email','handle','userId']