import pytest
from django.core import mail

from adventure import models, notifiers, repositories, usecases, views

from .test_02_usecases import MockJourneyRepository

#########
# Tests #
#########
from ..views import CreateVehicleAPIView


class TestRepository:
    def test_create_vehicle(self, mocker):
        mocker.patch.object(models.Vehicle.objects, "create")
        repo = repositories.JourneyRepository()
        car = models.VehicleType()
        repo.create_vehicle(name="a", passengers=10, vehicle_type=car)
        assert models.Vehicle.objects.create.called


class TestNotifier:
    def test_send_notification(self, mocker):
        mocker.patch.object(mail, "send_mail")
        notifier = notifiers.Notifier()
        notifier.send_notifications(models.Journey())
        assert mail.send_mail.called


class TestCreateVehicleAPIView:
    def test_create(self, client, mocker):
        vehicle_type = models.VehicleType(name="car")
        mocker.patch.object(
            models.VehicleType.objects, "get", return_value=vehicle_type
        )
        mocker.patch.object(
            models.Vehicle.objects,
            "create",
            return_value=models.Vehicle(
                id=1, name="Kitt", passengers=4, vehicle_type=vehicle_type
            ),
        )
        payload = {"name": "Kitt", "passengers": 4, "vehicle_type": "car"}
        response = client.post("/api/adventure/create-vehicle/", payload)
        assert response.status_code == 201


class TestCreateServiceAreaAPIView:
    def test_create(self, client, mocker):
        mocker.patch.object(
            models.ServiceArea.objects,
            "create",
            return_value=models.ServiceArea(
                id=1, kilometer=60, gas_price=784
            ),
        )

        payload = {"kilometer": 60, "gas_price": 784}
        response = client.post("/api/adventure/create-service-area/", payload)
        assert response.status_code == 201


@pytest.mark.django_db
class TestGetVehicleAPIView:
    def test_get(self, client, mocker):
        vehicle_type = models.VehicleType(name="car")
        mocker.patch.object(
            models.VehicleType.objects, "get", return_value=vehicle_type
        )
        mocker.patch.object(
            models.Vehicle.objects,
            "create",
            return_value=models.Vehicle(
                id=1, name="Kitt", passengers=4, vehicle_type=vehicle_type
            ),
        )
        assert client.get("/api/adventure/get-vehicle/").status_code == 200

    def test_get_by_license_plate(self, client, mocker):
        # TODO: Implement endpoint to get vehicle data by license plate
        pass


@pytest.mark.skip  # Remove
class TestGetServiceAreaAPIView:
    def test_get(self, client, mocker):
        # TODO: Implement endpoint to get full list of service areas
        pass

    def test_get_by_kilometer(self, client, mocker):
        # TODO: Implement endpoint to get service area by kilometer
        pass


class TestStartJourneyAPIView:
    def test_api(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 2}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 201

    def test_api_fail(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 6}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 400
