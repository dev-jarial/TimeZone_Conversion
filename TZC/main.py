from fastapi import FastAPI
from datetime import datetime, timedelta
import pytz

def format_datetime(dt, tz):
    formatted_dt = dt.astimezone(pytz.timezone(tz))
    return formatted_dt.strftime("%Y-%m-%d %I:%M:%S %p")


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
        converted_time_gmt = format_datetime(converted_dt, 'GMT')
        converted_time_mdt = format_datetime(converted_dt, 'US/Mountain')
        converted_time_utc = format_datetime(converted_dt, 'UTC')

        return {
            "from_country": from_country,
            "from_timezone": from_timezone,
            "to_country": to_country,
            "to_timezone": to_timezone,
            "datetime": datetime_str,
            "converted_time": converted_time,
            "converted_time_gmt": converted_time_gmt,
            "converted_time_mdt": converted_time_mdt,
            "converted_time_utc": converted_time_utc
        }
    except ValueError:
        return {"error": "Invalid datetime format provided."}

# here is the test url for get-by-name
# http://127.0.0.1:8000/convert_timezone?from_country=IN&from_timezone=Asia/Kolkata&to_country=PK&to_timezone=Asia/Karachi&datetime_str=2023-05-11T12:00:00


def convert_gmt_time(gmt_time: str, from_offset: timedelta, to_offset: timedelta) -> str:
    # Parse the GMT time string
    gmt_dt = datetime.strptime(gmt_time, "%Y-%m-%dT%H:%M:%S")

    # Apply the from_offset to convert GMT time to local time
    local_time = gmt_dt - from_offset

    # Apply the to_offset to convert local time to the target offset
    to_time = local_time + to_offset

    # Format the converted time as a string
    converted_time = to_time.strftime("%Y-%m-%dT%H:%M:%S")

    return converted_time

@app.get("/convert_timezone_by_gmt")
def convert_timezone_by_gmt(gmt_time: str, from_offset: str, to_offset: str):
    try:
        from_offset_parts = from_offset.split(":")
        from_offset = timedelta(hours=int(from_offset_parts[0]), minutes=int(from_offset_parts[1]))

        to_offset_parts = to_offset.split(":")
        to_offset = timedelta(hours=int(to_offset_parts[0]), minutes=int(to_offset_parts[1]))

        converted_time = convert_gmt_time(gmt_time, from_offset, to_offset)

        return {
            "gmt_time": gmt_time,
            "from_offset": from_offset.total_seconds(),
            "to_offset": to_offset.total_seconds(),
            "converted_time": converted_time
        }
    except ValueError:
        return {"error": "Invalid input format provided."}
    
# url for GMT coversion type
# http://127.0.0.1:8000/convert_timezone_by_gmt?gmt_time=2023-05-12T05:27:00&from_offset=-04:00&to_offset=+05:30

