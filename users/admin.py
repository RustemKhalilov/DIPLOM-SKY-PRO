from django.contrib import admin

from users.models import User, Posts


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "email",
    )


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_filter = (
        "Post",
    )
