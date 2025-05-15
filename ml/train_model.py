import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Cargar el dataset de cáncer de mama de scikit-learn
data = load_breast_cancer()
X = data.data
y = data.target  # 0 = maligno, 1 = benigno (o viceversa según el dataset)

# (Opcional) Dividir en conjunto de entrenamiento y prueba para evaluar desempeño
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de Regresión Logística (clasificación binaria)
model = LogisticRegression(max_iter=10000)  # max_iter alto para asegurar convergencia
model.fit(X_train, y_train)

# (Opcional) Imprimir exactitud en conjunto de prueba
accuracy = model.score(X_test, y_test)
print(f"Exactitud del modelo en datos de prueba: {accuracy:.2f}")

# Guardar el modelo entrenado a disco
joblib.dump(model, "ml/model.pkl")
print("Modelo entrenado guardado en ml/model.pkl")
