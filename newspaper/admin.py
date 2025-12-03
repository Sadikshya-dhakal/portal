from django.contrib import admin

from newspaper.models import Category, Post, Tag, OurTeam, Contact, Comment, Newsletter, Advertisement

from unfold.admin import ModelAdmin
from django import forms
from tinymce.widgets import TinyMCE
# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(OurTeam)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Newsletter)
admin.site.register(Advertisement) 




class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'status', 'views_count', 'published_at')
    


admin.site.register(Post, PostAdmin)
