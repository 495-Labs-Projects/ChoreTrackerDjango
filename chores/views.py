from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from chores.models import *
from chores.forms import *

# Child Views

class ChildList(View):
    def get(self, request):
        template = 'children/child_list.html'
        context = {
            'children': Child.objects.alphabetical()
        }
        return render(request, template, context)

class ChildDetail(View):
    def get(self, request, pk):
        template = 'children/child_detail.html'
        child = get_object_or_404(Child, pk=pk)
        context = {
            'child': child
        }
        return render(request, template, context)

class ChildCreate(View):
    def get(self, request):
        template = 'children/child_form.html'
        form = ChildForm()
        context = {
            'form': form
        }
        return render(request, template, context)

    def post(self, request):
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save()
            messages.success(request, 'Sucessfully created %s!' % child.name())
            return HttpResponseRedirect(reverse('chores:child_detail', args=(child.id,)))
        else:
            template = 'children/child_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class ChildUpdate(View):
    def get(self, request, pk):
        template = 'children/child_form.html'
        child = get_object_or_404(Child, pk=pk)
        form = ChildForm(instance=child)
        context = {
            'child': child,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk):
        child = get_object_or_404(Child, pk=pk)
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            child = form.save()
            messages.success(request, 'Sucessfully updated %s!' % child.name())
            return HttpResponseRedirect(reverse('chores:child_detail', args=(child.id,)))
        else:
            template = 'children/child_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class ChildDelete(View):
    def post(self, request, pk):
        child = get_object_or_404(Child, pk=pk)
        child.delete()
        messages.success(request, 'Sucessfully deleted %s!' % child.name())
        return HttpResponseRedirect(reverse('chores:child_list'))


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
            messages.success(request, 'Sucessfully created %s!' % task.name)
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
            messages.success(request, 'Sucessfully updated %s!' % task.name)
            return HttpResponseRedirect(reverse('chores:task_detail', args=(task.id,)))
        else:
            template = 'tasks/task_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class TaskDelete(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        messages.success(request, 'Sucessfully deleted %s!' % task.name)
        return HttpResponseRedirect(reverse('chores:task_list'))


# Chore Views



