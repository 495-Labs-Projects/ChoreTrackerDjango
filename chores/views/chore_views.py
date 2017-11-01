from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from chores.models import *
from chores.forms import *

# Chore Views

class ChoreList(View):
    def get(self, request):
        template = 'chores/chore_list.html'
        context = {
            'chores': Chore.objects.chronological()
        }
        return render(request, template, context)

class ChoreDetail(View):
    def get(self, request, pk):
        template = 'chores/chore_detail.html'
        chore = get_object_or_404(Chore, pk=pk)
        context = {
            'chore': chore
        }
        return render(request, template, context)

class ChoreCreate(View):
    def get(self, request):
        template = 'chores/chore_form.html'
        form = ChoreForm()
        context = {
            'form': form
        }
        return render(request, template, context)

    def post(self, request):
        form = ChoreForm(request.POST)
        if form.is_valid():
            chore = form.save()
            messages.success(request, 'Successfully created chore!')
            return HttpResponseRedirect(reverse('chores:chore_detail', args=(chore.id,)))
        else:
            template = 'chores/chore_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class ChoreUpdate(View):
    def get(self, request, pk):
        template = 'chores/chore_form.html'
        chore = get_object_or_404(Chore, pk=pk)
        form = ChoreForm(instance=chore)
        context = {
            'chore': chore,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk):
        chore = get_object_or_404(Chore, pk=pk)
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            chore = form.save()
            messages.success(request, 'Successfully updated chore!')
            return HttpResponseRedirect(reverse('chores:chore_detail', args=(chore.id,)))
        else:
            template = 'chores/chore_form.html'
            context = {
                'chore': chore,
            	'form': form
            }
            return render(request, template, context)

class ChoreDelete(View):
    def post(self, request, pk):
        chore = get_object_or_404(Chore, pk=pk)
        chore.delete()
        messages.success(request, 'Successfully deleted chore!')
        return HttpResponseRedirect(reverse('chores:chore_list'))


