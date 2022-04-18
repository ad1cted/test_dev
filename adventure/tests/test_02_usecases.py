import pytest
from django.utils import timezone

from adventure import models, notifiers, repositories, usecases


#########
# Mocks #
#########


class MockJourneyRepository(repositories.JourneyRepository):
    def get_or_create_car(self) -> models.VehicleType:
        return models.VehicleType(name="car", max_capacity=4)

    def create_vehicle(
            self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle) -> models.Journey:
        return models.Journey(vehicle=vehicle, start=timezone.now().date())

    def stop_journey(self, journey: models.Journey) -> models.Journey:
        return models.Journey(vehicle=journey.vehicle, end=timezone.now().date())


class MockNotifier(notifiers.Notifier):
    def send_notifications(self, journey: models.Journey) -> None:
        pass


#########
# Tests #
#########


class TestStartJourney:
    def test_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 2}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        journey = usecase.execute()

        assert journey.vehicle.name == "Kitt"

    def test_cant_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 6}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        with pytest.raises(usecases.StartJourney.CantStart):
            journey = usecase.execute()


class TestStopJourney:
    def test_stop_journey(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 2}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        journey = usecase.execute()
        stopped_journey = repo.stop_journey(journey)
        #assert stopped_journey.end < timezone.now().date()  #nope
        assert stopped_journey.is_finished
