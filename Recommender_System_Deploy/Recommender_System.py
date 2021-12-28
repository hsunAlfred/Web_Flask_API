from recommender import recommender
from rerank import nlp_ml_predict
import time


class Recommender_System:
    def __init__(self) -> None:
        self.__sunonym = None
        with open("./Recommender_System_Deploy/rerank/sunonym.txt", 'r', encoding='utf-8') as f:
            self.__sunonym = tuple(line.split(',')
                                   for line in f.read().split('\n'))

        self.__nmp = nlp_ml_predict.nlp_ml_predict()

        self.__derivativeFood = []

    def __getRecommender(self):
        bendom_ele, rattings = \
            recommender.RCMD([1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
                             ["青椒也太難吃", "番茄超級好吃"])

        return bendom_ele, rattings

    def __rerankRecommender(self, bendom_ele, rattings):

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
            print(ratting, ratio)
            for i in range(len(self.__sunonym)):
                bendom_ele_rerank[i][1] = i+1
                for suno in self.__sunonym[i]:
                    if suno in ratting:
                        bendom_ele_rerank[i][0] += ratio
                        break
        bendom_ele_rerank.sort(key=lambda x: x[0], reverse=True)
        print(bendom_ele_rerank)
        return bendom_ele_rerank[:3]

    def __getDerivative(self, bendom_ele_rerank):
        pass

    def run(self):
        bendom_ele, rattings = self.__getRecommender()
        bendom_ele_rerank = self.__rerankRecommender(bendom_ele, rattings)
        recommender_result = self.__getDerivative(bendom_ele_rerank)


rs = Recommender_System()
rs.run()
