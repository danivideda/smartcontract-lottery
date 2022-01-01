from brownie import Lottery, accounts


def deploy_lottery():
    account = accounts[0]
    lottery = Lottery.deploy(
        "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e", {"from": account}
    )
    print(lottery.address)


def main():
    deploy_lottery()
