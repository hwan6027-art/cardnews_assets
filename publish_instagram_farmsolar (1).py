"""
[에디토리얼 스타일] 영농형 태양광법·묵힌 농지 태양광 활용 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_farmsolar.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/farmsolar_08.png",
]

CAPTION = """12월 17일, 영농형 태양광이 시작됩니다.

10월 6일 국무회의에서 방치된 농지의 태양광 활용을 위한 인허가·자금 지원 방안 검토가 거론됐습니다. 다만 12월 17일 시행되는 영농형 태양광법은 '농사를 이어가며' 태양광을 설치하는 경우를 대상으로 합니다. 농사를 중단한 땅은 농지 전용, 농업진흥지역 규제 등을 별도로 확인해야 합니다.

영농형 태양광은 실제 경작 면적이 부지의 80% 이상이어야 하고, 모듈 차광률은 30% 미만, 구조물 최저 높이는 2.5m 이상이어야 합니다. 발전사업 허가는 처음 5년이며 영농실적 등을 확인해 연장하면 최대 23년까지 가능합니다.

내 땅이 어떤 유형인지, 계통 연결은 가능한지 먼저 확인해보세요.

카드 넘겨서 지금 확인해야 할 3가지 실무 포인트를 확인하세요 →

#태양광 #영농형태양광 #농지태양광 #영농형태양광법 #재생에너지 #태양광정책 #신재생에너지 #태양광사업 #농촌태양광 #에너지전환 #솔라워크"""

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
