from alphacode.machine_learning.prediction_engine.predictor import TagPredictor

prob_st = "data structure"
predictor = TagPredictor("ridge/vsm", parameters_path = "prediction_engine/")

def tag(prob_st):
    return predictor.predict(prob_st)

# print(tag(prob_st))
