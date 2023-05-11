from fastapi import FastAPI
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/convert_timezone")
def convert_timezone(from_country: str, from_timezone: str, to_country: str, to_timezone: str, datetime_str: str):
    try:
        from_tz = pytz.timezone(from_timezone)
        to_tz = pytz.timezone(to_timezone)

        # Parse the datetime string
        dt = datetime.fromisoformat(datetime_str)

        # Apply time zone conversion
        converted_dt = from_tz.localize(dt).astimezone(to_tz)

        # Format the converted datetime
        converted_time = converted_dt.strftime("%Y-%m-%d %I:%M:%S %p")

        return {
            "from_country": from_country,
            "from_timezone": from_timezone,
            "to_country": to_country,
            "to_timezone": to_timezone,
            "datetime": datetime_str,
            "converted_time": converted_time
        }
    except (pytz.UnknownTimeZoneError, ValueError):
        return {"error": "Invalid time zone or datetime format provided."}

# http://127.0.0.1:8000/convert_timezone?from_country=IN&from_timezone=Asia/Kolkata&to_country=PK&to_timezone=Asia/Karachi&datetime_str=2023-05-11T12:00:00

