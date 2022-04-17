import math
import re
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)
    fuel_efficiency = models.DecimalField(max_digits=6, decimal_places=2)  # in km/L
    fuel_tank_size = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        # Limitation: Fixed to 2 seats for row, this is not scalable but it's fast
        partial_row, fullrows = math.modf(self.passengers / 2)  # separate full rows from partials
        seat_distribution = [[True, True] for i in range(int(fullrows))]

        if partial_row > 0:
            seat_distribution.append([True, False])

        return seat_distribution


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        return (self.end != None and self.end <= date.today())


def validate_number_plate(number_plate: str) -> bool:
    list_number_plate = number_plate.split("-")
    if list_number_plate[0].isalpha()and list_number_plate[1].isnumeric() and list_number_plate[2].isnumeric():
        return True
    return False

class ServiceArea(models.Model):
    kilometer = models.IntegerField()
    gas_price = models.PositiveIntegerField()
    left_station = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,related_name='left')
    right_station = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,related_name='right')

    def validate_left(self):
        if self.left_station == None:
            return True

        if self.kilometer <= self.left_station.kilometer:
            raise ValidationError({'left_station': 'Stations to the left should be placed before the station.'})

    def validate_right(self):
        if self.right_station == None:
            return True

        if self.kilometer >= self.right_station.kilometer:
            raise ValidationError({'right_station': 'Stations to the right should be placed after the station.'})

    def clean(self, *args, **kwargs):
        self.validate_left()
        self.validate_right()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
