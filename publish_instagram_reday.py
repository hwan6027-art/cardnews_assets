"""
[프리미엄 네이비 스타일] 재생에너지의 날 법정기념일 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_reday.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/reday_08.png",
]

CAPTION = """10월 23일, 재생에너지의 날이 법정기념일이 됩니다.

2019년 세계 재생에너지 총회(서울) 개막일인 10월 23일에 학계·산업계·시민단체가 제정한 '재생에너지의 날'이 정부가 인정하는 법정기념일로 지정됐습니다. 행정안전부가 기념일 규정을 개정하고, 기후에너지환경부가 주관합니다. 2026년 제8회 기념식은 서울 코엑스에서 열릴 예정입니다.

한편 정부는 2030년까지 재생에너지 설비 100GW 목표를 재확인했고, 이 가운데 태양광은 87GW입니다. 다만 ESS 총량, 송·배전망 보강 범위, 비용 분담 주체는 아직 구체화되지 않았다는 업계 지적이 나옵니다.

(주)솔라워크는 기념일 이후의 과제인 계통과 인프라 이슈까지 계속 정리해드리겠습니다.

카드 넘겨서 핵심 숫자를 확인하세요 →

#태양광 #재생에너지의날 #법정기념일 #재생에너지 #신재생에너지 #태양광정책 #재생에너지100GW #태양광사업 #에너지전환 #솔라워크"""

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
