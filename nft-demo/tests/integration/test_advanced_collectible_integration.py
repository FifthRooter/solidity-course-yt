from brownie import network, AdvancedCollectible
import time
import pytest
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible_integration():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('only for integration testing')
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(60)
    assert advanced_collectible.tokenCounter() == 1