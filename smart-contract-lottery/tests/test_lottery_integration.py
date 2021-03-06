from brownie import network 
import pytest
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract, fund_with_link
import time
from scripts.deploy_lottery import deploy_lottery

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
         pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from': account})
    lottery.enter({'from':account, 'value': lottery.getEntranceFee()})
    lottery.enter({'from':account, 'value': lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({'from': account})
    time.sleep(130)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0