# API Interface 확정 문서

> ⚠️ 이 문서는 확정된 입출력 형식입니다. 임의로 변경 금지.
> 변경이 필요하면 반드시 협의 후 수정하세요.

---

## 공통 규칙

- 모든 통신: HTTP REST (JSON)
- 이미지: Base64 인코딩, JPEG 640×480
- 음성: Base64 인코딩, WAV 16kHz
- 점수: 모두 float 0~1 범위
- 서버 주소: http://localhost:8000 (개발) / Railway URL (배포)

---

## POST /image/analyze
**담당: 02번 | 호출 주기: 0.5초**

### Request
```json
{
  "image_base64": "string",
  "user_id": "string",
  "session_id": "string"
}
```

### Response
```json
{
  "visual_anger_score": 0.0,
  "visual_drowsiness_score": 0.0,
  "blink_rate": 0.0,
  "eye_closed_duration": 0.0,
  "yawn_score": 0.0,
  "anger_trend": "stable",
  "persistent_risk": false
}
```

### 필드 설명
| 필드 | 타입 | 설명 |
|---|---|---|
| visual_anger_score | float | 표정 기반 분노 점수 (0~1) |
| visual_drowsiness_score | float | 눈/하품 기반 졸음 점수 (0~1) |
| blink_rate | float | 눈 깜빡임 빈도 |
| eye_closed_duration | float | 눈 감긴 지속 시간(초) |
| yawn_score | float | 하품 강도 (0~1) |
| anger_trend | string | rising / stable / falling |
| persistent_risk | bool | 30초 이상 위험 지속 여부 |

---

## POST /audio/analyze
**담당: 04번 | 호출 주기: 3초**

### Request
```json
{
  "audio_base64": "string",
  "user_id": "string",
  "session_id": "string"
}
```

### Response
```json
{
  "audio_anger_score": 0.0,
  "audio_stress_score": 0.0,
  "vibe_status": "calm",
  "transcribed_text": "string",
  "profanity_detected": false
}
```

### 필드 설명
| 필드 | 타입 | 설명 |
|---|---|---|
| audio_anger_score | float | 음성 기반 분노 점수 (0~1) |
| audio_stress_score | float | vibe_stress = 욕설×0.6 + 데시벨상승률×0.4 |
| vibe_status | string | calm / warning / danger |
| transcribed_text | string | Google STT 변환 텍스트 |
| profanity_detected | bool | BEEP! 키워드 감지 여부 |

---

## POST /gps/analyze
**담당: 03번 | 호출 주기: 3초**

### Request
```json
{
  "latitude": 0.0,
  "longitude": 0.0,
  "driving_duration_min": 0.0,
  "user_id": "string",
  "session_id": "string"
}
```

### Response
```json
{
  "speed_norm": 0.0,
  "traffic_density_score": 0.0,
  "driving_duration_norm": 0.0,
  "night_driving_risk": 0.0,
  "rest_area_distance_norm": 0.0,
  "nearest_rest_area": "string"
}
```

### 필드 설명
| 필드 | 타입 | 설명 |
|---|---|---|
| speed_norm | float | 속도 정규화 (0~1) |
| traffic_density_score | float | low=0.2 / medium=0.5 / high=0.9 |
| driving_duration_norm | float | 누적 운전 시간 정규화 |
| night_driving_risk | float | 06~18시=낮음 / 18~22시=중간 / 22~06시=높음 |
| rest_area_distance_norm | float | log 변환 정규화 거리 |
| nearest_rest_area | string | 가장 가까운 휴게소/졸음쉼터 이름 |

---

## POST /fusion/calculate
**담당: 01번 | 호출 주기: 3초**

### Request
```json
{
  "visual_anger_score": 0.0,
  "visual_drowsiness_score": 0.0,
  "audio_anger_score": 0.0,
  "audio_stress_score": 0.0,
  "gps_features": {
    "speed_norm": 0.0,
    "traffic_density_score": 0.0,
    "driving_duration_norm": 0.0,
    "night_driving_risk": 0.0,
    "rest_area_distance_norm": 0.0
  },
  "user_id": "string",
  "session_id": "string"
}
```

### Response
```json
{
  "anger_score": 0.0,
  "drowsiness_score": 0.0,
  "context_risk": 0.0,
  "final_risk": 0.0,
  "risk_level": "low",
  "primary_risk_type": "low_risk",
  "context_type": "normal",
  "intervention_urgency": 0.0,
  "intervention_feasibility": "rest_limited",
  "driving_context_features": {}
}
```

### 필드 설명
| 필드 | 타입 | 설명 |
|---|---|---|
| anger_score | float | α1×visual_anger + α2×audio_anger |
| drowsiness_score | float | visual_drowsiness_score (이미지 단독) |
| context_risk | float | GPS 기반 주행 문맥 위험도 |
| final_risk | float | 최종 위험도 (0~1) |
| risk_level | string | low / medium / high |
| primary_risk_type | string | anger / drowsiness / mixed / low_risk |
| context_type | string | fatigue_night_longdrive / anger_congested_traffic / normal 등 |
| intervention_urgency | float | 개입 긴급도 (η1×drowsiness + η2×anger) |
| intervention_feasibility | string | rest_possible / rest_possible_soon / rest_limited |

---

## POST /decision/decide
**담당: 01번 + 04번 | 호출 주기: fusion 결과 수신 후**

### Request
```json
{
  "fusion_result": {},
  "user_id": "string",
  "session_id": "string",
  "nearest_rest_area": "string",
  "anger_trend": "stable"
}
```

### Response
```json
{
  "response_text": "string",
  "action_type": "string",
  "action_intensity": "string",
  "system_action": "string",
  "ui_notification": "string",
  "safety_block": false
}
```

### 필드 설명
| 필드 | 타입 | 설명 |
|---|---|---|
| response_text | string | iOS TTS로 출력할 텍스트 |
| action_type | string | calming / alert / recovery / conversation / music |
| action_intensity | string | soft / moderate / strong |
| system_action | string | play_music / alert_sound / none |
| ui_notification | string | 화면에 표시할 알림 텍스트 |
| safety_block | bool | true면 대화 차단 (FinalRisk ≥ 0.7) |

---

## GET /user/{user_id}/profile
**담당: 03번**

### Response
```json
{
  "user_id": "string",
  "preferred_music_genre": "string",
  "conversation_style": "string",
  "preferred_voice_tone": "string",
  "anger_trigger_context": "string",
  "hobby": "string"
}
```

---

## POST /user/{user_id}/update
**담당: 03번**

### Request
```json
{
  "preferred_music_genre": "string",
  "conversation_style": "string",
  "preferred_voice_tone": "string",
  "anger_trigger_context": "string",
  "hobby": "string"
}
```

---

## POST /intervention/log
**담당: 03번**

### Request
```json
{
  "user_id": "string",
  "session_id": "string",
  "action_type": "string",
  "action_intensity": "string",
  "response_text": "string",
  "risk_before": 0.0,
  "risk_after": 0.0
}
```

---

## Fusion 가중치 초기값
AngerScore:
α1 = 0.6  (visual_anger)
α2 = 0.4  (audio_anger)
ContextRisk:
γ1 = 0.30  (speed_norm)
γ2 = 0.20  (traffic_density)
γ3 = 0.15  (driving_duration)
γ4 = 0.25  (night_driving_risk)
γ5 = 0.10  (rest_area_distance)
FinalRisk:
δ1 = 0.40  (anger_score)
δ2 = 0.40  (drowsiness_score)
δ3 = 0.20  (context_risk)
InterventionUrgency:
η1 = 0.60  (drowsiness)
η2 = 0.30  (anger)
η3 = 0.10  (context_risk)
vibe_stress:
w1 = 0.60  (욕설 감지)
w2 = 0.40  (데시벨 상승률)

## iOS 호출 순서 (매 사이클)
0.5초마다:
POST /image/analyze
3초마다:
POST /audio/analyze
POST /gps/analyze
POST /fusion/calculate  ← image + audio + gps 결과 합쳐서
POST /decision/decide   ← fusion 결과 받은 후
(필요 시) response_text → TTS 출력

## LLM 모델
- 모델: gpt-4o
- 용도: 개인화 응답 생성
- HIGH 위험 시: Rule-based 사용 (LLM 호출 안 함)
- MEDIUM/LOW 위험 시: OpenAI API 호출
