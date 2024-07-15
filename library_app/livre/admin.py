from django.contrib import admin
from .models import Books , Loans , Penalty 

admin.site.register(Books)
admin.site.register(Loans)
admin.site.register(Penalty)