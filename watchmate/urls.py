from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view 

schema_view = get_swagger_view(title='Movie API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist_app.api.urls')),
    # path('api-auth', include('rest_framework.urls')),
    path('account/', include('user_app.api.urls')),
    path('api/doc/', schema_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
