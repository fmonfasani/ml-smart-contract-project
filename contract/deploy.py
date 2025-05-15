import json
from solcx import compile_standard, install_solc
from web3 import Web3

# Leer el código del contrato
with open("contract/MLContract.sol", "r") as file:
    contract_source_code = file.read()

# Instalar compilador Solidity versión 0.8.0 si no está instalado
install_solc("0.8.0")

# Compilar el contrato Solidity
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

# Extraer ABI y bytecode compilado
abi = compiled_sol["contracts"]["MLContract.sol"]["MLContract"]["abi"]
bytecode = compiled_sol["contracts"]["MLContract.sol"]["MLContract"]["evm"]["bytecode"]["object"]

# Conectar a la red Ethereum local (Ganache en este ejemplo)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.isConnected():
    raise Exception("Error: no se pudo conectar a Ganache/Hardhat en http://127.0.0.1:8545")

# Seleccionar la cuenta por defecto (primera cuenta de Ganache)
w3.eth.default_account = w3.eth.accounts[0]

# Construir el contrato en Web3
MLContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Desplegar el contrato
print("Desplegando contrato...")
tx_hash = MLContract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"Contrato desplegado exitosamente en la dirección: {contract_address}")

# Guardar ABI y dirección en archivos JSON para uso posterior (opcional)
with open("contract/MLContract_abi.json", "w") as abi_file:
    json.dump(abi, abi_file)
with open("contract/MLContract_address.txt", "w") as addr_file:
    addr_file.write(contract_address)
