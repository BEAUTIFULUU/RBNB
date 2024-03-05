from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apartments.views import (
    ApartmentView,
    ApartmentDetailView,
    ApartmentAdvertisementView,
    ApartmentAdvertisementDetailView,
)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("apartments/", ApartmentView.as_view(), name="get_apartments"),
    path(
        "apartments/<int:apartment_id>/",
        ApartmentDetailView.as_view(),
        name="get_apartment_details",
    ),
    path(
        "me/advertisements/",
        ApartmentAdvertisementView.as_view(),
        name="get_owner_advertisements",
    ),
    path(
        "me/advertisements/<int:advertisement_id>/",
        ApartmentAdvertisementDetailView.as_view(),
        name="get_owner_advertisement_details",
    ),
]
