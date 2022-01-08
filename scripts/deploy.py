from brownie import Lottery, accounts, config, network

NETWORK_ACTIVE = config["networks"][network.show_active()]


def deploy_lottery():
    account = accounts[0]
    lottery = Lottery.deploy(
        NETWORK_ACTIVE.get("eth_usd_price_feed"),
        {"from": account},
    )
    print(lottery.address)
    print(lottery.getEntranceFee())


def main():
    print(network.show_active())
    deploy_lottery()
