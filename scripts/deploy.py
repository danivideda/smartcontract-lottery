from brownie import Lottery, accounts, config
from brownie.network import account
from web3 import Web3

PRIVATE_KEY = config["wallets"]["private_key"]


def deploy_lottery():
    # account = accounts[0]
    account = accounts.add(PRIVATE_KEY)
    lottery = Lottery.deploy(
        "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e", {"from": account}
    )
    print("Deployed!", lottery.address)

    lottery.enter({"from": account, "value": Web3.toWei(0.01, "ether")})


def main():
    deploy_lottery()
