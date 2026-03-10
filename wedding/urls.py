from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("Dashboard/", lambda request: redirect("/login/")),
    path("dashboard/convidados/adicionar/", views.add_guest, name="add_guest"),
    path("dashboard/convidados/<int:guest_id>/editar/", views.edit_guest, name="edit_guest"),
    path("confirmar-presenca/", views.public_rsvp, name="public_rsvp"),
    path("rsvp/<uuid:token>/", views.rsvp_confirm, name="rsvp_confirm"),
]