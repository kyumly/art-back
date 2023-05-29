from django.contrib import admin
from art.models import User, Post, report, PostFile, Comment
# Register your models here.

@admin.register(Comment)
class UserAdmin(admin.ModelAdmin):
    pass
#
#
@admin.register(PostFile)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    pass