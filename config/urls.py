from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI

from app.accounts.api.views import router as account_router

api = NinjaAPI(title='Music YouTube API', docs_url='/docs/')


@api.get('/health', tags=['Health'])
def health_check(request):
    return {'msg': 'OK'}


api.add_router('/account', account_router, tags=['Accounts'])


urlpatterns = [path('admin/', admin.site.urls), path('api/v1/', api.urls)]
