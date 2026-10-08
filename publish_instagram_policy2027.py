"""
[에디토리얼 스타일] 국감 업무보고로 읽는 2027 태양광 시장 카드뉴스 - 인스타그램 캐러셀 자동 게시
(Instagram API - Instagram 로그인 기반, graph.instagram.com 사용)

실행: python publish_instagram_policy2027.py
"""

import json
import time
import urllib.error
import urllib.request
import urllib.parse

ACCESS_TOKEN = "IGAAL3pKyfaxFBZAFpUR3hJeVItZA0RZAcDF5THpScjZAkcGVQQWxNYWFKb3JhU1FwNEdiSFZASd1FsSFZAJdUpzQWNyRnk1cHZA1aWxnRlBRNDZAVX3ExZA1o1ZAlNRTFdxZAGxLcU5LRDNOdk11ZAVdFb0VtTFJnMERjcTctanJMLXc4WkZAlZAwZDZD"
IG_USER_ID = "27936490119342782"

IMAGE_URLS = [
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_01.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_02.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_03.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_04.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_05.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_06.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_07.png",
    "https://raw.githubusercontent.com/hwan6027-art/cardnews_assets/main/policy2027_08.png",
]

CAPTION = """2027 태양광 시장, 국감에서 밑그림이 나왔습니다.

10월 6일 기후에너지환경부가 국정감사 업무보고에서 2030년까지 재생에너지 설비 100GW 이상 목표를 제시했습니다. 2027년부터 RPS 의무 이행을 발전량에서 설비용량 기준으로 바꾸고, 시장 진입을 경쟁입찰 기반 장기 고정가격계약으로 일원화하는 방향입니다. 가정용 태양광은 상계에서 현금정산으로, 공장 지붕 태양광은 의무화가 추진됩니다.

계통 쪽도 달라집니다. 계통포화지역에 2030년까지 태양광 3GW가 추가 접속되고, 일반 배전선로 최대 접속용량은 14MW에서 16MW로, 변압기는 50MW에서 60MW로 늘어납니다. 햇빛소득마을 2차 공모에는 617곳이 신청해 1차(129곳)의 4배를 넘었습니다.

모두 추진 방향이며 세부 기준은 확정 전입니다. (주)솔라워크는 확정되는 내용을 계속 정리해드리겠습니다.

카드 넘겨서 사업자가 지금 점검할 3가지를 확인하세요 →

#태양광 #국정감사 #2027태양광 #재생에너지100GW #햇빛소득마을 #계통접속 #태양광정책 #신재생에너지 #태양광사업 #에너지전환 #솔라워크"""

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
