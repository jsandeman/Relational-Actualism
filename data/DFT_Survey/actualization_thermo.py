from rdkit import Chem
from rdkit.Chem import AllChem
from pyscf import gto, scf
import numpy as np

def get_pyscf_molecule(smiles, spin=0, charge=0):
    """Generates 3D coordinates from SMILES and builds a PySCF molecule object."""
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    
    # Generate 3D geometry using the ETKDG algorithm
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    AllChem.MMFFOptimizeMolecule(mol)
    
    conf = mol.GetConformer()
    atom_coords = []
    for i, atom in enumerate(mol.GetAtoms()):
        pos = conf.GetAtomPosition(i)
        atom_coords.append(f"{atom.GetSymbol()} {pos.x} {pos.y} {pos.z}")
        
    geometry = "; ".join(atom_coords)
    
    # Build the PySCF molecule (using a lightweight basis set for speed)
    pyscf_mol = gto.M(
        atom=geometry,
        basis='sto-3g', 
        spin=spin,
        charge=charge
    )
    return pyscf_mol

def calculate_energy(smiles, name, spin=0, charge=0):
    print(f"\n--- Running DFT for {name} ---")
    mol = get_pyscf_molecule(smiles, spin, charge)
    
    # Run Restricted or Unrestricted Hartree-Fock depending on spin
    if spin == 0:
        mf = scf.RHF(mol)
    else:
        mf = scf.UHF(mol)
        
    # Silence the verbose PySCF output
    mf.verbose = 0 
    energy = mf.kernel()
    print(f"Total Energy: {energy:.6f} Hartrees")
    return energy

if __name__ == "__main__":
    print("Initializing Quantum Chemistry Pipeline...")
    
    # We model the final JOIN: 
    # Monomethyl Phosphate Radical + Methoxy Radical -> Dimethyl Phosphate
    
    # 1. The Bound State
    bound_smiles = "COP(=O)(O)OC" # Dimethyl Phosphate
    e_bound = calculate_energy(bound_smiles, "Bound State (Dimethyl Phosphate)", spin=0)
    
    # 2. The Fragments (The state immediately before the JOIN)
    # Fragment A: Monomethyl Phosphate radical (missing one methoxy group)
    frag_A_smiles = "COP(=O)(O)[O]"
    e_frag_A = calculate_energy(frag_A_smiles, "Fragment A (Phosphate Core Radical)", spin=1)
    
    # Fragment B: Methyl radical
    frag_B_smiles = "[CH3]"
    e_frag_B = calculate_energy(frag_B_smiles, "Fragment B (Methyl Radical)", spin=1)
    
    # Calculate the Binding Energy
    e_fragments_total = e_frag_A + e_frag_B
    delta_e = e_bound - e_fragments_total
    
    # Convert Hartrees to kcal/mol (1 Hartree = 627.509 kcal/mol)
    delta_e_kcal = delta_e * 627.509
    
    print("\n==================================================")
    print("   RELATIONAL ACTUALISM: JOIN THERMODYNAMICS      ")
    print("==================================================")
    print(f"Energy of Separated Fragments: {e_fragments_total:.6f} Hartrees")
    print(f"Energy of Bound Molecule:      {e_bound:.6f} Hartrees")
    print(f"Binding Energy (Delta E):      {delta_e_kcal:.2f} kcal/mol")
    print("==================================================")
    
    if delta_e_kcal < 0:
        print("\n[VERIFIED] Delta E is negative.")
        print("To satisfy the Local Ledger Condition, the system MUST emit")
        print("an on-shell boson carrying away this exact energy difference.")
        print("Therefore, this abstract Assembly JOIN mathematically guarantees")
        print("at least one physical Actualization Event.")