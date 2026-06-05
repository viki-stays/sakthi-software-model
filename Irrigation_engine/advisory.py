def irrigation_advisory(
    temperature,
    humidity,
    soil_moisture,
    rain_forecast,
    wind_speed,
    crop_type
):

    if soil_moisture > 60:
        return {
            "water_today": "No",
            "reason": "Soil moisture is sufficient",
            "suggested_water": "0 L/m²"
        }

    if rain_forecast > 60:
        return {
            "water_today": "No",
            "reason": "Rain expected soon",
            "suggested_water": "0 L/m²"
        }

    water_needed = 5

    if temperature > 35:
        water_needed += 2

    if wind_speed > 15:
        water_needed += 1

    return {
        "water_today": "Yes",
        "reason": "Soil is dry and no significant rain expected",
        "suggested_water": f"{water_needed} L/m²"
    }


# Example Test

result = irrigation_advisory(
    temperature=32,
    humidity=70,
    soil_moisture=40,
    rain_forecast=20,
    wind_speed=10,
    crop_type="Tomato"
)

result = irrigation_advisory(
    temperature=38,
    humidity=50,
    soil_moisture=20,
    rain_forecast=10,
    wind_speed=20,
    crop_type="Tomato"
)

print("\nSAKTHI Irrigation Advisory")
print("--------------------------")
print("Water Today :", result["water_today"])
print("Reason      :", result["reason"])
print("Suggested   :", result["suggested_water"])
