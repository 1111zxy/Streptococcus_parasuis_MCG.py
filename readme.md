# A *Streptococcus parasuis* Minimum Core Genome (MCG) Typing Program

## Description  
A bioinformatics tool for identifying the Minimum Core Genome (MCG) group of *Streptococcus parasuis*. The program maps the assembled genome FASTA files to the BS26 reference genome and detects MCG group/lineage-specific SNPs. The program calculates the proportion of S. parasuis genome assigned to each MCG group by dividing the number of matched sites by total specific sites. The genome is then assigned to the MCG group with the highest proportion value.

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
1. Clone or download the script `Streptococcus_parasuis_MCG_Typing.py`.  
2. **File Placement Requirements**:  
   - Place the dependency file `clusters.txt` (predefined MCG clusters) **in the same directory as the script**.  
   - Ensure the `data` directory (containing reference genomes and MCG group-specific SNP markers) **is in the same directory as the script**.  

---

## Directory Structure  
```bash
Your_Working_Directory/
├── Streptococcus_parasuis_MCG_Typing.py   # Main script
├── clusters.txt                           # Predefined MCG clusters
└── data/                                  # Reference genomes and SNP markers
    ├── BS26.fasta                         # Reference genome sequences (FASTA)
    └── snps.table                         # SNP markers for each MCG group
```

---

## Usage  
### Basic Command  
```bash
python Streptococcus_parasuis_MCG_Typing.py --genome <input.fasta> --prefix <output_prefix>
```

