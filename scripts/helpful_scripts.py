from brownie import (
    Lottery,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    accounts,
    network,
    config,
    Contract,
)

LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-cli"]
LOCAL_FORKED_ENVIRONMENT = ["mainnet-fork"]
PRIVATE_KEY = config["wallets"]["from_key"]
NETWORK_ACTIVE = config["networks"][network.show_active()]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT
        or network.show_active() in LOCAL_FORKED_ENVIRONMENT
    ):
        return accounts[0]
    return accounts.add(PRIVATE_KEY)


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined. Otherwise, it will deploy a mock version of that contract and return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: the most recently deployed version of this contract.
            MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        if len(contract_type) <= 0:  # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]  # MockV3Aggregator[-1]
    else:
        contract_address = NETWORK_ACTIVE.get(contract_name)
        # Address
        # ABI (taken from MockV3Aggregator localy build)
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 2000 * 10 ** 8


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"Funded the contract with ${amount / (10 ** 18)} LINK")
    return tx
