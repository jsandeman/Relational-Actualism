import numpy as np
from collections import Counter

def generate_causal_diamond(N):
    """Sprinkle N points uniformly into a unit 4D causal diamond."""
    points = []
    while len(points) < N:
        # Generate in the bounding box: t in [0,1], x,y,z in [-0.5, 0.5]
        pt = np.random.uniform([-0.5, -0.5, -0.5, 0.0], [0.5, 0.5, 0.5, 1.0])
        r = np.sqrt(pt[0]**2 + pt[1]**2 + pt[2]**2)
        t = pt[3]
        # Must be in future of origin and past of top vertex (0,0,0,1)
        if t > r and (1 - t) > r:
            points.append(pt)
    return np.array(points)

def build_adjacency_matrix(points):
    """Construct the strictly upper-triangular adjacency matrix based on causal order."""
    N = len(points)
    A = np.zeros((N, N), dtype=int)
    
    # Sort points by time coordinate to ensure topological ordering
    sorted_indices = np.argsort(points[:, 3])
    pts = points[sorted_indices]
    
    for i in range(N):
        dt = pts[i+1:, 3] - pts[i, 3]
        dx = pts[i+1:, 0] - pts[i, 0]
        dy = pts[i+1:, 1] - pts[i, 1]
        dz = pts[i+1:, 2] - pts[i, 2]
        
        ds2 = dt**2 - (dx**2 + dy**2 + dz**2)
        
        # Causal relation: ds2 > 0 and dt > 0
        causal_links = (ds2 > 0) & (dt > 0)
        A[i, i+1:] = causal_links.astype(int)
        
    return A

def count_bdg_chains(A):
    """
    Correctly count the number of k-element chains (simplices).
    This exactly matches the Lean 4 matrix polynomial definition.
    """
    counts = {}
    
    # N_1 in BDG (2-element chains / edges)
    # This is simply the sum of all elements in the adjacency matrix
    counts[2] = int(np.sum(A))
    
    # N_2 in BDG (3-element chains)
    # A^2 counts the number of valid paths of length 2
    A2 = A @ A
    counts[3] = int(np.sum(A2))
    
    # N_3 in BDG (4-element chains)
    A3 = A2 @ A
    counts[4] = int(np.sum(A3))
    
    # N_4 in BDG (5-element chains)
    A4 = A3 @ A
    counts[5] = int(np.sum(A4))
    
    return counts

def run_eccentricity_experiment(N=2000, lambda_stretch=1.02):
    print(f"Generating unperturbed diamond (N={N})...")
    points = generate_causal_diamond(N)
    A_vacuum = build_adjacency_matrix(points)
    counts_vacuum = count_bdg_chains(A_vacuum)  # Updated function call
    
    print(f"Applying volume-preserving stretch (lambda={lambda_stretch})...")
    points_stretched = np.copy(points)
    points_stretched[:, 3] *= lambda_stretch
    points_stretched[:, 0:3] *= (lambda_stretch ** (-1/3))
    
    A_stretched = build_adjacency_matrix(points_stretched)
    counts_stretched = count_bdg_chains(A_stretched)  # Updated function call
    
    print("\n--- RESULTS ---")
    print(f"Vacuum Counts (N_k):   {counts_vacuum}")
    print(f"Stretched Counts (N_k):{counts_stretched}")
    
    delta_N = {k: counts_stretched[k] - counts_vacuum[k] for k in range(2, 6)}
    print(f"Delta N: {delta_N}")
    
    # -1(N1) + 9(N2) - 16(N3) + 8(N4)
    bdg_action = -1*delta_N[2] + 9*delta_N[3] - 16*delta_N[4] + 8*delta_N[5]
    print(f"\nBDG Action of Perturbation: {bdg_action}")

if __name__ == "__main__":
    run_eccentricity_experiment(N=2000, lambda_stretch=1.02)

def run_eccentricity_experiment(N=1000, lambda_stretch=1.05):
    print(f"Generating unperturbed diamond (N={N})...")
    points = generate_causal_diamond(N)
    A_vacuum = build_adjacency_matrix(points)
    counts_vacuum = count_bdg_intervals(A_vacuum)
    
    print(f"Applying volume-preserving stretch (lambda={lambda_stretch})...")
    # t' = lambda * t
    # r' = lambda^(-1/3) * r
    points_stretched = np.copy(points)
    points_stretched[:, 3] *= lambda_stretch
    points_stretched[:, 0:3] *= (lambda_stretch ** (-1/3))
    
    A_stretched = build_adjacency_matrix(points_stretched)
    counts_stretched = count_bdg_intervals(A_stretched)
    
    print("\n--- RESULTS ---")
    print(f"Vacuum Counts (N_k):   {dict(counts_vacuum)}")
    print(f"Stretched Counts (N_k):{dict(counts_stretched)}")
    
    delta_N = {k: counts_stretched[k] - counts_vacuum[k] for k in range(2, 6)}
    print(f"Delta N: {delta_N}")
    
    # Check the BDG on-shell condition: -N2 + 9N3 - 16N4 + 8N5 = 0
    # (Note: standard BDG indices map N_elements to these coefficients)
    bdg_action = -1*delta_N[2] + 9*delta_N[3] - 16*delta_N[4] + 8*delta_N[5]
    print(f"\nBDG Action of Perturbation: {bdg_action}")

if __name__ == "__main__":
    run_eccentricity_experiment(N=2000, lambda_stretch=1.02)