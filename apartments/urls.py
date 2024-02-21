from django.urls import path
from .views import (
    ApartmentView,
    ApartmentDetailView,
    UserDetailsView,
)

urlpatterns = [
    path("me/", UserDetailsView.as_view(), name="get_user_details"),
    path("apartments/", ApartmentView.as_view(), name="get_apartments"),
    path(
        "apartments/<int:apartment_id>/",
        ApartmentDetailView.as_view(),
        name="get_apartment_details",
    ),
]
