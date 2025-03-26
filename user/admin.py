from django.contrib import admin
from django.contrib.auth.models import User
from .models import (Subscription, SubscriptionList,
                     Lesson, UserLessonProgress, AccessRight)


class SubscriptionListInline(admin.TabularInline):
    model = SubscriptionList
    extra = 1
    search_fields = ['subscription_id']


class UserAdmin(admin.ModelAdmin):
    inlines = [SubscriptionListInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            return [field.name for field in self.model._meta.fields]
        return []

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_staff and not request.user.is_superuser:
            fields.remove('groups')
            fields.remove('is_superuser')
            fields.remove('user_permissions')
            fields.remove('password')
            fields.remove('first_name')
            fields.remove('last_name')
            fields.remove('is_active')
            fields.remove('date_joined')
        return fields


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
admin.site.register(SubscriptionList)
admin.site.register(AccessRight)
admin.site.register(Lesson)
admin.site.register(UserLessonProgress)
