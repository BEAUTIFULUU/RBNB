from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apartments.views import (
    ApartmentView,
    ApartmentDetailView,
    ApartmentAdvertisementView,
    ApartmentAdvertisementDetailView,
)
from images.views import AdvertisementImageView, AdvertisementImageDetailView
from visits.views import CreateVisitView, OwnerVisitView, TenantVisitView
from livehere import settings

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("apartments/", ApartmentView.as_view(), name="get_apartments"),
    path(
        "me/visits/",
        TenantVisitView.as_view(),
        name="get_tenant_apartment_visits",
    ),
    path(
        "apartments/<uuid:apartment_id>/",
        ApartmentDetailView.as_view(),
        name="get_apartment_details",
    ),
    path(
        "apartments/<uuid:apartment_id>/visit/",
        CreateVisitView.as_view(),
        name="post_apartment_visit",
    ),
    path(
        "me/advertisements/",
        ApartmentAdvertisementView.as_view(),
        name="get_owner_advertisements",
    ),
    path(
        "me/advertisements/visits/",
        OwnerVisitView.as_view(),
        name="get_owner_advertisements_visits",
    ),
    path(
        "me/advertisements/<uuid:advertisement_id>/",
        ApartmentAdvertisementDetailView.as_view(),
        name="get_owner_advertisement_details",
    ),
    path(
        "me/advertisements/<uuid:advertisement_id>/images/",
        AdvertisementImageView.as_view(),
        name="upload_apartment_images",
    ),
    path(
        "me/advertisements/<uuid:advertisement_id>/images/<uuid:image_id>/",
        AdvertisementImageDetailView.as_view(),
        name="get_advertisement_image_details",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
