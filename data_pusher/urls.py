from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import AccountViewSet, DestinationViewSet, handle_incoming_data, homepage

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('server/incoming_data/', handle_incoming_data),
    path('', homepage),  # Add this line for the homepage
]
