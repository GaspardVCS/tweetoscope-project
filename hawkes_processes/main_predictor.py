from predictor import Predictor
import numpy as np

if __name__ == "__main__":
    predictor = Predictor()
    history_600 = np.array([[0, 97], [2, 20771], [3, 140], [20, 240], [65, 75], [78, 51], [79, 64], [87, 1087], [100, 345], \
        [106, 968], [125, 655], [149, 87], [171, 150], [200, 1071], [241, 762], [273, 395], [274, 323], \
        [293, 3671], [362, 893], [374, 1848], [392, 340], [421, 410], [423, 300], [432, 12], [463, 589], [491, 483]])
    
    history_1200 = np.array([[0, 97], [2, 20771], [3, 140], [20, 240], [65, 75], [78, 51], [79, 64], [87, 1087], \
        [100, 345], [106, 968], [125, 655], [149, 87], \
        [171, 150], [200, 1071], [241, 762], [273, 395], [274, 323], [293, 3671], [362, 893], \
         [374, 1848], [392, 340], [421, 410], [423, 300], [432, 12], [463, 589], \
             [491, 483], [670, 162], [728, 286], [797, 26], [915, 490], [997, 361]])

    _, params = predictor.compute_MLE(history_600, 600)
    prediction1 = predictor.prediction(params, history_600, 600)
    prediction2 = predictor.prediction(params, history_1200, 1200)
    print(f"Prediction 1 : {prediction1}")
    print(f"Prediction 2: {prediction2}")
    print(f"real : {len(history_1200)}")
