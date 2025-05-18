import unittest
from src.models.market_making import MidPriceModel, TradeExecution, MarketMaker

class TestMarketMaking(unittest.TestCase):

    def setUp(self):
        self.mid_price_model = MidPriceModel()
        self.trade_execution = TradeExecution()
        self.market_maker = MarketMaker()

    def test_mid_price_simulation(self):
        # Test the mid-price simulation functionality
        result = self.mid_price_model.simulate()
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, float))

    def test_execution_intensity_calculation(self):
        # Test the execution intensity calculation
        intensity = self.trade_execution.calculate_intensity()
        self.assertIsInstance(intensity, float)
        self.assertGreaterEqual(intensity, 0)

    def test_market_maker_optimization(self):
        # Test the market maker optimization results
        optimization_result = self.market_maker.optimize_quotes()
        self.assertIsNotNone(optimization_result)
        self.assertTrue(isinstance(optimization_result, dict))

    def test_invalid_mid_price_simulation(self):
        # Test mid-price simulation with invalid parameters
        with self.assertRaises(ValueError):
            self.mid_price_model.simulate(invalid_param=True)

    def test_negative_execution_intensity(self):
        # Test execution intensity calculation with negative inputs
        with self.assertRaises(ValueError):
            self.trade_execution.calculate_intensity(-1)

    def test_market_maker_no_trades(self):
        # Test market maker optimization when no trades occur
        self.market_maker.trades = []  # Simulate no trades
        optimization_result = self.market_maker.optimize_quotes()
        self.assertEqual(optimization_result, {})  # Expect empty result

    def test_market_maker_large_inventory(self):
        # Test market maker behavior with large inventory
        self.market_maker.inventory = 1e6  # Simulate large inventory
        optimization_result = self.market_maker.optimize_quotes()
        self.assertIsNotNone(optimization_result)
        self.assertTrue(isinstance(optimization_result, dict))

if __name__ == '__main__':
    unittest.main()