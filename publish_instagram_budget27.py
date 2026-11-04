"""
[Q&A 스티커 스타일·1:1·6장] 2027 예산안 재생에너지 2.8조 카드뉴스 - 인스타그램 캐러셀 자동 게시
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
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/budget27_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/budget27_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/budget27_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/budget27_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/budget27_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/budget27_06.png",
]

CAPTION = """내년 재생에너지 예산, 2.8조로 2배 늘립니다 ☀️

대통령이 11/2 국회 시정연설에서 '햇빛소득마을 확산 등 재생에너지 확대에 2조8000억원 투자'를 밝혔습니다. (2027년도 예산안)

📈 태양광·햇빛소득마을 등 투자: 1.3조 → 2.8조원
🏘 햇빛소득마을: 700곳 → 2,200곳 (신규 1,500곳, 마을당 평균 650kW)
🏭 공장지붕·영농형 태양광 등 보급 지원: 0.9조 → 1.8조원
💳 재생에너지 금융지원: 0.65조 → 1.5조원 (태양광 2.1GW·풍력 1.2GW 목표)

※ 아직 국회 심의 단계(법정 처리 기한 12/2)로, 확정 금액은 심의 결과에 따라 달라질 수 있습니다.

(주)솔라워크는 태양광 정책·수익성 정보를 쉽게 정리해드립니다.
카드 넘겨서 확인하세요 →

출처: 대통령 시정연설(2026.11.2), 기획예산처 예산안, 아시아경제(2026.9.1)

#태양광 #재생에너지 #2027예산 #햇빛소득마을 #영농형태양광 #공장지붕태양광 #에너지대전환 #태양광정책 #신재생에너지 #솔라워크"""

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
    print("1) 캐러셀 아이템(이미지 6장) 컨테이너 생성 중...")
    child_ids = []
    for i, url in enumerate(IMAGE_URLS, start=1):
        res = api_post(f"{IG_USER_ID}/media", {
            "image_url": url,
            "is_carousel_item": "true",
            "access_token": ACCESS_TOKEN,
        })
        child_ids.append(res["id"])
        print(f"   - {i}/6 완료: {res['id']}")
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
