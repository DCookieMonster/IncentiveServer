from django.db import models
from django.utils.encoding  import smart_unicode
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
# Create your models here.

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
    

class Incentive(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets')
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    email = models.TextField()

    class Meta:
        ordering = ('created',)
    
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(email=self.email,
                              full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Incentive, self).save(*args, **kwargs)



    
