# Multilevel model applications

**Disclaimer**: *This is a working repository and so information and code may change*

## Overview: Multilevel models
Multilevel models are extensions of normal linear regression. They allow a scientist to model the inherent variability between related clusters in a wider population. As an example, lets assume there is a variable X that we believe to be related to a variable Y:

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/989cbf64-c526-4663-a789-476fb217cb3b)

Traditionally, one might fit a regression model to estimate the extent to which X predicts Y:

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/463a76d4-5cfc-489f-8a11-8796b82b1c42)

However, it's a complicated world. Not every*one* - or every*thing* is the same. There are groups within the whole that might differ in interesting ways. Perhaps for some of those groups, X predicts Y very strongly; for others, less so. When those groups are highlighted in different colours, the traditional regression model starts to look slightly inadequate to explain how X is related to Y. For example, X might predict a large change in Y for the blue group versus the pink group:

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/caa210d6-33c7-445e-bf2a-219b02fd74db)

Multilevel models are one way of analysing data like these. A regression line can be estimated for each group and with that, the variance of the effect across the population from which the gorups belong can be estimated. 

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/c38cb850-7ce5-450e-aacc-b68369273010)

I have given numerous talks and presentations about this analysis method. I believe it to be the present and future of statistical modelling, and concur with [Richard McElreath](https://xcelab.net/rm/statistical-rethinking/) when he says that it should be the default tool (and researchers should provide strong reasoning why they are choosing to use a different method). Despite my personal efforts in promoting multilevel models, their uptake is slow in my current research area (Human Factors). This is in spite of the vast improvements in computational power that allow Frequentist and Bayesian versions of these models to be fitted with relative computational ease. 

One reason for the lack of uptake in Human Factors is a lack of any formal tutorials. Whilst tutorials exist, they are largely in areas of Ecology, Linguistics, or Edcuation research. This is not surprising, considering that the quantitative data produced in these research areas is naturally hierarchical (e.g., Education: pupils within classes, classes within schools, schools within counties, and so on). These tutorials are fine in and of themselves, and can undoubtedly help people under the models. However, from my own experience, the hurdle is lessened if their is a tutorial that focuses specifically on the data you are working with. In this sense, I am providing the tutorial that I wanted when I first started working on these models back in 2019.   

## Code and analysis
This repository contains the analysis code in three languages - R, Python, and MATLAB - all reproducing the same set of multilevel models described in the manuscript. Having used all three, I'd recommend R, since it was purpose-built for statistical modelling. Start by cloning the repository so the relative file paths (set up via project-root packages) resolve correctly; the two data files used by the models (`data_RTs_cens_NA_removed.csv` and `goodridge_2024_dat.csv`) are already included in the data/ folder, so no extra download is needed to run the core model-fitting scripts.

R: Open `multilevel_model_HF_applications.Rproj` in RStudio - this sets the working directory automatically. The main analysis lives in `scripts/model_fits_R.Rmd`; open it and run the chunks in order (or knit the whole file). It uses the here package for file paths and depends on `ggplot2`, `dplyr`, `tidyr`, `viridis`, `lme4`, `data.table`, `emmeans`, `patchwork`, `marginaleffects`, `purrr`, `scales`, and `afex` — each is auto-installed via `if(!require(...)) install.packages(...)` at the top of the script if missing. Related scripts (`data_preprocessing.Rmd`, `manuscript_plots.Rmd`, `readme_plots_script.Rmd`) regenerate the source data and figures if you want to reproduce those steps too.

Python: Run `scripts/model_fits_python.py` from the repository root (or open it in an IDE - e.g., Spyder - with the root as the working directory) after installing `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `scipy`, and `pyprojroot`. It uses `pyprojroot.here()` to locate `data/data_RTs_cens_NA_removed.csv` relative to the project root, so the script must be run from within the cloned repo structure rather than a copied-out standalone file.

MATLAB: Open `model_fits_for_matlab.prj` to load the MATLAB project (this sets the correct paths automatically), then open and run `scripts/model_fits_matlab.mlx`, a MATLAB Live Script containing the equivalent model fits, section by section.

Each script mirrors the same sequence of models (from the basic linear regression through to the full multilevel specifications), cross-referenced to the equation and section numbers in the manuscript, so you can follow along in whichever language you're most comfortable with.




