from django.contrib import admin

from .models import Question,Choice
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
 
    fieldsets =[
        ("Add Question Here",{"fields":["question_text"]}),
        ("Date Information",{"fields":["pub_date"],"classes":["collapse"]}),
    ]

    inlines = [ChoiceInline]
    list_display = ["question_text","pub_date","was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

admin.site.register(Question,QuestionAdmin)
