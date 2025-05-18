# Optimal Market Making Model

This project implements an Optimal Market Making model designed to simulate and optimize trading strategies in financial markets. The model focuses on mid-price dynamics, trade arrival, execution probabilities, and optimization objectives.

## Project Structure

- `src/main.py`: Entry point for the application. Initializes the simulation framework and orchestrates the execution of the market making model.
- `src/models/market_making.py`: Core implementation of the Optimal Market Making model, including classes and functions for modeling price dynamics and optimizing quotes.
- `src/utils/helpers.py`: Utility functions for data handling, statistical calculations, and plotting results.
- `src/tests/test_market_making.py`: Unit tests for the market making model to ensure core functionalities work as expected.
- `src/config.json`: Configuration file for simulation parameters.
- `requirements.txt`: Lists the dependencies required for the project.
- `.gitignore`: Specifies files and directories to be ignored by version control.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd optimal-market-making
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the market making simulation, execute the following command:

```
python src/main.py --config src/config.json
```

### Configuration File

The `src/config.json` file contains the parameters for the simulation. You can modify the following fields:

- `initial_price`: The starting price of the asset.
- `volatility`: The volatility of the mid-price dynamics.
- `execution_probability`: The base probability of trade execution.
- `simulation_steps`: The number of steps to simulate.

Example:

```json
{
  "initial_price": 100,
  "volatility": 0.02,
  "execution_probability": 0.5,
  "simulation_steps": 1000
}
```

## Testing

To run the unit tests, execute:

```
python -m unittest discover -s src/tests
```

The tests cover:

- Mid-price simulation.
- Execution intensity calculations.
- Market maker optimization logic.

## Model Components

- **MidPriceModel**: Models the dynamics of the mid-price in the market.
- **TradeExecution**: Handles the execution of trades and calculates execution probabilities.
- **MarketMaker**: Implements the market making strategy and optimizes quotes based on market conditions.

## Results

The project includes functionality to visualize results, such as inventory levels and performance metrics. Use the utility functions in `helpers.py` to generate plots and analyze the performance of the market making strategy.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
