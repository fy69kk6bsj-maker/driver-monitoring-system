# API Interface 확정 문서
> 이 형식에 맞춰서 각자 구현하면 됩니다. 임의로 변경 금지.

## POST /image/analyze
**담당: 02번**

Request:
- image_base64: string (JPEG 640×480)
- user_id: string
- session_id: string

Response:
- visual_anger_score: float (0~1)
- visual_drowsiness_score: float (0~1)
- blink_rate: float
- eye_closed_duration: float
- yawn_score: float
- anger_trend: string (rising/stable/falling)
- persistent_risk: bool

## POST /audio/analyze
**담당: 04번**
...

(이하 동일하게 전부 작성)
