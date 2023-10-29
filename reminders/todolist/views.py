from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

from .models import ToDoItem
from .forms import ToDoItemModelForm


class ListTaskView(LoginRequiredMixin, ListView):
    template_name = "todolist/todo_list.html"
    model = ToDoItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_items"] = context["todoitem_list"].filter(completed=False)
        context["completed_items"] = context["todoitem_list"].filter(completed=True)
        return context

    def get_queryset(self):
        # Make sure user can only view his/her own tasks
        return super().get_queryset().filter(user=self.request.user)


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = ToDoItem
    form_class = ToDoItemModelForm
    template_name = "todolist/todo_form.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create a new task"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    form_class = ToDoItemModelForm
    template_name = "todolist/todo_form.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit task"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = ToDoItem
    template_name = "todolist/todo_confirm_delete.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@login_required
@require_POST
def complete_task(request, pk):
    item = get_object_or_404(ToDoItem, pk=pk)
    item.completed = request.POST.get("completed") == "true"
    item.save()
    return redirect("todo-list")


class ClearCompletedTasksView(LoginRequiredMixin, View):
    success_url = reverse_lazy("todo-list")

    def post(self, request, *args, **kwargs):
        completed_tasks = ToDoItem.objects.filter(
            user=self.request.user, completed=True
        )
        completed_tasks.delete()
        return HttpResponseRedirect(self.success_url)
