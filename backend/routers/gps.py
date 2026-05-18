from fastapi import APIRouter
import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/gps/test")
def gps_test():
    return {
        "lat": 37.5665,
        "lng": 126.9780,
        "status": "GPS API SUCCESS"
    }

@router.get("/gps/data")
def get_gps_data():
    df = pd.read_csv("gps_data.csv")
    return df.to_dict(orient="records")

@router.get("/gps/traffic")
def get_traffic_info():
    api_key = os.getenv("TRAFFIC_API_KEY")

    df = pd.read_csv("gps_data.csv")
    latest = df.iloc[-1]

    lat = float(latest["lat"])
    lng = float(latest["lng"])

    url = "https://openapi.its.go.kr:9443/trafficInfo"

    params = {
        "apiKey": api_key,
        "type": "all",
        "routeNo": "",
        "drcType": "all",
        "minX": lng - 0.02,
        "maxX": lng + 0.02,
        "minY": lat - 0.02,
        "maxY": lat + 0.02,
        "getType": "json"
    }

    response = requests.get(url, params=params, timeout=10)

    return {
        "latest_gps": {
            "lat": lat,
            "lng": lng
        },
        "request_url": response.url,
        "status_code": response.status_code,
        "traffic_response": response.json()
    }
