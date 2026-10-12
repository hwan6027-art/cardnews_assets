"""
[프리미엄 네이비 스타일] 10월 2주차 SMP·REC 시세 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_smpoct2.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/smpoct2_08.png",
]

CAPTION = """10월 SMP, 107원대까지 내려왔습니다.

전력거래소 기준 육지 SMP는 8월 월평균 148.39원에서 9월 119.02원으로 내려갔고, 10월 6~12일에는 일별 가중평균의 평균이 약 107.8원으로 9월 월평균보다 약 9% 낮은 수준입니다. 일별로는 10월 6일 107.81원, 9일 107.94원, 12일 108.85원으로 평일과 주말 차이도 3원 안팎으로 좁아졌습니다.

REC 현물시장은 10월 8일 종가 71,200원(거래량 201,313 REC)으로 7만 1천원대에서 거래됐습니다.

(주)솔라워크가 이번 주 확인할 포인트를 정리했습니다. 내 발전소가 SMP 연동인지 고정가 계약인지 먼저 확인하고, 월말 정산 전에 일별 SMP와 REC 종가로 예상 수익을 점검해보세요.

카드 넘겨서 일별 SMP 표와 실무 포인트를 확인하세요 →

#태양광 #SMP #REC #태양광수익 #재생에너지 #신재생에너지 #태양광사업 #에너지전환 #전력거래소 #솔라워크"""

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
