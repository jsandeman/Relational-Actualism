import numpy as np
from numba import njit, prange
import time

# BDG/Yeats Chord Multiplicities
# c_0 = 1, c_1 = 1, c_2 = 9, c_3 = 16, c_4 = 8
C_K = np.array([1, 1, 9, 16, 8], dtype=np.float64)

@njit
def generate_alexandrov_points(n):
    """
    Sprinkles n points uniformly in a 4D Minkowski Alexandrov interval.
    Uses rejection sampling in a bounding box for simplicity given small n.
    """
    points = np.zeros((n, 4))
    count = 0
    while count < n:
        # Sample uniformly in a bounding box [-1, 1]^4
        pt = np.random.uniform(-1.0, 1.0, 4)
        
        # Check if point is in the Alexandrov interval between 
        # past tip (-1, 0,0,0) and future tip (1, 0,0,0)
        dt_past = pt[0] - (-1.0)
        ds2_past = dt_past**2 - (pt[1]**2 + pt[2]**2 + pt[3]**2)
        
        dt_future = 1.0 - pt[0]
        ds2_future = dt_future**2 - (pt[1]**2 + pt[2]**2 + pt[3]**2)
        
        if dt_past > 0 and ds2_past > 0 and dt_future > 0 and ds2_future > 0:
            points[count] = pt
            count += 1
    return points

@njit
def get_causal_matrix(points, n):
    """Generates the adjacency matrix for causal relations."""
    C = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dt = points[j, 0] - points[i, 0]
            if dt > 0:
                ds2 = dt**2 - np.sum((points[j, 1:] - points[i, 1:])**2)
                if ds2 > 0:
                    C[i, j] = 1
    return C

@njit(parallel=True)
def run_mcmc_simulation(iterations, mu=1.0):
    """
    Runs the Monte Carlo simulation to extract expected N_k counts.
    """
    nk_totals = np.zeros(5, dtype=np.float64)
    
    for _ in prange(iterations):
        # 1. Sample N from Poisson distribution
        n = np.random.poisson(mu)
        
        if n == 0:
            nk_totals[0] += 0 # No vertices
            continue
            
        nk_totals[0] += n # N_0 is the number of vertices
        
        if n < 2:
            continue
            
        # 2. Sprinkle points and get causal relations
        points = generate_alexandrov_points(n)
        C = get_causal_matrix(points, n)
        
        # 3. Count intervals
        for i in range(n):
            for j in range(n):
                if C[i, j] == 1:
                    # Count points k such that i ≺ k ≺ j
                    k_count = 0
                    for k in range(n):
                        if C[i, k] == 1 and C[k, j] == 1:
                            k_count += 1
                    
                    if k_count == 0:
                        nk_totals[1] += 1 # 1-element interval (direct edge)
                    elif k_count == 1:
                        nk_totals[2] += 1
                    elif k_count == 2:
                        nk_totals[3] += 1
                    elif k_count == 3:
                        nk_totals[4] += 1

    # Average over iterations
    nk_expected = nk_totals / iterations
    return nk_expected

if __name__ == "__main__":
    iterations = 100_000_000 # 10^8 samples
    mu_critical = 1.0
    
    print(f"Starting simulation with {iterations} iterations at μ = {mu_critical}...")
    start_time = time.time()
    
    # Run simulation
    N_k_expected = run_mcmc_simulation(iterations, mu_critical)
    
    end_time = time.time()
    print(f"Simulation completed in {end_time - start_time:.2f} seconds.\n")
    
    print("--- Results ---")
    print(f"Expected N_k counts at μ=1:")
    for k in range(5):
        print(f"  <N_{k}> = {N_k_expected[k]:.6f}")
        
    print("\n--- Yeats / BDG Mapping ---")
    W_values = C_K * N_k_expected
    
    for k in range(5):
        print(f"  D_{k} = |c_{k}| * <N_{k}> = {C_K[k]:.0f} * {N_k_expected[k]:.6f} = {W_values[k]:.6f}")
        
    print("\nIs <D_k> converging to a constant W?")
    mean_W = np.mean(W_values)
    print(f"Mean W: {mean_W:.6f}")
    print(f"Standard Deviation of W: {np.std(W_values):.6f}")