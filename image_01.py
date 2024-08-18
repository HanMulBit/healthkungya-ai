import requests

subscription_key = "ff9151b1a2564fa4a552475ecac63fde"
search_url = "https://api.bing.microsoft.com/v7.0/images/visualsearch"

# 이미지 파일 경로
image_path = "C:/python_kakao/workspace/Team_project01/image01.png"
image_data = open(image_path, "rb").read()

headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "multipart/form-data"
}

response = requests.post(search_url, headers=headers, files={"image": image_data})
response.raise_for_status()
search_results = response.json()

# 음식 이름 출력
for tag in search_results["tags"]:
    if "displayName" in tag:
        print(f"음식 이름: {tag['displayName']}")

    for action in tag.get("actions", []):
        if action["actionType"] == "VisualSearch":
            for item in action.get("data", {}).get("value", []):
                if "name" in item:
                    print(f"관련 음식 이름: {item['name']}")

