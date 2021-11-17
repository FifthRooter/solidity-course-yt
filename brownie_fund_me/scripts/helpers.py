from brownie import network, MockV3Aggregator, config, accounts

FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 2000_000_000_00

def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def deploy_mocks():
    print(f'The active network is {network.show_active()}')
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
            mock_aggregator = MockV3Aggregator.deploy(DECIMALS,STARTING_PRICE, {'from': get_account()})
    print('Mocks deployed')