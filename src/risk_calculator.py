# src/risk_calculator.py

def calculate_risk(account_balance, risk_percent):
    """
    Calculates how much money you are risking per trade.
    """
    return account_balance * (risk_percent / 100)


def calculate_position_size(risk_amount, stop_loss_pips, pip_value):
    """
    Calculates position size based on risk.

    Formula:
    position_size = risk_amount / (stop_loss * pip_value)
    """
    if stop_loss_pips == 0:
        return 0

    return risk_amount / (stop_loss_pips * pip_value)


def calculate_risk_reward(entry, stop_loss, take_profit):
    """
    Returns risk:reward ratio
    """
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)

    if risk == 0:
        return 0

    return reward / risk


def portfolio_exposure(current_risk_list):
    """
    Calculates total portfolio risk exposure.
    Example input: [20, 15, 10]
    """
    return sum(current_risk_list)