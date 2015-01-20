from django.db import models
from django.utils.encoding  import smart_unicode
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
# Create your models here.
from django.contrib import admin

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class SignUp(models.Model):
    first_name = models.CharField(max_length=120,null=True,blank=True)
    last_name = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return smart_unicode(self.email)


class Tag(models.Model):
    #incentiveID = models.ForeignKey(Incentive,related_name="tags")
    tagID= models.IntegerField(null=False)
    tagName = models.CharField(max_length=100)

    # class Meta:
    #     unique_together = ('incentiveID','tagID')


    def __unicode__(self):
         return '%d: %s' % (self.tagID, self.tagName)

class Incentive(models.Model):
    owner = models.ForeignKey('auth.User', related_name='incentive')
   # highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    schemeID= models.IntegerField(default=0)
    schemeName = models.CharField(max_length=100, blank=True, default='')
    typeID=models.IntegerField(default=0)
    typeName=models.CharField(max_length=100,blank=True,default='')
    status=models.BooleanField(default=True)
    ordinal=models.IntegerField(null=True,blank=True,default=0)
    modeID=models.IntegerField(default=0)
    presentationDuration=models.DateTimeField(auto_now_add=True)
    groupIncentive=models.BooleanField(default=False)
    text =models.TextField()
    tags=models.ManyToManyField(Tag, null=True, blank=True)
    #image =models.ImageField()
    condition=models.TextField()
    # tags = models.ManyToManyField(Tag, null=True, blank=True,related_name="tags")
   # code = models.TextField()
  #  language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    #email = models.TextField()

    class Meta:
        ordering = ('created',)

    def user_can_manage_me(self, user):
        return user == self.owner
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        #lexer = get_lexer_by_name(self.language)
        #options = self.schemeName and {'title': self.schemeName} or {}
       # formatter = HtmlFormatter(text=self.text,
      #                        full=True, **options)
     #   self.highlighted = highlight(self.schemeName, lexer, formatter)
        super(Incentive, self).save(*args, **kwargs)

    def __unicode__(self):
         return '%d: %s' % (self.schemeID, self.schemeName)

class Document(models.Model):
    owner = models.ForeignKey('auth.User', related_name='document')
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')