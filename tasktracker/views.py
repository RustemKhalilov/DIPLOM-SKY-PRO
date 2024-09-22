from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from tasktracker.forms import TaskForm

from django.views.generic import TemplateView

from tasktracker.models import Task

from users.models import User

from datetime import date

from tasktracker.services import send_telegram_message


class HomeView(TemplateView):
    """
    Контроллер главной страницы сайта
    """
    template_name = 'tasktracker/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        context_data['all_tasks'] = tasks.count()
        # Вот этот ключ потом идет на отображение <li class="list-group-item">Всего заданий - {{all_task}}</li>
        # context_data['active_task'] = tasks.filter(status=Task.status).count()
        return context_data


class TaskListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за вывод заданий пользователя
    """
    model = Task

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        queryset = queryset.filter(Creator=self.request.user) | queryset.filter(Executor=self.request.user)
        return queryset


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание задания
    """
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasktracker:tasktracker_list')

    def form_valid(self, form):
        task = form.save()
        task.Creator = self.request.user
        task.save()
        message = f"Вам пришло задание от {task.Creator}"
        send_telegram_message(task.Executor.tg_nick, message)
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий просмотр деталей задания
    """
    model = Task
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['object_list'] = task  # Вот словарь 'object_list' потом извлекается на страницу
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование задания
    """
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('tasktracker:tasktracker_view', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """
        Функция, определяющая поля для редактирования в зависимости от прав пользователя
        """
        user = self.request.user
        if user == self.object.Creator or self.object.Executor or user.is_superuser:
            return TaskForm
        elif user.has_perm('tasktracker:tasktracker_list'):
            return TaskForm
        else:
            raise PermissionDenied


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление задания
    """
    model = Task
    success_url = reverse_lazy('tasktracker:tasktracker_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.Creator or self.request.user.is_superuser:
            return self.object
        else:
            redirect('tasktracker:error_permission')
    #         raise AttributeError
    # except AttributeError as e:
    #     print("Ошибка прав доступа")
    #     redirect("tasktracker/errorpermission.html")


class TaskReportView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за вывод отчета
    """
    model = Task
    template_name = 'tasktracker/task_report.html'

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        return queryset


class EmployeeReportView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за вывод отчета по загруженности сотрудников
    """
    model = Task
    template_name = 'tasktracker/employee_report.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        employee = User.objects.all()
        my_report = []
        for item in employee:
            work_day = 0
            task_count = 0
            for item2 in tasks:
                if item == item2.Executor and item2.status == "В работе":
                    task_count += 1
                    work_day += (item2.end_time - date.today()).days
            if f"{item.Firstname} {item.Surname} {item.Patronymic}" != "Самый Главный Админ":
                my_report.append(f" {item} Количество задач - {task_count} шт., Загруженность - {work_day} дней.")
        contex['my_report'] = my_report
        return contex


class ErrorpermissionView(LoginRequiredMixin, TemplateView):
    template_name = 'tasktracker/errorpermission.html'
