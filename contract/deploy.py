import json
from solcx import compile_standard, install_solc
from web3 import Web3

# Leer el contrato
with open("contract/MLContract.sol", "r") as file:
    contract_source_code = file.read()

# Instalar Solidity 0.8.0 si no está
install_solc("0.8.0")

# Compilar contrato
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"MLContract.sol": {"content": contract_source_code}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.0")

abi = compiled_sol["contracts"]["MLContract.sol"]["MLContract"]["abi"]
bytecode = compiled_sol["contracts"]["MLContract.sol"]["MLContract"]["evm"]["bytecode"]["object"]

# Conexión a nodo local (Hardhat)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise Exception("Error: no se pudo conectar a Hardhat en http://127.0.0.1:8545")

# Cuenta Hardhat #0
account_address = w3.eth.accounts[0]

# Crear contrato
MLContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Obtener nonce de la cuenta
nonce = w3.eth.get_transaction_count(account_address)

# Crear transacción
transaction = MLContract.constructor().build_transaction({
    "chainId": 31337,  # Hardhat por defecto
    "gasPrice": w3.to_wei("20", "gwei"),
    "from": account_address,
    "nonce": nonce
})

# Firmar y enviar transacción (no hace falta clave privada con Hardhat local)
tx_hash = w3.eth.send_transaction(transaction)

# Esperar a que se mine
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

print(f"✅ Contrato desplegado en: {contract_address}")

# Guardar ABI y dirección
with open("contract/MLContract_abi.json", "w") as abi_file:
    json.dump(abi, abi_file)
with open("contract/MLContract_address.txt", "w") as addr_file:
    addr_file.write(contract_address)
