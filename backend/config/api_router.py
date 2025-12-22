from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from recsa_challenge.users.api.views import UserViewSet
from recsa_challenge.appointments.api.views.appoinment_view import AppointmentViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register(r'appointments', AppointmentViewSet)


app_name = "api"
urlpatterns = router.urls
