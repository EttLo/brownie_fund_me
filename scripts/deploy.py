from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    getAccount,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_FundMe():
    account = getAccount()
    # pass the priceFeed address to the contract
    # if we are on a persistent network like rinkeby, use the associated address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print("the network is: ", network.show_active())
    # otherwise deploy mocks
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print("the network is: ", network.show_active(), " mock aggregator deployed")

    fundMe = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    return fundMe


def main():
    deploy_FundMe()
