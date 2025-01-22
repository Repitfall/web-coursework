"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from django.conf import settings
from delivery import views
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import debug_toolbar

router = routers.SimpleRouter()
router.register("users", views.UserViewSet)
router.register("addresses", views.UserAddressViewSet)
router.register("couriers", views.CourierViewSet)
router.register("restaurants", views.RestaurantViewSet)
router.register("groups", views.RestaurantGroupViewSet)
router.register("dishes", views.RestaurantDishViewSet)
router.register("orders", views.OrderViewSet)
router.register("orderdishes", views.OrderDishViewSet)
router.register("tickets", views.TicketViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("search/", views.search, name="search"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("dish/<int:id_dish>/", views.index, name="dish"),
    path('dish/<int:id_dish>/comment_add/', views.comment_add, name='comment_add'),
    path('comment/<int:id_comment>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:id_comment>/delete/', views.comment_delete, name='comment_delete'),
    path("<slug:restaurant_slug>/", views.index, name="restaurant_list"),
    path("<slug:restaurant_slug>/<slug:group_slug>", views.index, name="group_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
