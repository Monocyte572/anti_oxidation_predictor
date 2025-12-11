import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\ichan\OneDrive\Desktop\total_rgb_Brix_Hardness_AC.csv")
X = df.drop(columns=['Anti-oxidation'])
y = df['Anti-oxidation']

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=123)
train_dmatrix = xgb.DMatrix(data=train_X, label=train_y)
test_dmatrix = xgb.DMatrix(data=test_X, label=test_y)


param = {
    "booster": "gbtree",
    "objective": "reg:squarederror",
    "max_depth": 4, #max depth -> complexity of the model, higher depth -> more complex model
    "alpha": 10, #L1 regularization term on weights
    "eta": 0.1 ,
    "subsample": 0.8, #overfitting control
    "colsample_bytree": 0.8 #overfitting control
}
xgb_r = xgb.train(params=param, dtrain=train_dmatrix, num_boost_round=100)
pred = xgb_r.predict(test_dmatrix)


rmse = np.sqrt(MSE(test_y, pred))
print("RMSE: %f" % rmse)
mae = mean_absolute_error(test_y, pred)
r2 = r2_score(test_y, pred)
print(f"MAE: {mae:.4f}")
print(f"R Score: {r2:.4f}")

residuals = test_y - pred
sns.histplot(residuals, kde=True)
plt.title("Residual Distribution")

xgb.plot_importance(xgb_r)
plt.title("Feature Importance")
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(x=test_y, y=pred)
plt.plot([test_y.min(), test_y.max()], [test_y.min(), test_y.max()], 'r--')
plt.xlabel("real Brix")
plt.ylabel("predict Brix")
plt.show()


#model is not good, need more data and feature engineering
#model is a baseline but the tree gonna be revised, optimized and tuned
#maybe try other models or define custom models but how? 