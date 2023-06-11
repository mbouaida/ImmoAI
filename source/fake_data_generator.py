import pandas as pd
import numpy as np
from faker import Faker


class FakeDataGenerator:
    """A class used to generate fake data for real estate project."""

    def __init__(self, num_towns=100, num_years=10):
        """Initialize the generator.

        Args:
        num_towns (int): Number of towns to generate data for.
        num_years (int): Number of past years to generate data for.
        """
        self.fake = Faker()
        self.num_towns = num_towns
        self.num_years = num_years

    def generate_towns(self):
        """Generate town names."""
        return [self.fake.city() for _ in range(self.num_towns)]

    def generate_prices(self):
        """Generate random prices per square meter for each year."""
        return np.random.uniform(1000, 5000, (self.num_towns, self.num_years))

    def generate_security_scores(self):
        """Generate random security scores."""
        return np.random.uniform(1, 10, self.num_towns)

    def generate_school_scores(self):
        """Generate random school scores."""
        return np.random.uniform(1, 10, self.num_towns)

    def generate_transport_scores(self):
        """Generate random transport scores."""
        return np.random.uniform(1, 10, self.num_towns)

    def generate_commodities_scores(self):
        """Generate random commodities scores."""
        return np.random.uniform(1, 10, self.num_towns)

    def generate_green_spaces_scores(self):
        """Generate random green spaces scores."""
        return np.random.uniform(1, 10, self.num_towns)

    def generate_data(self):
        """Generate the full dataset and return as a pandas DataFrame."""
        towns = self.generate_towns()
        prices = self.generate_prices()
        security_scores = self.generate_security_scores()
        school_scores = self.generate_school_scores()
        transport_scores = self.generate_transport_scores()
        commodities_scores = self.generate_commodities_scores()
        green_spaces_scores = self.generate_green_spaces_scores()

        data = {
            'town': towns,
            'price_per_sqm': prices.tolist(),  # Convert numpy array to list
            'security_score': security_scores,
            'school_score': school_scores,
            'transport_score': transport_scores,
            'commodities_score': commodities_scores,
            'green_spaces_score': green_spaces_scores,
        }

        df = pd.DataFrame(data)
        return df


if __name__ == "__main__":
    generator = FakeDataGenerator()
    df = generator.generate_data()

    # Save the generated data to a CSV file
    df.to_csv('data.csv', index=False)
