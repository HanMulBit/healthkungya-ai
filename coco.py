import os
import json
import pandas as pd
from PIL import Image

def load_categories_from_excel(excel_file):
    df = pd.read_excel(excel_file)
    categories = {i: category for i, category in enumerate(df['음식 분류'].unique())}
    return categories

def yolo_to_coco_single(yolo_file_path, image_file_path, output_json_path, start_annotation_id, start_image_id, categories):
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # 카테고리 추가
    for class_id, class_name in categories.items():
        coco_data["categories"].append({
            "id": class_id,
            "name": class_name
        })

    annotation_id = start_annotation_id
    image_id = start_image_id

    # 이미지 크기를 가져오기 위해 PIL을 사용
    try:
        with Image.open(image_file_path) as img:
            image_width, image_height = img.size

        # 이미지 정보 추가
        coco_data["images"].append({
            "id": image_id,
            "width": image_width,
            "height": image_height,
            "file_name": os.path.basename(image_file_path)
        })

        with open(yolo_file_path, 'r') as f:
            for line in f.readlines():
                class_id, x_center, y_center, width, height = map(float, line.strip().split())

                # YOLO 형식에서 COCO 형식으로 변환
                bbox = [
                    (x_center - width / 2) * image_width,
                    (y_center - height / 2) * image_height,
                    width * image_width,
                    height * image_height
                ]

                annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": int(class_id),
                    "bbox": bbox,
                    "area": bbox[2] * bbox[3],
                    "iscrowd": 0
                }

                coco_data["annotations"].append(annotation)
                annotation_id += 1

        # COCO JSON 파일로 저장
        with open(output_json_path, 'w') as json_file:
            json.dump(coco_data, json_file, indent=4)

        print(f"Successfully converted {yolo_file_path} to COCO format.")
        return annotation_id, image_id + 1  # 다음 변환을 위한 새로운 시작 ID 반환

    except FileNotFoundError:
        print(f"Error: {image_file_path} not found.")
        return annotation_id, image_id  # 오류 발생 시 동일한 ID 반환

# 엑셀 파일에서 카테고리 로드
excel_file_path = r'C:\Users\ys\Downloads\음식 이미지 및 영양정보 텍스트\20240807_음식DB.xlsx'
categories = load_categories_from_excel(excel_file_path)

# 초기 ID 설정
annotation_id = 1
image_id = 1

# 경로 설정 (여러 파일을 변환할 때 반복 사용)
yolo_file_path = r'C:\Users\ys\Downloads\음식 이미지 및 영양정보 텍스트\Validation\[라벨]음식분류_VAL\txt\01011001\01_011_01011001_160273353645093.txt'
image_file_path = r'C:\Users\ys\Downloads\음식 이미지 및 영양정보 텍스트\Validation\[라벨]음식분류_VAL\images\01011001.jpg'
output_json_path = r'C:\Users\ys\Downloads\음식 이미지 및 영양정보 텍스트\Validation\coco_annotation_01011001.json'

# 변환 함수 호출
annotation_id, image_id = yolo_to_coco_single(yolo_file_path, image_file_path, output_json_path, annotation_id, image_id, categories)
