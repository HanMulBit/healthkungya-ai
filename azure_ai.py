from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

endpoint = "https://aiden-testcv.cognitiveservices.azure.com/"
subscription_key = "d028f3fd54aa4ab98fb20676ade098a6"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

image_url = "https://www.sbfoods-worldwide.com/ko/recipes/jvegc10000000aeu-img/5_Howtocook_rice_recipe.jpg"

tags_result = computervision_client.tag_image(image_url)

print("Tags in the image:")
if tags_result.tags:
    for tag in tags_result.tags:
        print(f"'{tag.name}' with confidence {tag.confidence:.2f}")
else:
    print("No tags detected.")
