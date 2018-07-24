from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user', views.UserAPIView)
router.register('login', views.LoginViewSet, base_name='login')
router.register('user/(?P<id>[^/.]+)/etherapi',views.UpdateEtherSet, base_name='postEtherData')
router.register('user/(?P<id>[^/.]+)/etherinfo',views.GetInfoFromEtherscan, base_name='getInfoEther')


urlpatterns = [
    url('^',include(router.urls)),
    path('v2/user/', views.UserView.as_view()),
    path('v2/user/info/', views.UserEtherView.as_view())
]

