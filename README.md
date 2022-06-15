# Mali
Mali: A malware classification tool (beta version).

## Goal
The goal of this project is to build a foundation for a malware classifier using machine learning that can classify and separate PE executables into different malware families (e.g. worm, trojan, backdoor, ransomware, etc.) with high accuracy and efficiency. This foundation will then be used to create a closed-source malware classification tool that can be utilized by security researchers.

## Dataset
The BODMAS Malware dataset was used to train the classification model. It contains 57,293 malware samples and 77,142 benign samples collected from August 2019 to September 2020, with carefully curated family information (581 families). You can download the dataset [here](https://drive.google.com/drive/folders/1Uf-LebLWyi9eCv97iBal7kL1NgiGEsv_). The dataset contains:
- feature vectors (~250 MB): `bodmas.npz`
- metadata (~12 MB): `bodmas_metadata.csv` 

They are sorted by the timestamp in ascending order (i.e., each feature vector corresponds to one row in the metadata file). `bodmas_metadata.csv` has three columns, indicating SHA-256, when the sample first appeared, and malware family. If the malware family is empty, then it’s a benign sample.

To load the feature vectors, you need to load `bodmas.npz` (a numpy compressed format) with the following code. Note that the feature values are unnormalized, which is fine for classifiers like gradient-boosted decision tree, but you may need to normalize them first when applying an MLP classifier.

``` python
import numpy as np 
filename = 'bodmas.npz' 
data = np.load(filename) 
X = data['X']  # all the feature vectors 
y = data['y']  # labels, 0 as benign, 1 as malicious 
print(X.shape, y.shape) # >>> (134435, 2381), (134435,) 
```
To learn more about the BODMAS dataset, you can visit this [link](https://whyisyoung.github.io/BODMAS/).

## Feature Engineering
The LIEF library was used to extract features from PE files. Raw features are extracted into JSON format and vectorized features are produced from these raw features and saved in binary format, from which they are converted into CSV or dataframes. The feature calculation is versioned:
- Feature version 1 is calculated with the LIEF library version 0.8.3.
- Feature version 2 includes the additional data directory feature, updated ordinal import processing, and is calculated with LIEF library version 0.9.0.

Each sample is represented as a 2381 feature vector, along with its label (benign or malicious) and malware family if it’s malicious.

## Model
The following machine learning models were evaluated:
- CatBoost boosted trees
- Extra-trees (using Shannon entropy as the node splitting criterion)
- Extra-trees (using Gini impurity as the node splitting criterion)
- Random forest (using Shannon entropy as the node splitting criterion)
- Random forest (using Gini impurity as the node splitting criterion)
- Tabular deep neural network

A weighted ensemble model, which combines predictions from extra-trees, random forest, CatBoost, and deep neural network classifiers, had the highest classification accuracy and, thus, is used as the final model.

## Results
|   |               model | score_test | score_val | pred_time_test | pred_time_val |    fit_time | pred_time_test_marginal | pred_time_val_marginal | fit_time_marginal | stack_level | can_infer | fit_order |
|--:|--------------------:|-----------:|----------:|---------------:|--------------:|------------:|------------------------:|-----------------------:|------------------:|------------:|----------:|----------:|
| 0 | WeightedEnsemble_L2 |   0.995965 |    0.9976 |      21.930001 |      2.681004 | 1418.062613 |                0.028000 |               0.007999 |          0.943001 |           2 |      True |         6 |
| 1 |      NeuralNetTorch |   0.995740 |    0.9968 |      19.396000 |      2.440000 | 1161.801305 |               19.396000 |               2.440000 |       1161.801305 |           1 |      True |         5 |
| 2 |      ExtraTreesGini |   0.994861 |    0.9964 |       2.289998 |      0.309004 |   89.408530 |                2.289998 |               0.309004 |         89.408530 |           1 |      True |         3 |
| 3 |      ExtraTreesEntr |   0.994838 |    0.9960 |       2.031004 |      0.222998 |   69.117058 |                2.031004 |               0.222998 |         69.117058 |           1 |      True |         4 |
| 4 |    RandomForestEntr |   0.994320 |    0.9944 |       1.919002 |      0.361995 |  188.971065 |                1.919002 |               0.361995 |        188.971065 |           1 |      True |         2 |
| 5 |    RandomForestGini |   0.994297 |    0.9952 |       2.506001 |      0.233005 |  255.318307 |                2.506001 |               0.233005 |        255.318307 |           1 |      True |         1 |
