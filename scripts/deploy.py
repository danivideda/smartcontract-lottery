from brownie import Lottery, accounts, config, network
from toolz.itertoolz import get
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time


def deploy_lottery():
    account = get_account()

    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()].get("key_hash"),
        config["networks"][network.show_active()].get("fee"),
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery!", lottery.address)
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery has started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + (1 * 10 ** 8)  # 0.1 GWEI
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You've entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Fund contract with LINK
    tx_fund_link = fund_with_link(lottery.address)
    tx_fund_link.wait(1)
    tx_ending_lottery = lottery.endLottery({"from": account})
    tx_ending_lottery.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    print(network.show_active())
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
