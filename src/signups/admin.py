from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets

# Register your models here.
from .models import SignUp,Incentive,Tag
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class SignUpAdmin(admin.ModelAdmin):
    class Meta:
        model = SignUp

    
# admin.site.register(SignUp,SignUpAdmin)

class IncentiveAdmin(admin.ModelAdmin):
    list_display = ("schemeID","schemeName")
    class Meta:
        model = Incentive

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

admin.site.register(Incentive,IncentiveAdmin)

class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag

    def get_readonly_fields(self, request, obj=None):
        if request.user == obj.owner or request.user.is_superuser:
            return self.readonly_fields

        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

admin.site.register(Tag,TagAdmin)