# 가상환경 설정 python -m venv venv
# pip install azure-cognitiveservices-vision-computervision
# pip install pandas
# pip install msrest
# pip install flask
# pip install openpyxl
# python app.py

import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

food_db = pd.read_excel("Food_DB.xlsx")

tag_to_food_name = {
    "rice": "밥",
    "gimbap": "김밥",
    "mandu": "만두",
    "lamian" : "라면",
    "ramen" : "라면",
    "pork" : "돼지고기"
}

endpoint = "https://aiden-after.cognitiveservices.azure.com/"
subscription_key = "00cc9c94162e4fb1829dbc1d4b1c8d2c"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

image_url = "https://dimg.donga.com/wps/NEWS/IMAGE/2024/02/02/123361133.8.jpg"
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
                print(f"'{food_name}' kcal: {r_value}")
                found = True
    
    if not found:
        print("No matching tags found in the database.")
else:
    print("No tags detected.")
