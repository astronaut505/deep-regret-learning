# This file serves as the entry point for the application. It initializes the simulation framework and orchestrates the execution of the market making model.

import sys
import os

# Add the parent directory of src to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import logging
from models.market_making import MidPriceModel, TradeExecution, MarketMaker


def setup_logging(log_level):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging initialized.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Optimal Market Making Simulation")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the configuration file."
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level."
    )
    return parser.parse_args()

import json
from models.market_making import MidPriceModel, TradeExecution, MarketMaker

def main():
    args = parse_arguments()
    setup_logging(args.log_level)

    try:
        # Load configuration
        with open(args.config, 'r') as config_file:
            config = json.load(config_file)

        # Initialize components
        mid_price_model = MidPriceModel(config["initial_price"], config["volatility"])
        trade_execution = TradeExecution(config["execution_probability"])
        market_maker = MarketMaker(mid_price_model, trade_execution)

        # Run the simulation
        market_maker.run_simulation(config["simulation_steps"])
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        raise

if __name__ == "__main__":
    main()