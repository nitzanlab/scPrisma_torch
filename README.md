# scPrisma_torch
scPrisma is a spectral analysis method, for pseudotime reconstruction, informative genes inference, filtering, and enhancement of underlying cyclic signals
<h2> For reproducibility of scPrisma manuscript, please refer to:<br /> https://github.com/nitzanlab/scPrisma_notebooks</h2>
<h1> This repository contains boosted version of scPrisma, which support calculations using GPU</h1>
<br />

![workflow](https://github.com/nitzanlab/scPrisma/blob/main/workflow.png?raw=true)
<br />
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Reconstruction](#reconstruction)
  * [Filtering workflow](#filtering-workflow)
  * [Enhancement workflow](#enhancement-workflow)
* [Tutorials](#tutorials)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project
[Manuscript](https://www.biorxiv.org/content/10.1101/2022.06.07.493867v1) <br />
[Notebooks](https://github.com/nitzanlab/scPrisma_notebooks)
### Built With
* [Python](https://www.python.org/) - 3.7 , Numpy and Numba libraries. it is recommended to use also Scanpy library.



<!-- GETTING STARTED -->
## Getting Started

```sh
git clone https://github.com/nitzanlab/scPrisma.git
cd scPrisma
pip install .
```
##Imports
It is recommended to use ['scanpy'](https://scanpy.readthedocs.io/en/stable/index.html) package. 

```
import scPrisma.algorithms as algo
import scanpy as sc
import numpy as np
```
## Pre-processing
```
adata = sc.read(path)
sc.pp.normalize_per_cell(adata, counts_per_cell_after=1e4)
sc.pp.log1p(adata)
```
'adata' should be AnnData object, where the observations (rows) are cells and the variables (columns) are genes. 
## Reconstruction
The first step in this workflow is reconstruct the signal, this can be done using the reconstriction algorithm:

```
E , E_rec = algo.reconstruction_cyclic(adata.X)
order = algo.E_to_range(E_rec)
adata = adata[order,:]
```
'reconstruction_cyclic' function receives as an input the gene expression matrix (and parameters that can be seen in 'algorithms.py') and returns 'E' which is a doubly stochastic matrix and 'E_rec' which is the desired permutation matrix.
'E_to_range' turns the permutation matrix into a permutation array.

If low-resolution pseudotime ordering exists (as prior knowledge) it can be used instead of applying the reconstruction algorithm:
```
adata = algo.sort_data_crit(adata=adata ,crit=crit,crit_list=crit_list)
```

Each cell should have a label of his place stored as 'obs'. 'crit' is the desired label,  'crit_list' is the desired order.
For example: for sorting a gene expression that was sampled at four different timepoints (0,6,12,18). The sampling time can be stored as 'ZT' (adata.obs['ZT'] = X). and applied the following function:
```
adata = algo.sort_data_crit(adata=adata ,crit='ZT',crit_list=['0','6','12','18'])
```
The best performance would be achieved if there were similar numbers of samples in each state. Subsampling states with more cells than others can solve this issue. 



## Filtering workflow
After reconstruction was applied, we can use the filtering algorithm. This algorithm filters out the expression profiles that are related to the reconstructed topology.
```
F = algo.filtering_cyclic(adata.X, regu=0 )
adata.X = adata.X * F
```
'regu' is the regularization parameter, it is recomended that this parameter would be between 0 and 0.5. As long as we increase this parameter <b><u>less</u></b> information would be filter out. Since it is a convex optimization problem, it is solved using backtracking line search gradient descent.
## Enhancement workflow
After reconstruction was applied, we can use the enhancement algorithm. This algorithm filters out the expression profiles that <b><u>are not</u></b> related to the reconstructed topology.
It is recomended to use the informative genes infereence algorithm before using the enhancement algorithm. Running the genes inference algorithm, prevents overfitting of genes that are not related to desired topology.
```
D = algo.filter_cyclic_genes_line(adata.X, regu=0)
D = np.identify(D.shape[0)-D
adata.X = (adata.X).dot(D)
```
'regu' is the regularization parameter, it is recomended that this parameter would be between -0.1 and 0.5. As long as we increase this parameter the algorithm would filter out <b><u>less</u></b> genes. But, we will retain the genes that the algorithm would not filter, so as long as we increase this parameter,<b><u>more</u></b> genes will be filtered out.
Next we can apply the enhancement algorithm:

```
F = algo.enhancement_cyclic(adata.X, regu=0 )
adata.X = adata.X * F
```

As long as we increase the regularization parameter we will filter out <b><u>more</u></b> information.


<!-- TUTORIALS -->
## Tutorials
[De-novo reonstruction, cyclic enhancement and filtering- HeLa S3 cells](https://github.com/nitzanlab/scPrisma/blob/main/tutorials/tutorial_de_novo_reconstruction.ipynb)
<br />
[Reonstruction from prior knowledge, cyclic enhancement and filtering, linear enhancment and filtering- Mouse liver lobules](https://github.com/nitzanlab/scPrisma/blob/main/tutorials/tutorial_prior_knowledge_linear_and_cyclic.ipynb)

<!-- CONTACT -->
## Contact
Jonathan Karin - jonathan.karin [at ] mail.huji.ac.il
