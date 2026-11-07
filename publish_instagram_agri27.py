"""
[딥그린 에디토리얼·4:5·7장] 영농형태양광사업법 12.17 시행 카드뉴스 - 인스타그램 캐러셀 자동 게시
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
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/agri27_07.png",
]

CAPTION = """농사 짓는 땅 위에서 전기도 버는 법 🌾☀️

'영농형태양광사업법'이 12월 17일 시행될 예정입니다. (농식품부, 11/6 상생한마당)

🌱 발전사업 부지 면적의 80% 이상에서 영농 의무
📐 차광률 30% 미만 제한 방향 · 구조물 높이 2.5m 이상 · 지주 간격 4m 이상
💰 100kW 시뮬레이션(업계 협회): 투자비 약 1.7억, 연 순수익 800~900만 원, 수익률 5% 안팎

※ 시뮬레이션은 REC 가중치 1.2 등을 가정한 업계 추정치입니다. RPS 개편에 따라 가중치가 달라질 수 있고, 정부는 우대 방안을 협의 중이나 확정되지 않았습니다. 세부 기준은 하위법령 마련 후 확정됩니다.

(주)솔라워크는 태양광 정책·수익성 정보를 쉽게 정리해드립니다.
카드 넘겨서 확인하세요 →

출처: 헤럴드경제(2026.11.6), 전자신문(2026.11.7), 농림축산식품부

#영농형태양광 #태양광 #영농형태양광사업법 #농촌태양광 #햇빛소득마을 #RPS #REC #재생에너지 #태양광정책 #솔라워크"""

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
