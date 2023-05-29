import numpy as np

def binomial_pricing(S, K, r, T, N, option_type='call'):
    """
    Binomial asset pricing model for European options.

    Parameters:
    - S: initial asset price
    - K: strike price
    - r: risk-free interest rate
    - T: time to maturity (in years)
    - N: number of time steps
    - option_type: type of option ('call' or 'put')

    Returns the option price.
    """

    # Calculate time step
    dt = T / N

    # Calculate up and down factors
    u = np.exp(r * dt)
    d = 1 / u

    # Calculate the probability of an up movement
    p = (np.exp(r * dt) - d) / (u - d)

    # Create empty arrays for stock prices and option values
    stock_prices = np.zeros((N + 1, N + 1))
    option_values = np.zeros((N + 1, N + 1))

    # Generate stock price tree
    stock_prices[0, 0] = S
    for i in range(1, N + 1):
        stock_prices[i, 0] = stock_prices[i - 1, 0] * u
        for j in range(1, i + 1):
            stock_prices[i, j] = stock_prices[i - 1, j - 1] * d

    # Calculate option values at maturity
    if option_type == 'call':
        option_values[N] = np.maximum(stock_prices[N] - K, 0)
    elif option_type == 'put':
        option_values[N] = np.maximum(K - stock_prices[N], 0)

    # Backward iteration to calculate option values at earlier time steps
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            option_values[i, j] = np.exp(-r * dt) * (p * option_values[i + 1, j + 1] + (1 - p) * option_values[i + 1, j])

    return option_values[0, 0]


# Example usage
S = int(input('initial asset price'))   # initial asset price
K = int(input('strike price')) # strike price
r = float(input('risk free interest rate'))  # risk-free interest rate
T = int(input('time to maturity')) 
N = int(input('number of time steps'))

option_price = binomial_pricing(S, K, r, T, N, option_type='call')
print(f"The option price is: {option_price}")
