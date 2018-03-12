from django.contrib import admin
from alphacode.models import RandomURLs

# Register your models here.

class URLAdmin(admin.ModelAdmin):
    list_display = ('id', 'random_url', 'group_name', 'timestamp', 'valid')
admin.site.register(RandomURLs, URLAdmin)
