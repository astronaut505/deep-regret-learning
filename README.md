# Optimal Market Making Model

This project simulates and optimizes trading strategies for a market maker, focusing on balancing profit and risk under inventory and execution uncertainties.

## Project Structure

- `src/main.py`: Entry point for running the simulation.
- `src/models/market_making.py`: Core implementation of the market making model.
- `src/utils/helpers.py`: Utility functions for calculations and plotting.
- `src/config.json`: Configuration file for simulation parameters.
- `requirements.txt`: Dependencies for the project.

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the simulation:

```
python src/main.py --config src/config.json
```

### Configuration

Modify `src/config.json` to adjust parameters:

```json
{
  "initial_price": 100,
  "volatility": 0.05,
  "execution_probability": 0.5,
  "simulation_steps": 10000
}
```

## License

This project is licensed under the MIT License.
