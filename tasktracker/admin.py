from django.contrib import admin
from tasktracker.models import Task
from users.models import Posts


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "Creator", "Executor", "name", "description", "status")
    list_filter = ("status",)
    search_fields = ("name",)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_filter = (
        "Post",
    )
