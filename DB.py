import pandas as pd

food_db = pd.read_excel("음식DB.xlsx")

food_db['대표식품명'] = food_db['대표식품명'].replace('가래떡', '떡')

food_db.to_excel("음식DB.xlsx", index=False)
