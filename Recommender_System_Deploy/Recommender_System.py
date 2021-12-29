try:
    from Recommender_System_Deploy.recommender import recommender
except:
    try:
        from recommender import recommender
    except:
        raise

try:
    from Recommender_System_Deploy.rerank import nlp_ml_predict
except:
    try:
        from rerank import nlp_ml_predict
    except:
        raise

from random import choice


class Recommender_System:
    def __init__(self) -> None:
        self.__sunonym = None
        with open("./Recommender_System_Deploy/rerank/sunonym.txt", 'r', encoding='utf-8') as f:
            self.__sunonym = tuple(line.split(',')
                                   for line in f.read().split('\n'))

        self.__nmp = nlp_ml_predict.nlp_ml_predict()

        self.__derivativeFood = [
            ["蜜汁雞腿", "滷雞腿"],
            ["蜜汁排骨", "滷排骨"],
            ["煎鮭魚", "燻鮭魚"],
            ["香腸炒飯"],
            ["炒綠花椰菜"],
            ["炒白花椰菜"],
            ["滷蛋"],
            ["荷包蛋"],
            ["水煮蛋"],
            ["炒豆芽"],
            ["番茄炒蛋", "番茄肉醬義大利麵"],
            ["炒青椒"],
            ["魚香茄子", "涼拌茄子"],
            ["蒜蓉四季豆", "水煮四季豆"],
            ["薑黃飯", "糙米飯", "白飯"],
        ]

    def __getRecommender(self, thisBendom, ratting):
        bendom_ele, rattings = \
            recommender.RCMD(thisBendom, ratting)

        return bendom_ele, rattings

    def __rerankRecommender(self, bendom_ele, rattings):
        '''
        return first three [rate and food_id] in list
        '''
        params = {
            "modelPath": './Recommender_System_Deploy/rerank/1640536039.7400753.joblib',
            "vectPath": './Recommender_System_Deploy/rerank/vect_1640536039.7400753.vect',
            "predictList": rattings,
            "h": True,
            "u": False
        }

        tex, ratio = self.__nmp.predict(**params)
        final_ratio = tuple(self.__nmp.toThreeClass(ratio))

        bendom_ele_rerank = [[i, -1] for i in bendom_ele]
        for ratting, ratio in zip(rattings, final_ratio):
            #print(ratting, ratio)
            for i in range(len(self.__sunonym)):
                bendom_ele_rerank[i][1] = i+1
                for suno in self.__sunonym[i]:
                    if suno in ratting:
                        bendom_ele_rerank[i][0] += ratio
                        break
        bendom_ele_rerank.sort(key=lambda x: x[0], reverse=True)

        return bendom_ele_rerank[:3]

    def __getDerivative(self, bendom_ele_rerank):
        return "-".join([choice(self.__derivativeFood[index_p1-1])
                         for rate, index_p1 in bendom_ele_rerank])

    def run(self, thisBendom: str, ratting: str):
        run_params = {
            "thisBendom": [int(i) for i in thisBendom.split("-")],
            "ratting": ratting.split("-")
        }
        bendom_ele, rattings = self.__getRecommender(**run_params)
        bendom_ele_rerank = self.__rerankRecommender(bendom_ele, rattings)
        recommender_result = self.__getDerivative(bendom_ele_rerank)
        return recommender_result


if __name__ == "__main__":
    rs = Recommender_System()
    params = {
        "thisBendom": "1-0-1-0-0-1-1-1-1-0-0-0-1-1-1",
        "ratting": "青椒也太難吃-番茄超級好吃"
    }
    res = rs.run(**params)
    print(res)
