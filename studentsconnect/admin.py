from django.contrib import admin
from studentsconnect.models import Category, Page, University
from studentsconnect.models import UserProfile, ContactMessage, Country


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')





admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(ContactMessage)
admin.site.register(Country)
admin.site.register(University)

