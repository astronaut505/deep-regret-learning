import numpy as np
from src.utils.helpers import calculate_pnl, calculate_sharpe_ratio


class MidPriceModel:
    def __init__(self, initial_price, volatility):
        self.price = initial_price
        self.volatility = volatility

    def simulate_price_dynamics(self, time_step):
        if time_step <= 0:
            raise ValueError("Time step must be positive.")
        drift = 0  # Assuming no drift for simplicity
        shock = self.volatility * np.sqrt(time_step) * np.random.normal()
        self.price *= np.exp(drift + shock)
        return self.price


class TradeExecution:
    def __init__(self, execution_probability):
        self.execution_probability = execution_probability

    def calculate_execution_intensity(self, quote_distance):
        A = 1.0  # Base intensity
        k = 0.1  # Sensitivity to distance
        return A * np.exp(-k * quote_distance)


class MarketMaker:
    def __init__(self, mid_price_model, trade_execution):
        self.mid_price_model = mid_price_model
        self.trade_execution = trade_execution
        self.inventory = 0
        self.trades = []
        self.pnl = 0

    def run_simulation(self, steps):
        try:
            for step in range(steps):
                # Simulate price dynamics
                self.mid_price_model.simulate_price_dynamics(1)

                # Optimize quotes
                quotes = self.optimize_quotes()
                print(f"Step {step + 1}/{steps}: Bid = {quotes['bid']}, Ask = {quotes['ask']}")

                # Simulate trades
                self.simulate_trades(1)
                print(f"Inventory after step {step + 1}: {self.inventory}")

            # Log performance metrics
            self.log_performance()
        except Exception as e:
            print(f"An error occurred during simulation: {e}")

    def optimize_quotes(self):
        # Adjust spread dynamically based on Sharpe Ratio
        sharpe_ratio = self.calculate_sharpe_ratio()
        spread = 0.02 + 0.01 * abs(self.inventory) / 100
        if sharpe_ratio < 0.05:  # Adjust spread if Sharpe Ratio is low
            spread *= 1.5
        bid_price = self.mid_price_model.price * (1 - spread / 2)
        ask_price = self.mid_price_model.price * (1 + spread / 2)
        return {"bid": bid_price, "ask": ask_price}

    def calculate_sharpe_ratio(self):
        if len(self.trades) < 2:
            return 0  # Not enough data to calculate Sharpe Ratio
        prices = [trade["price"] for trade in self.trades]
        returns = np.diff(prices)
        return calculate_sharpe_ratio(returns)

    def simulate_trades(self, num_trades):
        for _ in range(num_trades):
            trade_size = np.random.randint(1, 10)
            intensity = self.trade_execution.calculate_execution_intensity(trade_size)
            if np.random.uniform(0, 1) < intensity:
                trade_direction = np.random.choice(["buy", "sell"])
                if trade_direction == "buy":
                    self.inventory += trade_size
                    self.pnl -= trade_size * self.mid_price_model.price
                else:
                    self.inventory -= trade_size
                    self.pnl += trade_size * self.mid_price_model.price
                self.trades.append({"size": trade_size, "price": self.mid_price_model.price, "type": trade_direction})

    def log_performance(self):
        prices = [trade["price"] for trade in self.trades]
        inventory = [trade["size"] for trade in self.trades]
        pnl = calculate_pnl(prices, inventory)
        sharpe_ratio = calculate_sharpe_ratio(np.diff(prices))
        print(f"Cumulative P&L: {pnl}, Sharpe Ratio: {sharpe_ratio}")

    def calculate_objective(self, pnl, inventory):
        # Increase inventory penalty to reduce risk
        risk_penalty = 0.05 * inventory**2  # More aggressive penalty
        return pnl - risk_penalty