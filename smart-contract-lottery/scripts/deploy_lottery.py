from scripts.helpers import get_account, get_contract, config, fund_with_link
from brownie import Lottery, network, config
import time

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['keyhash'],
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify', False)
    )
    print('Deployed Lottery!')
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({'from':account})
    starting_tx.wait(1)
    print('The lottery has started!')

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee()
    print(f'Entrance fee is: {value}')
    tx = lottery.enter({'from': account, 'value': value})
    tx.wait(1)
    print('You entered the lottery!')

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # 1) Fund the contract
    # 2) End the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)

    ending_transaction = lottery.endLottery({'from': account})
    ending_transaction.wait(1)
    time.sleep(120)
    print(f'{lottery.recentWinner()} is the new winner!')

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()