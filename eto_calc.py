import math


def calculate_ET0(Latitude, Altitude, Date, Tmin, Tmax):
    Δ = 0.1708
    Rn = 8.09
    γ = 0.06316
    Tmean = 23.1
    u2 =  2.00
    es_ea = 1.207

    if (isinstance(Latitude, float) and isinstance(Altitude, float) and
            isinstance(Date, float) and isinstance(Tmin, float) and isinstance(Tmax, float)):
        if isinstance(Δ, float) and isinstance(Rn, float) and isinstance(γ, float) and isinstance(Tmean, float):
            if isinstance(u2, float) and isinstance(es_ea, float):
                u2 = max(u2, 0.5)
                ET0 = (0.408 * Δ * (Rn - 0) + γ * (900 / (Tmean + 273)) * u2 * es_ea) / (Δ + γ * (1 + 0.34 * u2))
                return ET0

    return None


# # Example usage
# Latitude = 37.5
# Altitude = 500.0
# Date = 7.0
# Tmin = 10.0
# Tmax = 30.0
#
# ET0 = calculate_ET0(Latitude, Altitude, Date, Tmin, Tmax)
# if ET0 is not None:
#     print("Reference Evapotranspiration (ET0):", ET0)
# else:
#     print("Invalid input values.")
