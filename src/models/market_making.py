import numpy as np
import matplotlib.pyplot as plt
from src.utils.helpers import calculate_pnl, calculate_sharpe_ratio


class MidPriceModel:
    def __init__(self, initial_price, volatility, risk_free_rate, model_type="GBM"):
        self.price = initial_price
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
        self.model_type = model_type  # Only "GBM" is supported now

    def simulate_price_dynamics(self, time_step):
        if time_step <= 0:
            raise ValueError("Time step must be positive.")

        drift = (self.risk_free_rate - 0.5 * self.volatility**2) * time_step
        shock = self.volatility * np.sqrt(time_step) * np.random.normal()

        if self.model_type == "GBM":
            self.price *= np.exp(drift + shock)
        else:
            raise ValueError("Unsupported model type. Only 'GBM' is supported.")

        return self.price


class TradeExecution:
    def __init__(self, execution_probability):
        self.execution_probability = execution_probability

    def calculate_execution_intensity(self, quote_distance):
        """
        Calculate the execution intensity based on quote distance using an exponential decay function.
        :param quote_distance: Distance of the quote from the mid-price.
        :return: Execution intensity.
        """
        A = 1.0  # Base intensity
        k = 0.1  # Sensitivity to distance
        return A * np.exp(-k * quote_distance)


class MarketMaker:
    def __init__(self, mid_price_model, trade_execution, risk_aversion=0.1, base_intensity=1.0, sensitivity=0.1):
        self.mid_price_model = mid_price_model
        self.trade_execution = trade_execution
        self.risk_aversion = risk_aversion
        self.base_intensity = base_intensity
        self.sensitivity = sensitivity
        self.inventory = 0  # Initialize inventory
        self.trades = []  # Initialize trades as an empty list
        self.pnl = 0  # Initialize profit and loss

    def calculate_optimal_quotes(self, volatility):
        """
        Calculate the optimal bid and ask distances based on the Avellaneda-Stoikov model.
        :param volatility: Current market volatility.
        :return: Optimal bid and ask distances (δ_b, δ_a).
        """
        half_spread = self.risk_aversion * volatility**2 / (2 * self.base_intensity)
        inventory_adjustment = self.inventory * self.risk_aversion * volatility

        delta_b = half_spread - inventory_adjustment
        delta_a = half_spread + inventory_adjustment

        return delta_b, delta_a

    def run_simulation(self, steps):
        """
        Simulate the market-making process over a given number of steps.
        :param steps: Number of simulation steps.
        """
        try:
            for step in range(steps):
                # Simulate mid-price dynamics
                mid_price = self.mid_price_model.simulate_price_dynamics(time_step=1)

                # Calculate optimal quotes
                delta_b, delta_a = self.calculate_optimal_quotes(self.mid_price_model.volatility)
                bid_price = mid_price - delta_b
                ask_price = mid_price + delta_a

                # Simulate trade arrivals
                if self.trade_execution.calculate_execution_intensity(delta_b) > np.random.uniform():
                    self.inventory += 1  # Buy at bid
                    self.pnl -= bid_price

                if self.trade_execution.calculate_execution_intensity(delta_a) > np.random.uniform():
                    self.inventory -= 1  # Sell at ask
                    self.pnl += ask_price

            # Log performance metrics
            self.log_performance()
        except Exception as e:
            print(f"An error occurred during simulation: {e}")

    def optimize_quotes(self, inventory, volatility):
        """
        Dynamically adjust bid and ask spreads based on inventory, volatility, and execution probability.
        Incorporates Sharpe Ratio into the optimization process.
        :param inventory: Current inventory level.
        :param volatility: Current market volatility.
        :return: Optimal bid and ask spreads.
        """
        base_spread = 0.01  # Base spread percentage
        inventory_penalty = 0.005 * abs(inventory)  # Penalty for large inventory
        volatility_adjustment = 0.01 * volatility  # Adjustment based on volatility

        # Calculate Sharpe Ratio for risk adjustment
        sharpe_ratio = self.calculate_sharpe_ratio()
        sharpe_adjustment = 0.01 / (1 + sharpe_ratio) if sharpe_ratio > 0 else 0.02

        optimal_bid_spread = base_spread + inventory_penalty + volatility_adjustment + sharpe_adjustment
        optimal_ask_spread = base_spread + inventory_penalty + volatility_adjustment + sharpe_adjustment

        return optimal_bid_spread, optimal_ask_spread

    def calculate_sharpe_ratio(self):
        if len(self.trades) < 2:
            return 0  # Not enough data to calculate Sharpe Ratio
        prices = [trade["price"] for trade in self.trades]
        returns = np.diff(prices)
        if returns.std() == 0:  # Handle zero standard deviation
            return 0
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
        returns = np.diff(prices)  # Calculate returns for performance metrics
        sharpe_ratio = calculate_sharpe_ratio(returns)

        # Calculate Sortino ratio
        downside_returns = [r for r in returns if r < 0]
        if len(downside_returns) > 0:
            sortino_ratio = np.mean(returns) / np.std(downside_returns)
        else:
            sortino_ratio = float('inf')

        # Calculate maximum drawdown
        cumulative_returns = np.cumsum(returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = peak - cumulative_returns
        max_drawdown = np.max(drawdown)

        print(f"Cumulative P&L: {pnl}, Sharpe Ratio: {sharpe_ratio}, Sortino Ratio: {sortino_ratio}, Maximum Drawdown: {max_drawdown}")

    def calculate_objective(self, pnl, inventory):
        """
        Calculate the objective function with an inventory penalty.
        :param pnl: Profit and Loss.
        :param inventory: Current inventory level.
        :return: Objective value.
        """
        risk_penalty = 0.05 * inventory**2  # Penalize large inventory deviations
        return pnl - risk_penalty

    def run_monte_carlo_simulation(self, num_simulations, steps):
        """
        Run multiple simulation paths and aggregate results.
        Validates the framework by ensuring meaningful parameter calibration.
        :param num_simulations: Number of Monte Carlo simulation paths.
        :param steps: Number of steps in each simulation.
        :return: Aggregated results including average P&L and Sharpe ratio.
        """
        all_pnls = []
        all_sharpe_ratios = []

        for _ in range(num_simulations):
            self.run_simulation(steps)
            pnl = calculate_pnl(self.mid_price_model.price, self.inventory)
            sharpe_ratio = self.calculate_sharpe_ratio()

            all_pnls.append(pnl)
            all_sharpe_ratios.append(sharpe_ratio)

        average_pnl = np.mean(all_pnls)
        average_sharpe_ratio = np.mean(all_sharpe_ratios)

        print(f"Monte Carlo Simulation Results:")
        print(f"Average P&L: {average_pnl}")
        print(f"Average Sharpe Ratio: {average_sharpe_ratio}")

        return {
            "average_pnl": average_pnl,
            "average_sharpe_ratio": average_sharpe_ratio
        }

    def run_sensitivity_analysis(self, parameter_name, parameter_values, steps):
        """
        Perform sensitivity analysis by varying a key parameter and observing performance metrics.
        :param parameter_name: Name of the parameter to vary (e.g., 'volatility').
        :param parameter_values: List of values for the parameter.
        :param steps: Number of steps in each simulation.
        :return: Results of the sensitivity analysis.
        """
        results = {}

        for value in parameter_values:
            if parameter_name == 'volatility':
                self.mid_price_model.volatility = value
            elif parameter_name == 'execution_probability':
                self.trade_execution.execution_probability = value
            else:
                raise ValueError(f"Unsupported parameter: {parameter_name}")

            monte_carlo_results = self.run_monte_carlo_simulation(num_simulations=10, steps=steps)
            results[value] = monte_carlo_results

        print("Sensitivity Analysis Results:")
        for param_value, metrics in results.items():
            print(f"{parameter_name} = {param_value}: {metrics}")

        return results

    def run_stress_test(self, stress_scenarios, steps):
        """
        Simulate extreme market conditions to evaluate strategy robustness.
        :param stress_scenarios: List of stress scenarios (e.g., high volatility, low liquidity).
        :param steps: Number of steps in each simulation.
        :return: Results of the stress tests.
        """
        results = {}

        for scenario in stress_scenarios:
            if scenario == 'high_volatility':
                self.mid_price_model.volatility *= 2  # Double the volatility
            elif scenario == 'low_liquidity':
                self.trade_execution.execution_probability /= 2  # Halve the execution probability
            else:
                raise ValueError(f"Unsupported stress scenario: {scenario}")

            monte_carlo_results = self.run_monte_carlo_simulation(num_simulations=10, steps=steps)
            results[scenario] = monte_carlo_results

            # Reset parameters after each scenario
            self.mid_price_model.volatility /= 2 if scenario == 'high_volatility' else 1
            self.trade_execution.execution_probability *= 2 if scenario == 'low_liquidity' else 1

        print("Stress Test Results:")
        for scenario, metrics in results.items():
            print(f"Scenario: {scenario}, Metrics: {metrics}")

        return results

    def plot_mid_price(self, mid_prices):
        plt.figure(figsize=(10, 5))
        plt.plot(mid_prices, label='Mid-Price')
        plt.title('Mid-Price Dynamics')
        plt.xlabel('Time Steps')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        plt.savefig('mid_price_dynamics.png')
        plt.show()

    def plot_inventory(self, inventory):
        plt.figure(figsize=(10, 5))
        plt.plot(inventory, label='Inventory')
        plt.title('Inventory Evolution')
        plt.xlabel('Time Steps')
        plt.ylabel('Inventory Level')
        plt.legend()
        plt.grid()
        plt.savefig('inventory_evolution.png')
        plt.show()

    def plot_pnl(self, pnl):
        plt.figure(figsize=(10, 5))
        plt.plot(pnl, label='Cumulative PnL')
        plt.title('Profit and Loss (PnL) Over Time')
        plt.xlabel('Time Steps')
        plt.ylabel('PnL')
        plt.legend()
        plt.grid()
        plt.savefig('pnl_over_time.png')
        plt.show()