from django.contrib import admin
from .models import AppReview, AppFeedback, Notification
# Register your models here.



class AppReviewAdmin(admin.ModelAdmin):
    model = AppReview
    list_display = ('id', 'user', 'rating', 'comment')
    search_fields = ('user', 'rating', 'comment')
    ordering = ('user',)
    list_filter = ('rating',)
    fieldsets = (
        ('Detail', {'fields': ('user', 'rating', 'comment')}),
    )
    
class AppFeedbackAdmin(admin.ModelAdmin):
    model = AppReview
    list_display = ('user', 'feedback')
    search_fields = ('user', 'feedback')
    ordering = ('user',)
    list_filter = ('user',)
    fieldsets = (
        ('Detail', {'fields': ('user', 'feedback')}),
    )
    
    
class NotificationAdmin(admin.ModelAdmin) :
    model = Notification
    list_display = ('title', 'date')
    ordering = ('date',)
    fieldsets = (
        ('Detail', {'fields': ('title', 'notification')}),
    )
    readonly_fields = ('date',)
    

admin.site.register(AppReview, AppReviewAdmin)
admin.site.register(AppFeedback, AppFeedbackAdmin)
admin.site.register(Notification, NotificationAdmin)