from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sensors.models import Sensor, Reading
from datetime import datetime
import csv
from django.db import transaction
import os

class Command(BaseCommand):
    help = "Seed database with one user, five sensors, and readings from CSV"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
        
            user, created = User.objects.get_or_create(
                username="seed_user",
                defaults={"email": "seed_user@test.com"}
            )
            if created:
                user.set_password("secret123")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(f"User already exists: {user.username}")

           
            sensors_data = [
                ("device-001", "EnviroSense"),
                ("device-002", "ClimaTrack"),
                ("device-003", "AeroMonitor"),
                ("device-004", "HydroTherm"),
                ("device-005", "EcoStat"),
            ]

            sensors = {}
            for name, model in sensors_data:
                sensor, _ = Sensor.objects.get_or_create(
                    owner=user,
                    name=name,
                    model=model,
                    defaults={"description": f"{model} description"}
                )
                sensors[name] = sensor
                self.stdout.write(self.style.SUCCESS(f"Created sensor: {sensor.name}"))

            # CSV
            csv_file = "sensor_readings_wide.csv"
            if not os.path.exists(csv_file):
                self.stdout.write(self.style.WARNING(f"CSV file not found: {csv_file}"))
                return

            with open(csv_file, newline="") as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    sensor_name = row.get("device_id")
                    sensor = sensors.get(sensor_name)
                    if not sensor:
                        continue
                    try:
                        
                        ts_str = row["timestamp"].replace(" ", "T")
                        timestamp = datetime.fromisoformat(ts_str)
                        Reading.objects.create(
                            sensor=sensor,
                            temperature=float(row["temperature"]),
                            humidity=float(row["humidity"]),
                            timestamp=timestamp
                        )
                        count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating reading: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Loaded {count} readings from CSV"))
            self.stdout.write
