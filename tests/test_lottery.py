from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()].get("eth_usd_price_feed"),
        {"from": account},
    )
    # 0.01575299307 ETH date: 8 January 2022 6:25
    # 15752993070000000 WEI
    assert lottery.getEntranceFee() > Web3.toWei(0.015, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.018, "ether")
