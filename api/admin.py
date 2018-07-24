from django.contrib import admin
from . import models



admin.site.register(models.UserAPI)

# Register your models here.


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
