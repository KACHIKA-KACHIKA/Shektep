from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from .models import (Pack, Task, SolvedPacks, Section,
                     Subsection, SolvedTasks, ReadingImage)

from user.models import AccessRight


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'task_image_preview', 'pack_id')

    def get_changeform_initial_data(self, request):
        last_pack = Pack.objects.order_by('-id').first()
        return {'pack_id': last_pack.id if last_pack else None}


class AssignAccessForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    access_right = forms.ModelChoiceField(
        queryset=AccessRight.objects.all(),
        required=True,
        label="Выберите право доступа"
    )


@admin.action(description="Назначить доступ...")
def assign_access_right(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = AssignAccessForm(request.POST)
        if form.is_valid():
            access_right = form.cleaned_data['access_right']
            for pack in queryset:
                pack.access_rights.add(access_right)
            modeladmin.message_user(
                request, f"Доступ {access_right} назначен {queryset.count()} пак(ам).")
            return redirect(request.get_full_path())
    else:
        form = AssignAccessForm(initial={
            'action': 'assign_access_right',
            '_selected_action': request.POST.getlist('action_checkbox')
        })

    return render(request, 'admin/assign_access.html', context={
        'items': queryset,
        'form': form,
        'title': 'Назначить доступ выбранным',
    })


class RemoveAccessForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    access_right = forms.ModelChoiceField(
        queryset=AccessRight.objects.all(),
        required=True,
        label="Выберите право доступа для удаления"
    )


@admin.action(description="Удалить доступ...")
def remove_access_right(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = RemoveAccessForm(request.POST)
        if form.is_valid():
            access_right = form.cleaned_data['access_right']
            for pack in queryset:
                pack.access_rights.remove(access_right)
            modeladmin.message_user(
                request, f"Доступ {access_right} удалён у {queryset.count()} пак(ов).")
            return redirect(request.get_full_path())
    else:
        form = RemoveAccessForm(initial={
            'action': 'remove_access_right',
            '_selected_action': request.POST.getlist('action_checkbox')
        })

    return render(request, 'admin/remove_access.html', context={
        'items': queryset,
        'form': form,
        'title': 'Удалить доступ у выбранных',
    })


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('id', 'subsection', 'is_published')
    actions = [assign_access_right, remove_access_right]


admin.site.register(Task, TaskAdmin)
admin.site.register(SolvedPacks)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(SolvedTasks)
admin.site.register(ReadingImage)
