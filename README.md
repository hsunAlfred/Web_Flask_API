# Web_Flask_API


recommender system api 20220104
url: http://34.124.166.150:22014/recomm
參數：sep, thisBendom, rattingStrs
    sep:str分隔符號, 預設為":"

    thisBendom:str, 把本次便當元素轉換為1(有)、0(無), 順序依 
        照雅潔在DB中的食物ID順序，分隔符號同sep
        0 drumstick
        1 rib
        2 salmon
        3 sausage
        4 broccoli
        5 cauliflower
        6 corned egg
        7 poached egg
        8 boiled egg
        9 bean sprouts
        10 tomato
        11 green pepper
        12 eggplant
        13 beans
        14 rice
        eg. "1-0-1-0-0-1-1-1-1-0-0-0-1-1-1"
        注意!!!!：食物就算我們沒有也要留那個位置，然後填0

    rattingStrs:str，分隔符號同sep
	    eg. 青椒也太難吃-番茄超級好吃

example code
    url = "http://34.124.166.150:22014/recomm"

    res = requests.post(
                url,
                params = {
                    "sep": "-"
                    "thisBendom": "1-0-1-0-0-1-1-1-1-0-0-0-1-1-1",
                    "ratting": "青椒也太難吃-番茄超級好吃"
                }
            ).text
    res = json.loads(res)
