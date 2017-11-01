from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from chores.models import *
from chores.forms import *

# Task Views

class TaskList(View):
    def get(self, request):
        template = 'tasks/task_list.html'
        context = {
            'tasks': Task.objects.alphabetical()
        }
        return render(request, template, context)

class TaskDetail(View):
    def get(self, request, pk):
        template = 'tasks/task_detail.html'
        task = get_object_or_404(Task, pk=pk)
        context = {
            'task': task
        }
        return render(request, template, context)

class TaskCreate(View):
    def get(self, request):
        template = 'tasks/task_form.html'
        form = TaskForm()
        context = {
            'form': form
        }
        return render(request, template, context)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Successfully created %s!' % task.name)
            return HttpResponseRedirect(reverse('chores:task_detail', args=(task.id,)))
        else:
            template = 'tasks/task_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class TaskUpdate(View):
    def get(self, request, pk):
        template = 'tasks/task_form.html'
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        context = {
            'task': task,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Successfully updated %s!' % task.name)
            return HttpResponseRedirect(reverse('chores:task_detail', args=(task.id,)))
        else:
            template = 'tasks/task_form.html'
            context = {
                'task': task,
            	'form': form
            }
            return render(request, template, context)

class TaskDelete(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        messages.success(request, 'Successfully deleted %s!' % task.name)
        return HttpResponseRedirect(reverse('chores:task_list'))

