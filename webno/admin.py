from django.contrib import admin
from .models import Post,Comment
from django.utils.translation import ugettext_lazy as _





class WebnoPost(admin.ModelAdmin):
	list_display = ('title', 'slug', 'owner', 'updatetime',)
	list_filter = ('createtime', 'updatetime', 'owner',)
	search_fields = ('title', 'content',)
	date_hierarchy = 'updatetime'
	ordering = ['updatetime']
	prepopulated_fields = {'slug': ('title',)}
 

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)   


admin.site.register(Post,WebnoPost)
