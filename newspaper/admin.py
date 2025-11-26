from django.contrib import admin

from newspaper.models import Category, Post, Tag, OurTeam, Contact

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(OurTeam)
admin.site.register(Contact)
