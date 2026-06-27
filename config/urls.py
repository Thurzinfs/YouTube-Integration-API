from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI

api = NinjaAPI(title='Music YouTube API', docs_url='/docs/')


@api.get('/health', tags=['Health'])
def health_check(request):
    return {'msg': 'OK'}


urlpatterns = [path('admin/', admin.site.urls), path('api/v1/', api.urls)]
