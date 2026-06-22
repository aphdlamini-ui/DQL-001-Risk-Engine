from risk_calculator import (
    calculate_risk,
    calculate_position_size,
    calculate_risk_reward,
    portfolio_exposure
)

# Account setup
account_balance = 2000
risk_percent = 1

risk_amount = calculate_risk(account_balance, risk_percent)

print("Risk per trade:", risk_amount)

# Position sizing example (generic hybrid model)
position = calculate_position_size(
    risk_amount=risk_amount,
    stop_loss_pips=50,
    pip_value=1
)

print("Position size:", position)

# Risk reward example
rr = calculate_risk_reward(
    entry=100,
    stop_loss=95,
    take_profit=120
)

print("Risk:Reward:", rr)

# Portfolio exposure
exposure = portfolio_exposure([20, 15, 10])
print("Total exposure:", exposure)