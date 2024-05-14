# Interactive-Plots-eQTL-Comparison

The objective of this Python module is to generate interactive plots using Plotly Dash, facilitating visual exploration and comparison of eQTL effect sizes across different immune lineages and experimental conditions. This tool aims to help gain insights into the concordance between genetic control of immune response variation and the impact of various experimental conditions (NS: non-stimulated, COV: stimulated with SARS-CoV-2 virus, and IAV: stimulated with influenza A virus) on eQTL effects.

## Usage
The dataset utilized in this module is sourced from Supplementary Table 5a of "**Dissecting human population variation in single-cell responses to SARS-CoV-2**" (2022) by Aquino *et al.* It contains detailed information about the identified ancestry-specific eQTLs at the immune lineage level. An example usage of the script is:

```
python app.py
```
## Output
Below are the example screenshots of the output:
<img width="1270" alt="Condition" src="https://github.com/tamarintandra/Interactive-Plots-eQTL-Comparison/assets/140521132/aa8de2bd-3156-433d-888d-79a64efb542e">

<img width="1272" alt="Cell Type" src="https://github.com/tamarintandra/Interactive-Plots-eQTL-Comparison/assets/140521132/a53ce0e3-dbb1-40e0-88a5-c747b327186a">

## Citation
[1] Aquino, Y., Bisiaux, A., Li, Z. et al. Dissecting human population variation in single-cell responses to SARS-CoV-2. *Nature* **621**, 120–128 (2023). https://doi.org/10.1038/s41586-023-06422-9
