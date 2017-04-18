# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Question, Choice, Profile
from django.contrib import admin

# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
	list_display=['question','pub_date']
	search_fields= ('question',)

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Profile)
