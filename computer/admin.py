from django.contrib import admin
from .models import Item, Maker, Category, Comment
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.
admin.site.register(Item, MarkdownxModelAdmin)
admin.site.register(Comment)

class MakerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('maker_name',)}
admin.site.register(Maker,MakerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
admin.site.register(Category,CategoryAdmin)
