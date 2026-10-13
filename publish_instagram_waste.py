"""
[에디토리얼 스타일] 태양광 폐패널 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_waste.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/waste_08.png",
]

CAPTION = """태양광 폐패널, 7년 뒤 3.8배로 늘어납니다.

국회입법조사처의 2026 국정감사 이슈 분석에 따르면 태양광 폐패널 발생량은 2025년 2,547톤에서 2027년 2,645톤, 2029년 6,796톤, 2032년 9,632톤으로 늘어날 전망입니다. 2032년에는 2025년의 약 3.8배입니다. 발생 시점은 자연재해, 파손, 발전효율 저하, 리파워링 등에 따라 달라질 수 있습니다.

반면 재활용사업자 8곳의 연간 처리능력은 약 2만 3천 톤이지만 2025년 가동률은 약 11%에 그쳤습니다. 입법조사처는 설비 정보와 폐기물 정보가 분산돼 발생량 예측이 어렵고, 수거 물류망과 지역별 시설 배치, 저부가가치 재활용 우려를 과제로 짚었습니다.

(주)솔라워크는 설치만큼 철거·처리도 사업 계획에 넣어야 하는 시대가 오고 있다고 봅니다.

카드 넘겨서 연도별 전망과 남은 과제를 확인하세요 →

#태양광 #태양광폐패널 #폐패널재활용 #국정감사 #재생에너지 #신재생에너지 #태양광사업 #자원순환 #에너지전환 #솔라워크"""

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
