"""
[네이비 프리미엄·4:5·7장] LH 공동주택 요금상계거래 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_grid.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/lhnet_07.png",
]

CAPTION = """아파트 태양광, 남는 전기도 요금에서 뺍니다 ☀️

LH가 공동주택 단지에 처음으로 '요금상계거래'를 도입했습니다.

📍 세종 산울마을 4단지 (행복주택 238세대)
⚡ 단지 태양광 246kW (세대당 1,035W)
📊 월평균 발전량이 사용량의 49.1%
💰 가구당 월 약 8,000원 추가 절감 예상 (LH 예상치)

※ 한전과 협의해 적용 가능한 단지를 검토하는 단계이며, 확대 일정은 정해지지 않았습니다.

(주)솔라워크는 태양광 사업·정책·수익성 정보를 쉽게 정리해드립니다.
카드 넘겨서 자세히 확인하세요 →

출처: 파이낸셜뉴스(2026.11.03), LH

#태양광 #요금상계거래 #LH #공동주택태양광 #ZEB #제로에너지건축물 #재생에너지 #신재생에너지 #태양광시공 #솔라워크"""

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
    print("1) 캐러셀 아이템(이미지 7장) 컨테이너 생성 중...")
    child_ids = []
    for i, url in enumerate(IMAGE_URLS, start=1):
        res = api_post(f"{IG_USER_ID}/media", {
            "image_url": url,
            "is_carousel_item": "true",
            "access_token": ACCESS_TOKEN,
        })
        child_ids.append(res["id"])
        print(f"   - {i}/7 완료: {res['id']}")
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
