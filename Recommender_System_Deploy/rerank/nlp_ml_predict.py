from typing import final
from joblib import load
try:
    from Recommender_System_Deploy.rerank import nlp_frame
except:
    try:
        from rerank import nlp_frame
    except:
        raise


class nlp_ml_predict(nlp_frame.nlp_frame):
    def __init__(self) -> None:
        super().__init__()

    def predict(self, modelPath: str, vectPath: str, predictList: list, h: bool, u: bool):
        model = load(modelPath)
        vect = load(vectPath)

        tex = self.seg(predictList, h, u)
        tex = vect.transform(tex).toarray()

        res = model.predict(tex)

        return tex, res


if __name__ == "__main__":
    nmp = nlp_ml_predict()
    params = {
        "modelPath": 'nlpModel_NB/1640536039.7400753.joblib',
        "vectPath": 'nlpModel_NB/vect_1640536039.7400753.vect',
        "predictList": ["青椒也太難吃", "番茄超級好吃"],
        "h": True,
        "u": False
    }

    tex, res = nmp.predict(**params)
    final_res = nmp.toThreeClass(res)

    print(params['predictList'], final_res)
