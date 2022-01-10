from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
    fund_with_link,
    get_account,
)
from scripts.deploy import deploy_lottery
import pytest


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()

    account = get_account()
    lottery = deploy_lottery()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    tx = lottery.endLottery({"from": account})
    tx.wait(2)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
