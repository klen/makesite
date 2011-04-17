from django.contrib import admin
from django.db.models.loading import get_models, get_app


# Register main models in admin
app = get_app('main')
for model in get_models(app):
    admin.site.register(model, admin.ModelAdmin)
