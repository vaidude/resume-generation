# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.from .models import reg
from .models import Transaction
from .models import *

# Register your models here.
admin.site.register(Reg)
admin.site.register(Transaction)
admin.site.register(Resume)
admin.site.register(job_provider)
admin.site.register(JobApplication)
admin.site.register(Exam)

admin.site.register(Addjob)
admin.site.register(Feedback)