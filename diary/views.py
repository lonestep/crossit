#! /usr/bin/env python
# -*-coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.template.response import TemplateResponse
from diary.forms import DiaryForm

def home(request):
    form = DiaryForm()
    return TemplateResponse(request,"diary/index.html",{'form':form})