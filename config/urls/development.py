from django.conf import settings
from django.conf.urls.static import static
from .base import *
import debug_toolbar

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('', include(debug_toolbar.urls)),
]
