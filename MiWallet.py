import json
import os
from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod

# Configuración de la red (TestNet)
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
HEADERS = {"User-Agent": "algod-python"}
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS, HEADERS)

# Ruta del archivo donde se guarda la wallet
WALLET_FILE = "mi_wallet.json"

# ----------------------------------------------------------------------
# Crear o cargar cuenta principal
def obtener_wallet():
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as f:
            data = json.load(f)
            private_key = mnemonic.to_private_key(data["mnemonic"])
            address = data["address"]
            print("\n✅ Wallet cargada desde archivo.")
    else:
        private_key, address = account.generate_account()
        passphrase = mnemonic.from_private_key(private_key)
        with open(WALLET_FILE, "w") as f:
            json.dump({"address": address, "mnemonic": passphrase}, f)
        print("\n🆕 Wallet creada y guardada.")
        print(f"Dirección : {address}")
        print(f"Frase mnemónica : {passphrase}")
    return private_key, address

# ----------------------------------------------------------------------
# Consultar saldo
def obtener_saldo(address):
    acct_info = algod_client.account_info(address)
    micro_algo = acct_info.get('amount', 0)
    algo = micro_algo / 1_000_000
    print(f"Saldo de {address[:6]}... : {algo} ALGO")
    return micro_algo

# ----------------------------------------------------------------------
# Enviar ALGO
def enviar_algo(sender_sk, sender_addr, receiver_addr, amount_micro):
    params = algod_client.suggested_params()
    txn = transaction.PaymentTxn(
        sender=sender_addr,
        sp=params,
        receiver=receiver_addr,
        amt=amount_micro,
        note=b"Transferencia desde wallet fija"
    )
    signed_txn = txn.sign(sender_sk)
    txid = algod_client.send_transaction(signed_txn)
    print(f"\nTransacción enviada. ID: {txid}")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 5)
        print("✅ Confirmada en el bloque:", confirmed_txn.get('confirmed-round'))
    except Exception as e:
        print("⚠️ Error esperando confirmación:", e)

# ----------------------------------------------------------------------
if __name__ == "__main__":
    private_key, address = obtener_wallet()
    obtener_saldo(address)

    input("\nPresiona ENTER después de recibir fondos desde la faucet...")

    obtener_saldo(address)

    # Crear receptor temporal
    recv_sk, recv_addr = account.generate_account()
    print(f"\nReceptor creado: {recv_addr}")
    input("Presiona ENTER para enviar 0.1 ALGO...")

    enviar_algo(private_key, address, recv_addr, 100_000)

    print("\n=== Saldos finales ===")
    obtener_saldo(address)
    obtener_saldo(recv_addr)