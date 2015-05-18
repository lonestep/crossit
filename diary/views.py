#! /usr/bin/env python
# -*-coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.template.response import TemplateResponse

def home(request):
    return TemplateResponse(request,"diary/index.html",{})