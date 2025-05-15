# 🧠🔗 Integración de Machine Learning con Contrato Inteligente en Ethereum

Este proyecto combina un modelo de _Machine Learning_ entrenado en Python con un contrato inteligente en Solidity desplegado sobre una red local de Ethereum (Hardhat o Ganache). Permite realizar predicciones off-chain y tomar decisiones automatizadas on-chain.

---

## 📁 Estructura del Proyecto

ml-smart-contract-project/
├── ml/ # Entrenamiento y modelo ML
│ ├── train_model.py
│ └── model.pkl
├── backend/ # API REST con FastAPI
│ ├── app.py
│ └── requirements.txt
├── contract/ # Smart Contract en Solidity + deploy
│ ├── MLContract.sol
│ ├── deploy.py
│ ├── contracts/ # Carpeta creada por Hardhat
│ ├── hardhat.config.js
├── test/ # Script de prueba completo
│ └── test_workflow.py

---

## 🚀 Paso a Paso de Instalación y Ejecución

### 1. Clonar e instalar dependencias

```bash
git clone https://github.com/fmonfasani/ml-smart-contract-project.git
cd ml-smart-contract-project
python -m venv venv
## en power shell
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r backend/requirements.txt

2. Entrenar el modelo ML

python ml/train_model.py

3. Iniciar red Ethereum local
Usá uno de los dos:

✅ Hardhat (recomendado):

cd contract
npx hardhat node

4. Desplegar el contrato inteligente

python contract/deploy.py

5. Configurar el backend
En backend/app.py, actualizá:


contract_address = "0x...direccion_del_contrato..."

6. Levantar el backend FastAPI

uvicorn backend.app:app --reload --port 8000

🧪 Endpoints disponibles
🔹 /predict (POST)
Realiza una predicción con el modelo ML.


{
  "features": [val1, val2, ..., val30]
}

🔹 /trigger (POST)
Envía la predicción al contrato inteligente.


{
  "prediction": 1
}

✅ Script de prueba completo

Edit
python test/test_workflow.py

📌 Requisitos
Python 3.8+

Node.js 18 LTS (Hardhat no soporta 21+)

Ganache o Hardhat

✅ Extensiones futuras
Usar oráculos (Chainlink)

Automatizar con scripts de frontend

Añadir histórico de predicciones en Solidity

Validación de seguridad y autenticación

🏁 Resultado Final
Podrás conectar un modelo de ML real a una red Ethereum local, y ejecutar lógica blockchain basada en sus predicciones, de forma automática.

### RESUMEN

🧠🔗 Resumen del Proyecto
🎯 Objetivo general:
Integrar un modelo de Machine Learning entrenado en Python con un contrato inteligente desplegado en una red Ethereum local, permitiendo que decisiones automáticas basadas en predicciones se reflejen on-chain.

🔧 Componentes desarrollados:
1. Machine Learning (ml/train_model.py)
Usaste scikit-learn para entrenar un modelo de clasificación binaria (LogisticRegression).

Entrenaste el modelo con un dataset sintético de 30 features.

Guardaste el modelo entrenado como model.pkl usando joblib.

2. Backend API (backend/app.py)
Implementaste un servidor REST con FastAPI que expone 3 endpoints:

POST /predict: recibe un array de 30 números y devuelve una predicción 0 o 1.

POST /trigger: toma la predicción, se conecta al contrato inteligente y actualiza lastPrediction en la blockchain local.

GET /status: consulta el valor actual de lastPrediction() directamente desde el contrato.

Usaste web3.py para interactuar con Ethereum desde Python.

Leés automáticamente la dirección y ABI del contrato desde archivos generados por el script de despliegue.

3. Contrato Inteligente (contract/MLContract.sol)
Escribiste un contrato en Solidity que:

Guarda la última predicción (bool public lastPrediction).

Tiene una función actualizarEstado(bool) para actualizarla.

Tiene una función actuar() para ejecutar lógica condicional basada en la predicción.

4. Script de despliegue (contract/deploy.py)
Compilaste el contrato Solidity con solcx.

Conectaste al nodo local de Hardhat (http://127.0.0.1:8545).

Desplegaste el contrato usando web3.py, y guardaste:

MLContract_address.txt

MLContract_abi.json

5. Red local de Ethereum (Hardhat)
Iniciaste el nodo local con:


npx hardhat node
Usaste las cuentas preconfiguradas con 10.000 ETH para firmar transacciones automáticamente.

🧪 Pruebas realizadas
Probaste POST /predict con datos válidos → predicción devuelta.

Probaste POST /trigger → el contrato se actualizó on-chain.

Probaste GET /status → lectura exitosa desde la blockchain.

Lograste integración completa entre modelo ML, backend y contrato Solidity.

📦 Herramientas y tecnologías
Tecnología	Uso principal
Python + FastAPI	Backend REST API
scikit-learn	Entrenamiento del modelo de ML
web3.py	Interacción con Ethereum desde Python
Solidity	Lógica del contrato inteligente
Hardhat	Red local y cuentas Ethereum
Uvicorn	Servidor ASGI para FastAPI

```
