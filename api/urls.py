from django.urls import path, include
from django.conf.urls import url
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

# Views
from .views import (
    QlassicScoreViewSet, 
    QlassicInformationViewSet,
    ProjectInfoViewSet,
    UserViewSet,

)

# from api.soap.create_transaction import test_create_transaction
from api.soap.get_contractor import test_request_contractor

from .schedulers import start_jobs

# Routers provide an easy way of automatically determining the URL conf.
class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass
router = NestedDefaultRouter()

qlassic_score_router = router.register('qlassic-score', QlassicScoreViewSet, 'qlassic-score')
qlassic_information_router = router.register('qlassic-information', QlassicInformationViewSet, 'qlassic-information')
project_info_router = router.register('project-info', ProjectInfoViewSet)
user_router = router.register('user', UserViewSet)

from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # REST
    path(r'api/v1/', include(router.urls)),
    url(r'auth/', include('rest_auth.urls')),
    url(r'auth/registration/', include('rest_auth.registration.urls')),

    url('auth/obtain/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # SOAP
    # path('soap/create-transaction/', views.test_create_transaction, name='soap_test_create_transaction'),
    # path('soap/contractor/', test_request_contractor, name='soap_contractor'),
]

# CRON JOBS
# start_jobs()