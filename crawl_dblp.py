import requests
import json
from datetime import datetime

# need to update the keywords by year and number of papers from DBLP
keywords = [['federated%20learning', [[2004, 1], [2005, 3], [2008, 1], [2009, 2], [2010, 1], [2012, 1], [2013, 3], [2014, 2], [2015, 1], [2016, 4], [2017, 10], [2018, 42], [2019, 229], [2020, 908], [2021, 1977], [2022, 3103], [2023, 4461], [2024, 1139]] ],  ]
all_data = []
acc_num = 0
for kw in keywords:
    print(kw[0])
    for year, cnt in kw[1]:
        # print(year, cnt)
        acc_num += cnt
        for num_page in range((cnt + 999) // 1000):            
            kwq = f'{kw[0]}%20year%3A{year}%3A'
            url_api = f'https://dblp.org/search/publ/api?q={kwq}&h=1000&f={num_page * 1000}&format=json'
            print(url_api)
            
            try:
                json_data = requests.get(url_api).json()
                # print(len(json_data['result']['hits']['hit']))
                all_data.extend(json_data['result']['hits']['hit'])                
            except Exception as e:
                pass
        print(f"Up to {year} : {len(all_data)}, cnt: {acc_num}")


date_str = datetime.now().strftime("%y%m%d")
with open(f'fl_dblp_{date_str}.json', 'w') as f:
    json.dump(all_data, f, indent=2)

