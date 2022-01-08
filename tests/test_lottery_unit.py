from brownie import Lottery, accounts, config, network
from scripts.deploy import deploy_lottery
from web3 import Web3


def test_deploy_lottery():
    deploy_lottery()


def test_get_entrance_fee():
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    # In mock
    # 2000 USD / ETH
    # 2000/1ETH == 50/(x)ETH ==> 0.025 ETH
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    assert expected_entrance_fee == entrance_fee
