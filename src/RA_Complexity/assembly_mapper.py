import networkx as nx
from rdkit import Chem
from rdkit.Chem import Draw
import numpy as np

class AssemblyMapper:
    def __init__(self, smiles: str, name: str):
        self.smiles = smiles
        self.name = name
        self.mol = Chem.MolFromSmiles(smiles)
        self.graph = self._build_graph()
        
    def _build_graph(self) -> nx.Graph:
        """Converts the RDKit molecule into a strictly topological NetworkX graph."""
        if self.mol is None:
            raise ValueError(f"Invalid SMILES string: {self.smiles}")
            
        G = nx.Graph()
        # Add vertices (Atoms)
        for atom in self.mol.GetAtoms():
            G.add_node(atom.GetIdx(), 
                       element=atom.GetSymbol(), 
                       mass=atom.GetMass())
            
        # Add edges (Bonds)
        for bond in self.mol.GetBonds():
            G.add_edge(bond.GetBeginAtomIdx(), 
                       bond.GetEndAtomIdx(), 
                       bond_type=str(bond.GetBondType()))
        return G

    def analyze_topology(self):
        """Extracts the basic topological metrics for Assembly Theory mapping."""
        num_atoms = self.graph.number_of_nodes()
        num_bonds = self.graph.number_of_edges()
        elements = [data['element'] for _, data in self.graph.nodes(data=True)]
        unique_elements = set(elements)
        
        print(f"--- Topological Analysis: {self.name} ---")
        print(f"SMILES: {self.smiles}")
        print(f"Vertices (Atoms): {num_atoms}")
        print(f"Edges (Bonds): {num_bonds}")
        print(f"Base Alphabet (Unique Elements): {unique_elements}")
        
        # In standard Assembly Theory, the absolute maximum A(M) is (N - 1)
        # where N is the number of bonds. The actual A(M) will be lower 
        # due to duplicate substructures (like the two methyl groups).
        max_assembly_index = num_bonds - 1 if num_bonds > 0 else 0
        print(f"Maximum possible Assembly Index A(M): {max_assembly_index}")
        print("-" * 40)

if __name__ == "__main__":
    # Target: Dimethyl Phosphate (Model for the Phosphodiester bond)
    target_smiles = "COP(=O)(O)OC"
    
    mapper = AssemblyMapper(target_smiles, "Dimethyl Phosphate")
    mapper.analyze_topology()
    
    # Optional: Generate a visual diagnostic of the molecule
    # Draw.MolToFile(mapper.mol, "dimethyl_phosphate.png")