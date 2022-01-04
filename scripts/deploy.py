from brownie import Lottery, accounts, config, network

NETWORK_ACTIVE = config["networks"][network.show_active()]


def deploy_lottery():
    account = accounts[0]
    lottery = Lottery.deploy(
        NETWORK_ACTIVE.get("price_feed_usd"),
        {"from": account},
    )
    print(lottery.address)


def main():
    deploy_lottery()
