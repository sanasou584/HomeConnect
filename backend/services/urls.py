from django.urls import path
from . import views

urlpatterns = [
    path("", views.ServiceListView.as_view(), name="service_list"),
    path("espace-prestataire/", views.ProviderDashboardView.as_view(), name="provider_dashboard"),
    path("nouveau/", views.ServiceCreateView.as_view(), name="service_create"),
    path("<int:pk>/modifier/", views.ServiceUpdateView.as_view(), name="service_update"),
    path("<int:pk>/supprimer/", views.ServiceDeleteView.as_view(), name="service_delete"),
]