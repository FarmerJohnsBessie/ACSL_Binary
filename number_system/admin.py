from django.contrib import admin
from .models import Profile, SolverProfile, DailyAPICallCount, Subscription

# Register your models here.
admin.site.register(Profile)
admin.site.register(SolverProfile)
admin.site.register(DailyAPICallCount)
admin.site.register(Subscription)