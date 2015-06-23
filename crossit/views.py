#! /usr/bin/env python
# -*-coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse,HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse
from utils import *
from crossit.models import *
from crossit.wsgi import g_qmail_obj
import random




#Login page
def home(request):
    if not request.user.is_authenticated():
        return TemplateResponse(request,"index.html",{'emails':g_qmail_obj.getNameList()})
    return MainPage(request)

''' 
 Check if user with name <name> exists
 We'll send him a verification code in case he's NOT
'''
def checkExist(request):
    name = request.POST['name']
    u = CrossUser.objects.filter(name=name)
    if len(u) > 0:
        return JsonResponse({'exist':True})
    elif name in g_qmail_obj.getNameList():
        vcode = VCode.objects.filter(name=name)
        if len(vcode) <= 0:
            code    = ''.join(random.sample('ABCEFGHJKLMNPQRSTUVWXYZ',4))
            vcode   = VCode(name=name,vcode=code)
            vcode.save()
            to_list = name + '@' + g_qmail_obj.domain
            content = '感谢注册，您的邮箱验证码是:%s' %(code)
            html_ct = '感谢注册，您的邮箱验证码是：<h3>%s</h3>' %(code)
            j = MailJobQue(subject='[Crossit]您的注册验证码',
              to_list = to_list,
              content = content,
              html_ct = html_ct)
            j.save()
    return JsonResponse({'exist':False})
'''
Registration of new users
'''
def regUsr(request):
    if request.method != 'POST':
      return JsonResponse({'success':False,'msg':'无效请求。'})
    name    = request.POST['email']
    passwd  = request.POST['password']
    passwd2 = request.POST['password2']
    vcode   = request.POST['vcode']
    if not name:
        return JsonResponse({'success':False,'msg':'请输入用户名。'})
    if passwd != passwd2:
        return JsonResponse({'success':False,'msg':'两次密码不一致。'})
    c = VCode.objects.filter(name=name)
    if len(c) <= 0 or c[0].vcode != vcode:
        return JsonResponse({'success':False,'msg':'无效验证码。'})
    u = CrossUser.objects.filter(name=name)
    if len(u) > 0:
        return JsonResponse({'success':False,'msg':'该用户已存在。'})
    elif name in g_qmail_obj.getNameList():
        email = name + '@' + g_qmail_obj.domain
        fullname = g_qmail_obj.users[email].name
        try:
          u = CrossUser.objects.create_user(fullname[1:],fullname[0], email, passwd,True,name=name)
        except:
          return JsonResponse({'success':False,'msg':'创建用户失败。'})
        u.save()
        #Default SESSION_COOKIE_AGE will be 2 weeks, By default, SESSION_EXPIRE_AT_BROWSER_CLOSE is set to False
        #So when the 'remember me' is not checked, we set it expired when close browser
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)
        return JsonResponse({'success':True,'msg':'用户注册成功。'})
    return JsonResponse({'success':False,'msg':'无效请求。'})
'''
Login 
'''
def loginUsr(request):
  if request.method != 'POST':
    return JsonResponse({'success':False,'msg':'无效请求。'})
  if not request.POST.get("email",None) or not request.POST.get("password",None):
    return JsonResponse({'success':False,'msg':'无效请求。'})
  name  = request.POST.get("email",None)
  passw = request.POST.get("password",None)
  if not name or not passw:
    return JsonResponse({'success':False,'msg':'用户名/密码不能为空。'})
  cache_usr = authenticate(email=name+ '@' + g_qmail_obj.domain,password=passw)
  if cache_usr is None:
    return JsonResponse({'success':False,'msg':'密码错误。'})
  else:
    login(request,cache_usr)
    if not request.POST.get('remember', None):
        request.session.set_expiry(0)
    return  HttpResponsePermanentRedirect('/main/')

'''
Logout
'''
def UsrLogout(request):
    if request.user.is_authenticated():
        logout(request)
    return  HttpResponsePermanentRedirect('/')
'''
MainPage after one's login
'''
def MainPage(request):
    if not request.user.is_authenticated():
        return TemplateResponse(request,"error.html",{'error':'未登录。'})
    u = CrossUser.objects.get(pk=request.user.id)
    try:
        newcount = g_qmail_obj.users[u.email].unread
    except Exception as err:
        newcount = 'N/A'
        print(err)
    return TemplateResponse(request,"main.html",
        {'user':u,
        'email':{'fast':g_qmail_obj.getFastLane(u.email),
        'unread':newcount}})