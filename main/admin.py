from django.contrib import admin

from main.models import ContractTemplate, Contract, AuthenticationCode

admin.site.register(ContractTemplate)
admin.site.register(Contract)
admin.site.register(AuthenticationCode)
