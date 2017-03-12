from django.contrib import admin

# Register your models here.
from .models import author,comment,category,post,friend


admin.site.register(author)
admin.site.register(comment)
admin.site.register(category)
admin.site.register(post)
admin.site.register(friend)