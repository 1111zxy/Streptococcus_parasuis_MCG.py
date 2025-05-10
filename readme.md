# A Streptococcus parasuis Minimum Core Genome (MCG) Typing Program

## Description  
A bioinformatics tool for identifying the **Minimum Core Genome (MCG)** of *Streptococcus parasuis* and performing MCG typing. The program clusters input genomes based on conserved MCG group and assigns MCG types using reference clusters defined in `clusters.txt`.

---

## Requirements  
- **Python**: ≥3.5  
- **MUMmer**: ≥3.1 (for genome alignment and comparison)  
  - Install MUMmer via conda:  
    ```bash
    conda install -c bioconda mummer
    ```  

---

## Installation  
1. Clone or download the script `Streptococcus_parasuis_MCG.py`.  
2. **File Placement Requirements**:  
   - Place the dependency file `clusters.txt` (predefined MCG clusters) **in the same directory as the script**.  
   - Ensure the `data` directory (containing reference genomes and MCG group-specific SNP markers) **is in the same directory as the script**.  

---

## Directory Structure  
```bash
Your_Working_Directory/
├── Streptococcus_parasuis_MCG.py   # Main script
├── clusters.txt                    # Predefined MCG clusters
└── data/                           # Reference genomes and SNP markers
    ├── BS26.fasta                # Reference genome sequences (FASTA)
    └── snps.table                   # SNP markers for each MCG group