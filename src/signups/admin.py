from django.contrib import admin

# Register your models here.
from .models import SignUp,Incentive,Tag


class SignUpAdmin(admin.ModelAdmin):
    class Meta:
        model = SignUp
    
admin.site.register(SignUp,SignUpAdmin)

class IncentiveAdmin(admin.ModelAdmin):
    class Meta:
        model = Incentive

admin.site.register(Incentive,IncentiveAdmin)

class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag

admin.site.register(Tag,TagAdmin)