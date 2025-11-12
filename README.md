# Option Pricing Models in Python

This repository implements three fundamental option pricing models:

1. **Black–Scholes Model (Analytical Solution)**
2. **Monte Carlo Simulation (European Options)**
3. **Binomial Tree Model (European and American Options)**

All models price options under the same risk–neutral framework.

---

## 1. Black–Scholes Model

### 1.1 Model Overview

The Black–Scholes model provides a **closed-form analytical solution** for pricing **European call and put options**. It assumes that the underlying stock follows a **geometric Brownian motion** under the risk-neutral measure **Q**.

### 1.2 Stock Price Dynamics

The price of the underlying asset **S(t)** evolves according to the stochastic differential equation:

$$dS_t = r S_{t} dt + \sigma S_{t} dW_{t}$$

where:
- $r$ is the continuously compounded risk-free interest rate
- $\sigma$ is the volatility of the stock
- $W_t$ is a Wiener process (Brownian motion)

### 1.3 Derivation Summary

Under the risk-neutral measure, the option value **V(S, t)** satisfies the **Black–Scholes partial differential equation**:

$$\frac{\partial V}{\partial t} + \frac{1}{2} {\sigma}^2 \frac{{\partial}^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0$$

with terminal condition:

$$V(S,T) = max(S-K,0)$$ for calls

$$V(S,T) = max(K-S,0)$$ for puts

Solving this PDE gives the analytical pricing formulas.

### 1.4 Black-Scholes Pricing Formulas

For a **European Call**:

$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

For a **European Put**:

$$P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$

where:

$$d_1 = \frac{ln(\frac{S_0}{K}) + (r + \frac{1}{2} {\sigma}^2) T}{\sigma \sqrt{T}}$$

$$d_2 = d_1 - \sigma \sqrt{T}$$

## 2. Monte Carlo Simulation (European Options)

### 2.1 Model Overview

The Monte Carlo simulation method estimates the expected discounted payoff of an option by simulating a large number of possible future price paths for the underlying asset.

### 2.2 Stock Price Dynamics

Under the risk-neutral measure, the terminal stock price S(T) is simulated using:

$$S_T = S_0 e^{(r-\frac{1}{2} {\sigma}^2)T + \sigma \sqrt{T} Z}$$

where:
- $Z$ is a standard normal random variable $Z \sim N(0,1)$

### 2.3 Option Value Estimation

The option price is obtained as the discounted expectation of the payoff:

$$V_0 = e^{-rT} \mathbb{E}_Q \[\text{payoff} (S_T)\]$$

For a call: 

$$\text{payoff} = max(S_T-K,0)$$

For a put:

$$\text{payoff} = max(K-S_T,0)$$

### 2.4 Variance Reduction Techniques

To improve convergence, the following techniques are included:

1. **Antithetic Variates** – Use pairs of random variables (Z, -Z) to reduce sampling variance.
2. **Control Variates** – Use the known expectation of S(T), i.e., E[S_T] = S0 * exp(rT), to reduce noise in the simulated payoff.

### 2.5 Convergence Property

The Monte Carlo estimate converges to the true price as the number of simulations increases:

$$\text{standard error} \propto \frac{1}{\sqrt{N}}$$

## 3. Binomial Tree Model

### 3.1 Model Overview

The binomial tree model represents the evolution of the stock price using a discrete-time lattice.

It can handle both European and American options, making it more flexible than the Black–Scholes or Monte Carlo models.

### 3.2 Stock Price Evolution

Over each time step of length $\Delta t = \frac{T}{N}$:

$$u = e^{\sigma \sqrt{\Delta t}}$$ (up factor)

$$d = \frac{1}{u}$$ (down factor)

$$p = \frac{e^{r \Delta t} - d}{u - d}$$ (risk-neutral probability)

The stock price at node(i,j) is:

$$S_{ij} = S_0 u^j d^{i-j}$$

### 3.3 Payoff and Backward Induction

At maturity (i=N):

$$V_{Nj} = max(S_{Nj}-K,0)$$ (for calls)

$$V_{Nj} = max(K-S_{Nj},0)$$ (for puts)

Then move backward through the tree:

$$V_{ij} = e^{-r \Delta t} \[ p V_{i+1,j+1} + (1-p) V_{i+1,j} \]$$

For American options, early exercise is allowed:

$$V_{i,j} = max(\text{immediate payoff}, \text{continuation value})$$

### 3.5 Convergence Property

As the number of time steps **N** increases, the binomial model converges to the **Black–Scholes price** for European options.
