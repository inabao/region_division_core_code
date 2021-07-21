from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from data_deal import dataset_generate, dataset_generate_both
import numpy as np

def train(X_train, y_train):
    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(X_train, y_train)
    return reg


def test(res, y_test, criterion="mae"):
    if criterion == "mae":
        return np.mean(np.abs(res - y_test))
    elif criterion == "rmse":
        return np.sqrt(np.mean((res - y_test)**2))

def HA(X_train):
    return np.mean(X_train, axis=1)

def predict_error(sqrt_n, day):
#     X_train, y_train = dataset_generate([16, 15], regx=16, regy=32, depart=(64, 64), interval=30)
#     X_test, y_test = dataset_generate(14, regx=16, regy=32, depart=(64, 64), interval=30)
    X_train, y_train = dataset_generate_both(14, depart=(sqrt_n, sqrt_n), interval=10)
    # print(X_train[0][0])
    X_test, y_test = dataset_generate_both(day, depart=(sqrt_n, sqrt_n), interval=30)
    X_train = X_train.reshape(sqrt_n**2 * X_train.shape[-2], X_train.shape[-1])
    y_train = y_train.reshape(sqrt_n**2 * y_train.shape[-1], 1)
    reg = train(X_train, y_train)
    res = 0

    for i in range(sqrt_n):
        a = np.random.randint(sqrt_n)
        b = np.random.randint(sqrt_n)
        res += test(reg.predict(X_test[a][b]), y_test[a][b], "mae")
    return res * sqrt_n


