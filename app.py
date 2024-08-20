from flask import Flask, request, jsonify
import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

app = Flask(__name__)

endpoint = "https://aiden-after.cognitiveservices.azure.com/"
subscription_key = "00cc9c94162e4fb1829dbc1d4b1c8d2c"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

food_db = pd.read_excel("Food_DB.xlsx")

tag_to_food_name = {
    "rice": "밥",
    "gimbap": "김밥",
    "mandu": "만두"
}

@app.route('/analyze_image')
def analyze_image():
    data = request.json
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    tags_result = computervision_client.tag_image(image_url)

    if tags_result.tags:
        detected_tags = [tag.name for tag in tags_result.tags]
        print("Detected tags:", detected_tags)  

        found = False
        for tag in detected_tags:
            food_name = tag_to_food_name.get(tag, None) 
            if food_name:
                food_name = food_name.strip() 
                print(f"Checking if '{food_name}' is in the database...")  

                food_db['음 식 명'] = food_db['음 식 명'].str.strip() 

                if food_name in food_db['음 식 명'].values:
                    matching_row = food_db[food_db['음 식 명'] == food_name]
                    r_value = matching_row['에너지(kcal)'].values[0]
                    found = True
                    result = {
                        "final_label": food_name,
                        "calories": r_value
                    }
                    return jsonify(result)
        
        if not found:
            return jsonify({"error": "No matching tags found in the database."}), 404
    else:
        return jsonify({"error": "No tags detected."}), 404

if __name__ == '__main__':
    app.run(debug=True)
