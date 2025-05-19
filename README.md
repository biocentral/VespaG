[![License](https://shields.io/github/license/jschlensok/vespag)](https://opensource.org/license/gpl-3-0)
![Static Badge](https://img.shields.io/badge/python-3.10-blue)
[![Tests](https://github.com/JSchlensok/VespaG/actions/workflows/run_tests.yml/badge.svg)](https://github.com/JSchlensok/VespaG/actions/workflows/run_tests.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# VespaG: Expert-Guided Protein Language Models enable Accurate and Blazingly Fast Fitness Prediction

⚠️ **This is the deployment branch of the biocentral VespaG fork!** ⚠️

**VespaG** is a blazingly fast single amino acid variant effect predictor, leveraging embeddings of the protein language model [ESM-2](https://github.com/facebookresearch/esm) ([Lin et al. 2022](https://www.science.org/doi/abs/10.1126/science.ade2574)) as input to a minimal deep learning model.

To overcome the sparsity of experimental training data, we created a dataset of 39 million single amino acid variants from a subset of the Human proteome, which we then annotated using predictions from the multiple sequence alignment-based effect predictor [GEMME](http://www.lcqb.upmc.fr/GEMME/Home.html) ([Laine et al. 2019](https://doi.org/10.1093/molbev/msz179)) as a proxy for experimental scores.

Assessed on the [ProteinGym](https://proteingym.org) ([Notin et al. 2023](https://www.biorxiv.org/content/10.1101/2023.12.07.570727v1)) benchmark, **VespaG** matches state-of-the-art methods while being several orders of magnitude faster, predicting the entire single-site mutational landscape for a human proteome in under a half hour on a consumer-grade laptop.

More details on **VespaG** can be found in the corresponding [publication](https://doi.org/10.1093/bioinformatics/btae621)

### Installation
0. create virtual environment
1. `git clone https://github.com/jschlensok/vespag.git`
2. `pip install .` or `uv pip install .`

## Deployment branch

**This is a deployment branch for VespaG, 
created primarily for usage in [biocentral](https://github.com/biocentral/biocentral_server/).** 

*Kept API Files:*
- `vespag/utils/mutations.py`: Dataclasses for SAVs/Mutations
- `vespag/utils/utils.py`: ScoreNormalizer, mask mutations and compute mutation scores

### How to cite
```
@article{10.1093/bioinformatics/btae621,
    author = {Marquet, Céline and Schlensok, Julius and Abakarova, Marina and Rost, Burkhard and Laine, Elodie},
    title = {Expert-guided protein language models enable accurate and blazingly fast fitness prediction},
    journal = {Bioinformatics},
    volume = {40},
    number = {11},
    pages = {btae621},
    year = {2024},
    month = {11},
    issn = {1367-4811},
    doi = {10.1093/bioinformatics/btae621},
    url = {https://doi.org/10.1093/bioinformatics/btae621},
    eprint = {https://academic.oup.com/bioinformatics/article-pdf/40/11/btae621/60811415/btae621.pdf},
}
```
