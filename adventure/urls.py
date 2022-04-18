from django.urls import path

from adventure import views

urlpatterns = [
    path("create-vehicle/", views.CreateVehicleAPIView.as_view()),
    path("create-service-area/", views.CreateServiceAreaAPIView.as_view()),
    path("start/", views.StartJourneyAPIView.as_view()),
    path("get-vehicle/", views.GetVehicleAPIView.as_view()),
    path("get-vehicle/<str:license>", views.GetVehicleAPIView.as_view()),

]
