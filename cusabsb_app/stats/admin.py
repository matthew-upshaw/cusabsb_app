from django.contrib import admin

from .models import (
    Batter,
    Pitcher,
    Fielder,
)

admin.site.register(Batter)
admin.site.register(Pitcher)
admin.site.register(Fielder)
