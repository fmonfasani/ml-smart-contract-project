from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
from web3 import Web3
from fastapi.responses import JSONResponse

app = FastAPI()

# Cargar el modelo entrenado al iniciar la aplicación
model = joblib.load("ml/model.pkl")

# Definir la estructura esperada del JSON de entrada para /predict
class InputData(BaseModel):
    features: list[float]  # Lista de características numéricas de entrada

# Definir la estructura esperada del JSON de entrada para /trigger
class TriggerData(BaseModel):
    prediction: int  # Predicción (0 o 1) que se enviará al contrato

# Configurar conexión a la red Ethereum local (Ganache o Hardhat)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():
    raise Exception("No se pudo conectar a la red Ethereum local. Asegúrate de que Ganache/Hardhat esté en ejecución.")

# **IMPORTANTE**: La dirección y ABI del contrato deben ser actualizados 
# después de desplegar el contrato inteligente con deploy.py.
contract_address = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"
 # ← actualizar con la dirección desplegada
contract_abi = [
    {
      "inputs": [{"internalType": "bool","name": "_prediccion","type": "bool"}],
      "name": "actualizarEstado",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "actuar",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "lastPrediction",
      "outputs": [{"internalType": "bool","name": "","type": "bool"}],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "anonymous": False,
      "inputs": [{"indexed": False,"internalType": "bool","name": "prediccion","type": "bool"}],
      "name": "PredictionUpdated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [],
      "name": "ActionExecuted",
      "type": "event"
    }
]


contract = w3.eth.contract(address=contract_address, abi=contract_abi)
print("Contrato:", contract_address)
print("ABI cargado:", type(contract_abi))
print("Conexión:", w3.is_connected())
print("Probar llamada:", contract.functions.lastPrediction().call())
# Usar la primera cuenta de Ganache/Hardhat para las transacciones (privada en local)
default_account = w3.eth.accounts[0]
w3.eth.defaultAccount = default_account

@app.post("/predict")
def predict(input_data: InputData):
    # Convertir la lista de características a un array de numpy 2D (una sola muestra)
    X = np.array([input_data.features])
    # Realizar la predicción con el modelo cargado
    pred = model.predict(X)[0]  # predicción 0 o 1
    return {"prediction": int(pred)}

@app.post("/trigger")
def trigger(data: TriggerData):
    pred_bool = bool(data.prediction)
    # Llamar a la función actualizarEstado del contrato con la predicción
    tx1 = contract.functions.actualizarEstado(pred_bool).transact({'from': default_account})
    receipt1 = w3.eth.wait_for_transaction_receipt(tx1)
    # Llamar a la función actuar del contrato para tomar acción si la predicción es true
    tx2 = contract.functions.actuar().transact({'from': default_account})
    receipt2 = w3.eth.wait_for_transaction_receipt(tx2)
    return {"status": "triggered", "prediction": data.prediction}

@app.get("/status")
def get_last_prediction():
    try:
        last_pred = contract.functions.lastPrediction().call()
        return JSONResponse(content={"lastPrediction": bool(last_pred)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
