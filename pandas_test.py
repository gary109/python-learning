import pandas as pd

groups = ["Modern Web", "DevOps", "Cloud", "Big Data", "Security", "自我挑戰組"]
ironmen = [46, 8, 12, 12, 6, 58]

ironmen_dict = {"groups": groups,
                "ironmen": ironmen
                }

ironmen_df = pd.DataFrame(ironmen_dict)

print(ironmen_df.iloc[0:1, 1]) # 第一列第二欄：Modern Web 組的鐵人數
print("---")
print(ironmen_df.iloc[0:1,:]) # 第一列：Modern Web 組的組名與鐵人數
print("---")
print(ironmen_df.iloc[:,1]) # 第二欄：各組的鐵人數
print("---")
print(ironmen_df["ironmen"]) # 各組的鐵人數
print("---")
print(ironmen_df.ironmen) # 各組的鐵人數