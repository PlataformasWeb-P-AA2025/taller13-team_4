# urls.py
from rest_framework import routers
from serviciosWeb.views import EdificioViewSet, DepartamentoViewSet

router = routers.DefaultRouter()
router.register(r'edificios', EdificioViewSet)
router.register(r'departamentos', DepartamentoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
