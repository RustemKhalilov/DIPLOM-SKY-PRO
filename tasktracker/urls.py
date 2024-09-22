from django.urls import path

from tasktracker.apps import TasktrackerConfig
from tasktracker.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    HomeView, TaskReportView, EmployeeReportView, ErrorpermissionView,
)

app_name = TasktrackerConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("list/", TaskListView.as_view(), name="tasktracker_list"),
    path("create/", TaskCreateView.as_view(), name="tasktracker_create"),
    path("tasksreport/", TaskReportView.as_view(), name="tasktracker_report"),
    path("employeesreport/", EmployeeReportView.as_view(), name="employees_report"),
    path("errorpermission/", ErrorpermissionView.as_view(), name="error_permission"),
    path("view/<int:pk>/'", TaskDetailView.as_view(), name="tasktracker_view"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="tasktracker_update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="tasktracker_delete")
]
