from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task

from .forms import TaskForm

# Create your views here.


def signup(request):
    if request.method == "GET":
        return render(request, "home/signup.html", {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "home/signup.html",
                    {"form": UserCreationForm, "error": "Username already exists."},
                )

        return render(
            request,
            "home/signup.html",
            {"form": UserCreationForm, "error": "Passwords did not match."},
        )


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "task/tasks.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "task/create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task/create_task.html",
                {"form": TaskForm, "error": "Error creating task."},
            )


def home(request):
    return render(request, "home/home.html")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "home/signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "home/signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect.",
                },
            )

        login(request, user)
        return redirect("tasks")


def findTasks(request):
    filterTitle = request.GET.get("filterTitle", "")

    tasks = Task.objects.filter(title=filterTitle)

    return render(request, "task/tasks.html", {"tasks": tasks})


from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Task


@login_required
def manage_tasks(request):
    if request.method == "POST":
        action = request.POST.get("action")
        print(action)
        # Acción de actualización
        if action and action.startswith("update_"):
            task_id = action.split("_")[1]
            print(f"Actualizar tarea con ID: {task_id}")
            return redirect("updateTask", task_id=task_id)

        # Acción de marcar como completada

        # Acción de eliminar tareas seleccionadas
        elif action == "delete_selected":
            tasks_to_delete = request.POST.getlist("tasks_to_delete")
            if tasks_to_delete:
                Task.objects.filter(
                    id__in=tasks_to_delete
                ).delete()  # Eliminar tareas seleccionadas
                print(f"Tareas eliminadas: {tasks_to_delete}")
            return redirect("AdminTask")
        elif action and action.startswith("completed_"):
            task_id = action.split("_")[1]
            print(task_id)
            task = get_object_or_404(Task, id=task_id)
            task.datecompleted = timezone.now()
            task.save()
            return redirect("AdminTask")
    # Si no es POST, renderiza las tareas
    tasks = Task.objects.all()
    return render(request, "task/tasksAdmin.html", {"tasks": tasks})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.save()
        return redirect("AdminTask")
    return render(request, "task/update_task.html", {"task": task})
