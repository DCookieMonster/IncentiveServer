from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets

# Register your models here.
from .models import SignUp,Incentive,Tag,Document
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class SignUpAdmin(admin.ModelAdmin):
    class Meta:
        model = SignUp

import logging
logger = logging.getLogger(__name__)
# admin.site.register(SignUp,SignUpAdmin)

class IncentiveAdmin(admin.ModelAdmin):
    list_display = ("schemeID","schemeName")
    class Meta:
        model = Incentive
    def get_form(self, request, obj=None, **kwargs):
            logger.info("%s is seeing: %s" % (request.user,obj))
            return super(IncentiveAdmin, self).get_form(request, obj=None, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj==None or request.user == obj.owner or request.user.is_superuser:
            return self.readonly_fields

        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
        def save_model(self, request, obj, form, change):
            super(IncentiveAdmin, self).save_model(request, obj, form, change)

admin.site.register(Incentive, IncentiveAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("docfile","owner")
    class Meta:
        model = Document
    def get_form(self, request, obj=None, **kwargs):
            logger.info("%s is seeing: %s" % (request.user,obj))
            return super(DocumentAdmin, self).get_form(request, obj=None, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj==None or request.user == obj.owner or request.user.is_superuser:
            return self.readonly_fields

        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
        def save_model(self, request, obj, form, change):
            super(DocumentAdmin, self).save_model(request, obj, form, change)
admin.site.register(Document,DocumentAdmin)

class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user == obj.owner or request.user.is_superuser:
    #         return self.readonly_fields
    #
    #     if self.declared_fieldsets:
    #         return flatten_fieldsets(self.declared_fieldsets)
    #     else:
    #         return list(set(
    #             [field.name for field in self.opts.local_fields] +
    #             [field.name for field in self.opts.local_many_to_many]
    #         ))

admin.site.register(Tag,TagAdmin)