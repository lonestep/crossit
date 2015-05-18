#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import *
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


#User manager, create dihe user
class DiHeUserManager(BaseUserManager):
    def _create_user(self, first_name,last_name, email, password,
                     is_active,is_superuser,is_staff,**extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(u'请提供有效邮箱.')
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,
                          last_name=last_name,
                          is_active=is_active,
                          is_superuser=is_superuser,
                          is_staff = is_staff,
                          last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, first_name,last_name, email, password,is_active,**extra_fields):
        return self._create_user(first_name,last_name, email, password,
                     is_active,False,False,**extra_fields);
    def create_superuser(self, first_name,last_name, email, password,**extra_fields):
        return self._create_user(first_name,last_name, email, password,True,True,True,**extra_fields);

#Abstract dihe user, parent class for DiHeUser 
class DiHeAbstractUser(AbstractBaseUser,PermissionsMixin):
    first_name  = models.CharField(_('first name'), max_length=30)
    last_name   = models.CharField(_('last name'), max_length=30)
    email       = models.EmailField(_('email address'),unique=True)
    is_active   = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = DiHeUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.id)
    def get_full_name(self):
        full_name = '%s%s' % (self.last_name,self.first_name )
        return full_name.strip()
    def get_short_name(self):
        return self.first_name
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
    def GetUsrFilePath(self):
        return self.date_joined.strftime('%Y%m/%d/') + str(self.id)
    
def GetUsrFilePath(usr):
    return usr.date_joined.strftime('%Y%m/%d/') + str(usr.id)
def GetUsrTempFilePath(usr,filename):
    return GetUsrFilePath(usr,filename)+'tmp'

GENDER_CHOICES = (
    ('NOTSET', 0),
    ('MALE', 1),
    ('FEMALE', 2),
)
#Class representing a homesa user  
class DiHeUser(DiHeAbstractUser):
    hasMsg    = models.BooleanField(verbose_name="是否有新信息",default=False)
    mood      = models.CharField(max_length=128,default='',blank=True, null=True)
    addr      = models.CharField(max_length=128,default='',blank=True, null=True)
    tel       = models.CharField(max_length=16,default='',blank=True, null=True)
    name      = models.CharField(max_length=16,default='',blank=True, null=True)
    mobile    = models.CharField(max_length=16,default='',blank=True, null=True)
    position  = models.CharField(max_length=32,default='',blank=True, null=True)
    depts     = models.CharField(max_length=128,default='',blank=True, null=True)
    gender    = models.CharField(verbose_name="性别",max_length=6,choices=GENDER_CHOICES,default='NOTSET')
    native    = models.CharField(max_length=128,default='',blank=True, null=True)
    iShare    = models.BinaryField(blank=True, null=True)
    tShare    = models.TextField(default='[]',blank=True, null=True)
    birthd    = models.DateField(blank=True, null=True)
    avatar    = models.FileField(upload_to=GetUsrFilePath,default='default/default_avatar.png')
    tmpfile   = models.FileField(upload_to=GetUsrTempFilePath,default='/media/tmp/')
    mcount    = models.PositiveIntegerField(default=0)
    class Meta(DiHeAbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

