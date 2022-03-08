from scripts.helpful_scripts import getAccount, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_FundMe
from brownie import accounts, network, exceptions
import pytest


def test_fund_withdraw():
    account = getAccount()
    fund_me = deploy_FundMe()
    entrance_fee = fund_me.get_entrance_fee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.AddressToAmount(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.AddressToAmount(account.address) == 0


def test_onlyOwner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
    account = getAccount()
    bad_actor = accounts.add()
    fund_me = deploy_FundMe()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
