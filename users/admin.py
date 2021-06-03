from django.contrib import admin
from .models import Question, Choice
# Register your models here.

admin.site.site_header = "LivePolls Admin"
admin.site.site_title = "LivePolls Admin Area"
admin.site.index_title = "Welcome to the LivePolls admin area"

# admin.site.register((Question, Choice))

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}),
                ('User Information', {'fields': ['user']}),
                ('Live Status', {'fields': ['livestatus']}),
                ('publish Status', {'fields': ['publicstatus']}),
                ('Date Information', {'fields': ['timestamp'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInline]


    
# admin.site.register(Question)
# admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
