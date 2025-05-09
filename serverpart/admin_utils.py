from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from user.models import AccessRight


def make_assign_access_action():
    @admin.action(description="Назначить доступ...")
    def assign_access(modeladmin, request, queryset):
        model_name = modeladmin.model._meta.verbose_name_plural
        return _handle_access_right_form(
            modeladmin, request, queryset, assign=True,
            title=f"Назначить доступ выбранным {model_name}"
        )
    assign_access.__name__ = "assign_access_right"
    return assign_access


def make_remove_access_action():
    @admin.action(description="Удалить доступ...")
    def remove_access(modeladmin, request, queryset):
        model_name = modeladmin.model._meta.verbose_name_plural
        return _handle_access_right_form(
            modeladmin, request, queryset, assign=False,
            title=f"Удалить доступ у выбранных {model_name}"
        )
    remove_access.__name__ = "remove_access_right"
    return remove_access


def _handle_access_right_form(modeladmin, request, queryset, assign=True, title=""):
    class AccessForm(forms.Form):
        action = forms.CharField(widget=forms.HiddenInput)
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        access_right = forms.ModelChoiceField(
            queryset=AccessRight.objects.all(),
            required=True,
            label="Выберите право доступа"
        )

    action_name = "assign_access_right" if assign else "remove_access_right"

    if 'apply' in request.POST:
        form = AccessForm(request.POST)
        if form.is_valid():
            access_right = form.cleaned_data['access_right']
            for obj in queryset:
                if hasattr(obj, 'access_rights'):
                    if assign:
                        obj.access_rights.add(access_right)
                    else:
                        obj.access_rights.remove(access_right)
            action_past = "назначен" if assign else "удалён"
            modeladmin.message_user(
                request,
                f"Доступ {access_right} {action_past} у {queryset.count()} объект(ов)."
            )
            return redirect(request.get_full_path())
    else:
        form = AccessForm(initial={
            'action': action_name,
            '_selected_action': request.POST.getlist('action_checkbox')
        })

    return render(request, 'admin/assign_access.html', context={
        'items': queryset,
        'form': form,
        'title': title,
    })
