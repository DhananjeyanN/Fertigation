import penmon.eto as pm
from datetime import datetime, date


class ETO:
    pm.CHECK_RADIATION_RANGE = False

    def __init__(self, elevation, latitude, wind_speed_height, t_min, t_max, sunlight_hours, wind_speed, humidity):
        self.elevation = elevation
        self.latitude = latitude
        self.wind_speed_height = wind_speed_height
        self.t_min = t_min
        self.t_max = t_max
        self.sunlight_hours = sunlight_hours
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.station = pm.Station(latitude=latitude, altitude=elevation)

    def calc(self):
        day = pm.Station(self.latitude, self.elevation, anemometer_height=10).get_day(
            day_number=238,
            temp_min=self.t_min,
            temp_max=self.t_max,
            wind_speed=self.wind_speed,
            humidity_mean=self.humidity,)
        print(day)
        return day.eto()

E = ETO(elevation=10, latitude=80.4, wind_speed_height=10, t_min=40, t_max=60, sunlight_hours=10, wind_speed=30, humidity=40)
print(E.calc())
