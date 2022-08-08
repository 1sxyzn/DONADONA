from django.contrib import admin
from .models import *


class TimeInline(admin.TabularInline):
    model = Time


class DayAdmin(admin.ModelAdmin):
    inlines = (TimeInline,)


class AddressDetailInline(admin.TabularInline):
    model = AddressDetail


class AddressAdmin(admin.ModelAdmin):
    inlines = (AddressDetailInline,)


class AbilityDetailInline(admin.TabularInline):
    model = AbilityDetail


class AbilityAdmin(admin.ModelAdmin):
    inlines = (AbilityDetailInline,)


admin.site.register(Day, DayAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Ability, AbilityAdmin)

admin.site.register(User)
admin.site.register(Post)
