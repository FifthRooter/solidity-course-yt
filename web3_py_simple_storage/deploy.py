import os
from solcx import compile_standard, install_solc
from web3 import Web3
import json
from dotenv import load_dotenv

load_dotenv()

install_solc('0.6.0')

with open('./SimpleStorage.sol', 'r') as file:
    simple_storage_file = file.read()

# compile solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol": {
                "content": simple_storage_file
        }},
        "settings": {
            "outputSelection" : {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
)

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# for connecting to Ganache
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
chain_id = 1337
my_address = '0x5ea16bE14FbE57Aaecd9e4c886e0BAD357817fA1'
private_key = os.getenv('PRIVATE_KEY')

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Build the transaction
transaction = SimpleStorage.constructor().buildTransaction({
    'chainId': chain_id,
    'from': my_address,
    'nonce': nonce
    })

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with the contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print('Updating contract...')
store_transaction = simple_storage.functions.store(15).buildTransaction({
    'chainId': chain_id,
    'from': my_address,
    'nonce': nonce + 1
})

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print('Updated!')
print(simple_storage.functions.retrieve().call())
