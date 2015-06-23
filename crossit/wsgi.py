"""
WSGI config for crossit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crossit.settings")
from django.core.wsgi import get_wsgi_application
from qmail.qmail import *
from utils.labthread import CrossThread
from utils.labmail import SendMail
from crossit.models import *
'''
Thread function to send email
'''
def MainFcn():
    for j in MailJobQue.objects.all():
        to_list = j.to_list.split(',')
        SendMail(j.subject, None, to_list, [], j.content, j.html_ct)
        j.delete()
'''
Create a global email thread, and start
'''
g_mail_thread = CrossThread(5,MainFcn,None,False)
g_mail_thread.start()


g_qmail_obj = Qmail('lonestep1','48f0685065ef95a1df5e896b99359005',True)
g_qmail_obj.initDepts(g_qmail_obj.depts)

application = get_wsgi_application()
