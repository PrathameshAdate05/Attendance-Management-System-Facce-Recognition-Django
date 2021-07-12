from django.contrib import admin

# Register your models here.
from .models import facultyReg
from .models import studentreg
from .models import mon_reports
admin.site.register(facultyReg)
admin.site.register(studentreg)
admin.site.register(mon_reports)