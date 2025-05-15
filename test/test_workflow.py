import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from web3 import Web3
import json

# Cargar modelo entrenado
model = joblib.load("ml/model.pkl")

# Cargar un ejemplo de datos (usaremos el primer dato del dataset de cáncer de mama)
data = load_breast_cancer()
X_example = data.data[0]  # primer ejemplo
y_example = data.target[0]  # etiqueta real del primer ejemplo (por curiosidad)

# Predecir usando el modelo
pred = model.predict(X_example.reshape(1, -1))[0]
print(f"Predicción del modelo para el ejemplo de prueba: {int(pred)} (Etiqueta real: {y_example})")

# Conectar a la red Ethereum local
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# Cargar ABI y dirección del contrato desplegado (asegúrate de haber ejecutado deploy.py)
with open("contract/MLContract_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)
with open("contract/MLContract_address.txt", "r") as addr_file:
    contract_address = addr_file.read().strip()

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Llamar a la función actualizarEstado del contrato con la predicción
tx1 = contract.functions.actualizarEstado(bool(pred)).transact()
w3.eth.wait_for_transaction_receipt(tx1)
print(f"Transacción actualizarEstado enviada (predicción = {bool(pred)})")

# Leer el estado almacenado en el contrato para verificar
stored_value = contract.functions.lastPrediction().call()
print(f"Valor almacenado en contrato lastPrediction: {stored_value}")

# Llamar a la función actuar del contrato
tx2 = contract.functions.actuar().transact()
w3.eth.wait_for_transaction_receipt(tx2)
print("Función actuar ejecutada en el contrato (si lastPrediction=true, se habrá emitido evento ActionExecuted).")
