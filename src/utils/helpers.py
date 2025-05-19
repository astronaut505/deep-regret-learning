def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    if len(returns) == 0:
        print("Warning: Returns array is empty. Returning None.")
        return None  # Fallback value for empty returns
    if returns.std() == 0:
        raise ValueError("Standard deviation of returns cannot be zero.")
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std()

def plot_inventory(inventory, title='Inventory Over Time', save_path=None):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(inventory, label='Inventory')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Inventory Level')
    plt.legend()
    plt.grid()
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

def simulate_trades(trade_arrival_rate, duration):
    import numpy as np
    trades = np.random.poisson(trade_arrival_rate, duration)
    return trades

def calculate_pnl(prices, trade_sizes):
    """
    Calculate P&L from executed trades.
    :param prices: List of trade prices.
    :param trade_sizes: List of trade sizes. Positive = buy, Negative = sell.
    :return: Total P&L.
    """
    prices = np.array(prices)
    trade_sizes = np.array(trade_sizes)
    return -np.sum(prices * trade_sizes)
