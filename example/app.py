from fastapi import FastAPI
from django.apps import apps
from django.conf import settings

apps.populate(settings.INSTALLED_APPS)

app = FastAPI(title='Fast ORM Example')

from example.views import example_router  # noqa: E402
app.include_router(prefix='/examples', router=example_router)
