from django.contrib import admin

from .models import User, listing, bid, comments, watch

# Register your models here.
admin.site.register(User)
admin.site.register(listing)
admin.site.register(bid)
admin.site.register(comments)
admin.site.register(watch)