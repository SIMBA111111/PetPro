from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("userapp.urls")),
    path("chat/", include("chat.urls")),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path("__debug__/", include("debug_toolbar.urls")),
]
