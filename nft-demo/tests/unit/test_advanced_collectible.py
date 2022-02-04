from brownie import network, AdvancedCollectible
import pytest
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy_and_create()
    requestId = creation_tx.events['requestedCollectible']['requestId']
    RANDOM_NUMBER = 888
    get_contract('vrf_coordinator').callBackWithRandomness(requestId, RANDOM_NUMBER , advanced_collectible.address, {'from': account})
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == RANDOM_NUMBER % 3 