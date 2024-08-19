from flask import Flask, request, jsonify
import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
# pandas, azure-cognitiveservices-vision-computervision, msrest

# Flask 앱 초기화
app = Flask(__name__)

# Azure Cognitive Services 설정
endpoint = "https://aiden-after.cognitiveservices.azure.com/"
subscription_key = "00cc9c94162e4fb1829dbc1d4b1c8d2c"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# 엑셀 파일 로드
food_db = pd.read_excel("음식DB.xlsx")

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    data = request.json
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    # 이미지 태그 추출
    tags_result = computervision_client.tag_image(image_url)
    
    # 태그 결과 출력
    labels = {}
    if tags_result.tags:
        for tag in tags_result.tags:
            labels[tag.name] = tag.confidence
    
    rice_related = ['white rice', 'steamed rice', 'jasmine rice', 'rice']
    confidence_threshold = 0.8

    rice_confidence = sum([labels[label] for label in rice_related if label in labels])

    if rice_confidence > confidence_threshold:
        final_label = '쌀밥'
    else:
        final_label = max(labels, key=labels.get)

    # '쌀밥'에 해당하는 칼로리 값 검색
    rice_row = food_db[food_db['대표식품명'].str.contains('쌀밥', na=False)]

    if not rice_row.empty:
        kcal_value = rice_row['에너지(kcal)'].values[0]
        result = {
            "final_label": final_label,
            "calories": kcal_value
        }
    else:
        result = {
            "final_label": final_label,
            "calories": None,
            "message": "'쌀밥' not found in the database."
        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
