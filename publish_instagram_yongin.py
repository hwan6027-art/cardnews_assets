"""
[에디토리얼 스타일] 용인 농우태양광 168kW 준공 현장 홍보 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_yongin.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/yongin_08.png",
]

CAPTION = """경기도 용인시 농우태양광 168kW급 준공 현장을 소개합니다.

(주)솔라워크가 완벽한 공사로 마무리했습니다. 건물 옥상은 물론 옥상주차장 상부까지 쓸 수 있는 공간을 발전 공간으로 활용했고, 주차장 캐노피 아래 공간은 기존처럼 사용할 수 있도록 구성했습니다.

분전·보호 설비는 차단기와 SPD(서지보호장치), 디지털 패널미터까지 반듯하게 정리했고, 인버터 결선과 접지선 연결 상태, 접지 측정까지 현장에서 직접 확인했습니다.

설계부터 시공, 준공까지. 태양광 설치가 고민되신다면 (주)솔라워크와 상담하세요. DM으로 편하게 문의 주세요.

카드 넘겨서 현장 사진을 확인하세요 →

#태양광 #태양광시공 #옥상태양광 #주차장태양광 #용인태양광 #168kW #태양광준공 #태양광설치 #신재생에너지 #솔라워크"""

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
