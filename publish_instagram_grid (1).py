"""
[Q&A 스티커 스타일·1:1·6장] 송전망 주변 마을 태양광 수익 공유 카드뉴스 - 인스타그램 캐러셀 자동 게시
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
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/grid_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/grid_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/grid_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/grid_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/grid_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/grid_06.png",
]

CAPTION = """송전선 지나는 마을에 태양광 수익을 나눕니다 ☀️

기후에너지환경부가 송전망 주변 마을 지원 방안을 내놨습니다. 지자체에 지급되는 송전선로 지원금(가공선로 1km당 20억 원)의 3분의 2 이내를 송·변전설비 주변지역에 배분하고, 주변 마을이 태양광 사업을 추진하면 설치비용을 우선 반영해 주민이 발전수익을 나눌 수 있게 합니다.

입지 선정 과정에도 주민 참여가 늘어납니다. 시군구 주민설명회는 2회에서 3회로, 후보 입지는 2곳 이상 비교하고, 주민은 회의를 참관하고 대안 부지를 서면으로 제안할 수 있습니다.

입법예고는 10월 22일부터 12월 1일까지이며, 이후 의견 수렴과 법제처 심사를 거쳐 확정됩니다. 주변지역의 거리 기준과 주민 수익 배분 비율은 아직 공개되지 않았습니다.

(주)솔라워크가 쉽게 정리했습니다. 저장해두고 필요할 때 확인하세요!

#태양광 #송전망 #마을태양광 #계통햇빛소득마을 #재생에너지 #신재생에너지 #태양광정책 #주민참여 #에너지전환 #솔라워크"""

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
