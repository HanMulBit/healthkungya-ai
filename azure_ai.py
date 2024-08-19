#pip install azure-cognitiveservices-vision-computervision
#pip install pandas
#pip install msrest

import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

food_db = pd.read_excel("Food_DB.xlsx")

tag_to_food_name = {
    "rice": "밥",
    "mandu": "만두",
    "fried rice": "볶음밥"
}

endpoint = "https://aiden-after.cognitiveservices.azure.com/"
subscription_key = "00cc9c94162e4fb1829dbc1d4b1c8d2c"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbIeoRuEpgQ0G2gnWWuTgnAnxLVEeGLT91VA&s"
tags_result = computervision_client.tag_image(image_url)

if tags_result.tags:
    detected_tags = [tag.name for tag in tags_result.tags]
    
    for tag in detected_tags:
        if tag in food_db['음 식 명'].values:
            matching_row = food_db[food_db['음 식 명'] == tag]
            r_value = matching_row['에너지(kcal)'].values[0]
            print(f"'{tag}' kcal: {r_value}")
else:
    print("No tags detected.")