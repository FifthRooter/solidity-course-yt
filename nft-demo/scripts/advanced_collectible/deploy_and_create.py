from scripts.helpers import get_account, OPENSEA_URL, network, config, get_contract, fund_with_link
from brownie import AdvancedCollectible
from web3 import Web3

FEE = Web3.toWei(0.05, 'ether')

def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract('vrf_coordinator'),
        get_contract('link_token'),
        config['networks'][network.show_active()]['keyhash'],
        config['networks'][network.show_active()]['fee'],
        {'from': account},
        publish_source=True
        )
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({'from': account})
    creating_tx.wait(1)
    print('New token has been created!')
   
def main():
    deploy_and_create()