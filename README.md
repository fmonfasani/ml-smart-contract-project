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
git clone <repo-url>
cd ml-smart-contract-project
python -m venv venv
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



---

¿Querés que lo guarde como archivo `README.md` directamente o te lo paso también como `.pdf` para documentació
```
