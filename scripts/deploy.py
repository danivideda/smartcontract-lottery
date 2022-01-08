from brownie import Lottery, accounts, config, network
from toolz.itertoolz import get
from scripts.helpful_scripts import get_account, get_contract

NETWORK_ACTIVE = config["networks"][network.show_active()]
# ORACLE = NETWORK_ACTIVE["chainlink"]


def deploy_lottery():
    account = get_account()
    # lottery = Lottery.deploy(
    #     NETWORK_ACTIVE.get("eth_usd_price_feed"),
    #     ORACLE.get("vrf_coordinator"),
    #     ORACLE.get("link_token"),
    #     ORACLE.get("key_hash"),
    #     ORACLE.get("fee"),
    #     {"from": account},
    # )
    # print(lottery)

    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        NETWORK_ACTIVE.get("key_hash"),
        NETWORK_ACTIVE.get("fee"),
        {"from": account},
        publish_source=NETWORK_ACTIVE.get("verify", False),
    )
    print("Deployed Lottery!", lottery.address)


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery has started!")


def main():
    print(network.show_active())
    deploy_lottery()
    start_lottery()
