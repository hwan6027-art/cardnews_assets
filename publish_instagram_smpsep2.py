"""
[프리미엄 네이비 스타일] 9월 SMP·REC 동향 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_smpsep2.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpsep2_08.png",
]

CAPTION = """9월 SMP, 한 달 새 20% 빠졌습니다.

전력거래소 기준 9월 육지 월평균 SMP는 119.02원/kWh로, 8월(148.39원)보다 29.37원(약 19.8%) 낮아졌습니다. 선선해진 날씨와 추석 연휴 등이 하락 배경으로 거론됩니다. 9월 초에는 평일 160원대, 주말 100원 안팎으로 요일별 편차도 컸습니다.

반면 REC 현물가는 9월 3주차 평균 71,850원으로 소폭 상승했습니다.

태양광 수익은 SMP 하나로 읽지 않습니다. 내 발전소가 SMP 연동인지, 고정가 계약인지 확인하고 REC 시세와 함께 월 수익을 점검해보세요.

카드 넘겨서 이번 달 확인 포인트를 살펴보세요 →

#태양광 #SMP #REC #태양광수익 #재생에너지 #신재생에너지 #태양광사업 #태양광정책 #에너지전환 #솔라워크"""

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
