import brownie
from scripts.aave_borrow import (
    get_asset_price,
    get_lending_pool,
    approve_erc20,
    get_account,
    get_borrowable_data,
)
from brownie import config, network, accounts
from web3 import Web3


def test_borrowing():
    account = get_account()
    lending_pool = get_lending_pool()
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.50)
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account, "gas_limit": Web3.toWei(1, "ether"), "allow_revert": True},
    )
    borrow_tx.wait(1)
    assert borrow_tx is not True
    with brownie.reverts():
        print(f"{borrow_tx.revert_msg}")


def test_get_asset_price():
    # Arrange / Act
    asset_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # Assert
    assert asset_price > 0


def test_get_lending_pool():
    # Arrange / Act
    lending_pool = get_lending_pool()
    # Assert
    assert lending_pool is not None


def test_approve_erc20():
    # Arrange
    account = get_account()
    lending_pool = get_lending_pool()
    amount = 1000000000000000000  # 1
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    # Act
    tx = approve_erc20(amount, lending_pool.address, erc20_address, account)
    # Assert
    assert tx is not True
