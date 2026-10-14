"""
[프리미엄 네이비 스타일] 햇빛소득마을 2차 선정 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_village.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/village_08.png",
]

CAPTION = """햇빛소득마을, 누적 523곳으로 늘었습니다.

10월 7일 행정안전부가 햇빛소득마을 2차 선정 결과를 발표했습니다. 심사 대상 608개 마을 가운데 436곳이 선정돼 1차 87곳을 더한 누적 선정은 523곳입니다. 정부의 올해 목표는 700곳입니다.

다만 436곳 중 바로 사업을 추진할 수 있는 곳은 23곳이고, 413곳은 부지 임대 협의, 자금 계획, 계통연계 상황 등을 보완해야 하는 조건부 선정입니다. 160곳은 부지 미확보나 자금 계획 미제출 등으로 다음 공모 신청이 권고됐습니다. 권역별로는 전남·광주 106곳, 전북 59곳, 충북·경북 각 56곳, 충남 47곳 순입니다.

정부는 인허가 절차, 최대 85% 금융지원, 사업부지 확보, 계통연계 문제 해소를 지원한다고 밝혔습니다. 3차 공모는 10월 30일까지이며 12월 말 결과가 발표될 예정입니다.

(주)솔라워크가 참여를 검토 중인 분들을 위해 부지, 자금, 계통 세 가지 실무 포인트를 정리했습니다.

카드 넘겨서 확인하세요 →

#태양광 #햇빛소득마을 #주민참여태양광 #재생에너지 #신재생에너지 #태양광정책 #태양광사업 #농촌태양광 #에너지전환 #솔라워크"""

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
