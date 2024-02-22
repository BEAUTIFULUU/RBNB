from django.urls import path
from .views import (
    ApartmentView,
    ApartmentDetailView,
    ApartmentAdvertiseView,
    ApartmentAdvertiseDetailView,
)

urlpatterns = [
    path("apartments/", ApartmentView.as_view(), name="get_apartments"),
    path(
        "apartments/<int:apartment_id>/",
        ApartmentDetailView.as_view(),
        name="get_apartment_details",
    ),
    path(
        "me/apartments_adv/",
        ApartmentAdvertiseView.as_view(),
        name="get_user_apartments",
    ),
    path(
        "me/apartments_adv/<int:apartment_id>/",
        ApartmentAdvertiseDetailView.as_view(),
        name="get_advertisement_details",
    ),
]
