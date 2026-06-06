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
@router.get("/gps/rest-area")
def get_rest_area_info():

    rest_api_key = os.getenv("REST_AREA_API_KEY")

    url = "https://api.data.go.kr/openapi/tn_pubr_public_rest_area_api"

    params = {
        "serviceKey": rest_api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "type": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    items = data["response"]["body"]["items"]

    return {
        "message": "전국휴게소 API 연동 성공",
        "count": len(items),
        "rest_areas": items
    }
@router.get("/gps/sleep-shelter")
def get_sleep_shelter():

    df = pd.read_csv("한국도로공사_졸음쉼터.csv")

    shelters = df.head(10).to_dict(orient="records")

    return {
        "message": "졸음쉼터 CSV 로드 성공",
        "count": len(shelters),
        "sleep_shelters": shelters
    }
