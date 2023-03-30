from django.contrib import admin

from .models import (Book,
                     Authors,
                     Categories,
                     Borrow)

# Register your models here.

class BookAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'copies', 'slug',)
  list_display_links = ('id', 'title','slug',)
  search_fields = ('title', 'id', 'slug',)
  prepopulated_fields = {'slug': ('title',)}
  
  
class BorrowAdmin(admin.ModelAdmin):
  list_display = ('id', 'when', 'copies', 'status',)
  list_display_links = ('id',)
  search_fields = ('id', 'status',)
  

class AuthorAdmin(admin.ModelAdmin):
  list_display = ('id', 'get_full_name', 'slug',)
  list_display_links = ('id', 'slug',)
  search_fields = ('id', 'get_full_name', 'slug',)
  
class CategoriesAdmin(admin.ModelAdmin):
  list_display = ('id', 'slug',)
  list_display_links = ('id', 'slug',)
  search_fields = ('id', 'slug',)


admin.site.register(Book, BookAdmin)
admin.site.register(Borrow)
admin.site.register(Authors)
admin.site.register(Categories)
