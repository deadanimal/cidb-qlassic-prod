from django.conf import settings
from django.conf.urls import include, url
from django.contrib.gis import admin

from rest_framework import routers
from rest_framework_extensions.routers import NestedRouterMixin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from users.views_api import (
    MyTokenObtainPairView
)

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass

router = NestedDefaultRouter()

# Users app
from users.views_api import (
    CustomUserViewSet,
    AssessorViewSet
)
users_router = router.register(
    'users', CustomUserViewSet
)
users_router = router.register(
    'assessors', AssessorViewSet
)
# Is Alive
from users.views_api import (
    IsAlive,
    # LoginView,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # REST
    url(r'api/v1/', include(router.urls)),
    url(r'auth/', include('rest_auth.urls')),
    url(r'auth/registration/', include('rest_auth.registration.urls')),
    # url(r'auth/login/', LoginView.as_view(), name='api_login'),

    url('isAlive/', IsAlive.as_view(), name='isAlive'),
    url('auth/obtain/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# CRON JOBS
from api.schedulers import start_jobs
start_jobs()