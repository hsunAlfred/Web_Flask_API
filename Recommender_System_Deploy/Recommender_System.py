try:
    from Recommender_System_Deploy.recomm import recommender
except:
    try:
        from recomm import recommender
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
import pandas as pd


class Recommender_System:
    def __init__(self) -> None:
        self.__sunonym = None
        with open("./Recommender_System_Deploy/rerank/sunonym.txt", 'r', encoding='utf-8') as f:
            self.__sunonym = tuple(line.split(',')
                                   for line in f.read().split('\n'))

        self.__nmp = nlp_ml_predict.nlp_ml_predict()

        self.__derivativeFood = {}
        df = pd.read_csv(
            "./Recommender_System_Deploy/rerank/derivativeFood.csv", encoding='utf-8')

        for row in range(df.shape[0]):
            k = df.iloc[row, ]['deri']
            v = df.iloc[row, ]['food']
            if k in self.__derivativeFood.keys():
                self.__derivativeFood[k].append(v)
            else:
                self.__derivativeFood[k] = [v]

        # 預載入DB資料
        self.rrr = recommender.RCMD()

    def __getRecommender(self, thisBendom, rattingStrs):
        bendom_ele, rattings = \
            self.rrr.getRecomm(thisBendom, rattingStrs)

        return bendom_ele, rattings

    def __rerankRecommender(self, bendom_ele, rattingStrs):
        '''
        return first three [rate and food_id] in list
        '''
        # params = {
        #     "modelPath": './Recommender_System_Deploy/rerank/1640536039.7400753.joblib',
        #     "vectPath": './Recommender_System_Deploy/rerank/vect_1640536039.7400753.vect',
        #     "predictList": rattingStrs,
        #     "h": True,
        #     "u": False
        # }

        params = {
            "modelPath": './Recommender_System_Deploy/rerank/1642254722.262666.joblib',
            "vectPath": './Recommender_System_Deploy/rerank/vect_1642254722.262666.vect',
            "predictList": rattingStrs,
            "h": True,
            "u": False
        }

        tex, ratio = self.__nmp.predict(**params)
        # final_ratio -> 3 2 1
        final_ratio = tuple(self.__nmp.toThreeClass(ratio))

        # bendom_ele_rerank = [[便當分數, 設定便當index(1-15)]]
        bendom_ele_rerank = [[i, -1] for i in bendom_ele]
        for rattingStr, ratio in zip(rattingStrs, final_ratio):
            for i in range(len(self.__sunonym)):
                # 設定便當index(1-15)
                bendom_ele_rerank[i][1] = i+1
                for suno in self.__sunonym[i]:
                    if suno in rattingStr:
                        # 便當分數
                        bendom_ele_rerank[i][0] += ratio
                        break
        bendom_ele_rerank.sort(key=lambda x: x[0], reverse=True)
        bendom_ele_rerank = [
            ber for ber in bendom_ele_rerank if ber[1] not in [4, 6, 8, 9, 15]]
        return bendom_ele_rerank[:3]

    def __getDerivative(self, bendom_ele_rerank, sep):
        res = []
        for rate, index_p1 in bendom_ele_rerank:
            if index_p1 in self.__derivativeFood:
                res.append(choice(self.__derivativeFood[index_p1]))

        return sep.join(res)

    def run(self, thisBendom: str, rattingStrs: str, sep: str = ":"):
        run_params = {
            "thisBendom": [int(i) for i in thisBendom.split(sep)],
            "rattingStrs": rattingStrs.split(sep)
        }
        bendom_ele, rattingStrs = self.__getRecommender(**run_params)
        bendom_ele_rerank = self.__rerankRecommender(bendom_ele, rattingStrs)
        recommender_result = self.__getDerivative(bendom_ele_rerank, sep)
        return recommender_result


if __name__ == "__main__":
    rs = Recommender_System()
    params = {
        "thisBendom": "1:0:1:0:0:1:1:1:1:0:0:0:1:1:1",
        "rattingStrs": "青椒也太難吃:番茄超級好吃",
        "sep": ":"
    }
    res = rs.run(**params)
    print('\n\n\n')
    print(res)
