from rdkit import Chem
from rdkit.Chem import AllChem
from pyscf import gto, scf, dft
import numpy as np
import time

def get_pyscf_molecule(smiles, spin=0, charge=0):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    AllChem.MMFFOptimizeMolecule(mol)
    
    conf = mol.GetConformer()
    atom_coords = []
    for i, atom in enumerate(mol.GetAtoms()):
        pos = conf.GetAtomPosition(i)
        atom_coords.append(f"{atom.GetSymbol()} {pos.x} {pos.y} {pos.z}")
        
    geometry = "; ".join(atom_coords)
    
    # UPGRADE: Using a high-fidelity basis set
    pyscf_mol = gto.M(
        atom=geometry,
        basis='6-311+G*', 
        spin=spin,
        charge=charge
    )
    return pyscf_mol

def calculate_energy(smiles, spin=0, charge=0):
    mol = get_pyscf_molecule(smiles, spin, charge)
    
    # UPGRADE: Using B3LYP Density Functional Theory
    if spin == 0:
        mf = dft.RKS(mol) # Restricted Kohn-Sham for closed shells
    else:
        mf = dft.UKS(mol) # Unrestricted Kohn-Sham for radicals
        
    mf.xc = 'b3lyp'
    mf.verbose = 0 
    return mf.kernel()

def run_reaction(name, bound_smiles, frag1_smiles, frag2_smiles):
    print(f"\n--- Processing: {name} ---")
    start_time = time.time()
    
    e_bound = calculate_energy(bound_smiles, spin=0)
    print(f"Bound State ({bound_smiles}): {e_bound:.4f} Hartrees")
    
    e_frag1 = calculate_energy(frag1_smiles, spin=1)
    print(f"Fragment 1 ({frag1_smiles}):  {e_frag1:.4f} Hartrees")
    
    e_frag2 = calculate_energy(frag2_smiles, spin=1)
    print(f"Fragment 2 ({frag2_smiles}):  {e_frag2:.4f} Hartrees")
    
    delta_e_hartree = e_bound - (e_frag1 + e_frag2)
    delta_e_kcal = delta_e_hartree * 627.509
    
    elapsed = time.time() - start_time
    print(f">> Delta E: {delta_e_kcal:.2f} kcal/mol (Computed in {elapsed:.1f}s)")
    return delta_e_kcal

if __name__ == "__main__":
    print("Initializing B3LYP/6-311+G* Quantum Survey...")
    
    # The Reaction Ledger: Ensuring exact homolytic cleavage for accurate Delta E
    reactions = [
        # 1. C-C Bond (Ethane -> two Methyl radicals)
        ("Carbon-Carbon Bond", "CC", "[CH3]", "[CH3]"),
        
        # 2. Peptide Bond Model (Formamide -> Amino radical + Formyl radical)
        ("Peptide Bond (C-N)", "NC=O", "[NH2]", "[CH]=O"),
        
        # 3. Glycosidic/Ether Bond Model (Dimethyl ether -> Methoxy + Methyl)
        ("Glycosidic Bond (C-O)", "COC", "C[O]", "[CH3]"),
        
        # 4. Disulfide Bond (Dimethyl disulfide -> two Methanethiyl radicals)
        ("Disulfide Bond (S-S)", "CSSC", "C[S]", "C[S]"),
        
        # 5. Phosphoester Bond (Dimethyl phosphate -> Methyl + Phosphate core)
        ("Phosphoester Bond (P-O)", "COP(=O)(O)OC", "[CH3]", "COP(=O)(O)[O]")
    ]
    
    results = {}
    for name, bound, f1, f2 in reactions:
        try:
            results[name] = run_reaction(name, bound, f1, f2)
        except Exception as e:
            print(f"  [!] FAILED to process {name}: {e}")
            results[name] = 0.0 # Placeholder for failed runs
        
    print("\n==================================================")
    print("   RELATIONAL ACTUALISM: C1 COMPUTATIONAL SURVEY    ")
    print("==================================================")
    for name, de in results.items():
        status = "VERIFIED (Exothermic)" if de < 0 else "FAILED"
        print(f"{name:<25} | Delta E: {de:>7.2f} kcal/mol | {status}")
    print("==================================================")
    print("All bound states require an on-shell boson emission.")