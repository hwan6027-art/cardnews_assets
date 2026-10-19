"""
[에디토리얼 스타일] 인버터 지속운전 요건 국감 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_inverter.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/inverter_08.png",
]

CAPTION = """인버터 지속운전 요건, 20kW 이상으로 넓힌다는 계획.

10월 19일 기후에너지환경부 국정감사에서 김주영 의원은 전압·주파수 이상 시 태양광 인버터가 동시에 탈락하면 지난해 스페인·포르투갈 대정전과 같은 사고가 국내에서도 날 수 있다고 짚었습니다. 재생에너지 접속 용량 41.1GW 가운데 배전망 연결은 30.7GW로 약 75%입니다.

한국전력은 현재 90kW 이상 설비에 지속운전 성능을 보장해 왔고, 이를 20kW 이상으로 넓힐 계획이라고 답했습니다. 저전압·저주파수·고전압 대응(LVRT·LFRT·HVRT) 보완 계획은 2029년까지 수립해 추진 중이라고 밝혔습니다. 확정된 기준이 아니라 국감에서 제시된 계획입니다.

(주)솔라워크가 설치·운영 사업자를 위해 체크포인트를 정리했습니다. 내 인버터의 계통 대응 기능을 사양서로 확인하고, 신규 설치라면 인버터 선정 단계에서 먼저 점검하세요.

카드 넘겨서 실무 체크리스트를 확인하세요 →

#태양광 #인버터 #국정감사 #계통 #배전망 #재생에너지 #신재생에너지 #태양광사업 #태양광정책 #솔라워크"""

GRAPH_VERSION = "v21.0"
BASE = f"https://graph.instagram.com/{GRAPH_VERSION}"


def api_post(path, params):
    url = f"{BASE}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print("\n=== 메타 서버 실제 응답 (에러 원인) ===")
        print(error_body)
        print("=====================================\n")
        raise
    result = json.loads(body)
    if "error" in result:
        raise RuntimeError(f"API 오류: {result['error']}")
    return result


def main():
    print("1) 캐러셀 아이템(이미지 8장) 컨테이너 생성 중...")
    child_ids = []
    for i, url in enumerate(IMAGE_URLS, start=1):
        res = api_post(f"{IG_USER_ID}/media", {
            "image_url": url,
            "is_carousel_item": "true",
            "access_token": ACCESS_TOKEN,
        })
        child_ids.append(res["id"])
        print(f"   - {i}/8 완료: {res['id']}")
        time.sleep(1)

    print("2) 캐러셀 컨테이너 생성 중...")
    carousel = api_post(f"{IG_USER_ID}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(child_ids),
        "caption": CAPTION,
        "access_token": ACCESS_TOKEN,
    })
    creation_id = carousel["id"]
    print(f"   - 캐러셀 컨테이너 ID: {creation_id}")

    print("3) 처리 대기 중 (10초)...")
    time.sleep(10)

    print("4) 게시 중...")
    published = api_post(f"{IG_USER_ID}/media_publish", {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    })
    print(f"완료! 게시물 ID: {published['id']}")
    print(f"확인: https://www.instagram.com/solarwork_1/")


if __name__ == "__main__":
    main()
