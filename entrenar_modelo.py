import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# Cargar los datos
url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
df = pd.read_csv(url)

# Seleccionar variables
features = ["zn", "indus", "rm", "ptratio", "b", "lstat"]
X = df[features]
y = df["medv"]

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Evaluar
y_pred = modelo.predict(X_test)
print(f"R2: {r2_score(y_test, y_pred):.4f}")

# RMSE calculado
import numpy as np
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse:.4f}")

# Guardar modelo
joblib.dump(modelo, "best_model.pkl")
print("Modelo guardado como best_model.pkl")