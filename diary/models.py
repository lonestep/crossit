from django.db import models
from  DjangoUeditor.models import UEditorField


def getUploadImgPath(model_instance=None):
    here = datetime.datetime.now()
    return 'diary/images/%d/%d/%d/' %(model_instance.who.name,here.year,here.month,here.day)

def getUploadAttachPath(model_instance=None):
    here = datetime.datetime.now()
    return 'diary/attach/%d/%d/%d/' %(model_instance.who.name,here.year,here.month,here.day)

class Diary(models.Model):
    when    = models.DateTimeField(blank=True, null=True)
    who     = models.ForeignKey('crossit.CrossUser')
    content = UEditorField(u'内容',
        width=600, 
        height=300, 
        toolbars="full", 
        imagePath='diary/images/', 
        filePath='diary/attach/', 
        upload_settings={"imageMaxSize":1204000},
        settings={},
        command=None)

