# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:43:45 2024

@author: psccgoo
"""

# load necessary packages
import pandas as pd
import numpy as np 
import os
from pyprojroot.here import here
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report
import statsmodels.api as sm
import statsmodels.formula.api as smf

# =============================================================================
# The sklearn has functionality for fitting linear regressions. However, the summary of cofficients, standard errors, and statistical tests is limited.  As such, there is no equivalent to the summary() function in R. Parameter values have to be extracted manually. On explanation for this is that this package is more focused on machine learning and thus using the model for prediction. However, model building requires some inspectin of the model itself before using it for prediction. Hence, for the main model fitting, we concentrate on statsmodel package which provides a more classical statistical approach when summarising model parameters. 
# =============================================================================

# Loading Mole et al (2020) data
data_RTs_cens_NA_removed = pd.read_csv(here('OneDrive - University of Leeds\\ITS\\Multilevel models paper\\Mole et al (2020) data and analysis\\data_RTs_cens_NA_removed.csv'))

# =============================================================================
# Model 1: Ordinary linear regression - sklearn variant
# =============================================================================

# Prepare data for model fitting
y = data_RTs_cens_NA_removed[['TLC_takeover']]
x = data_RTs_cens_NA_removed[['TLC_failure']]

# initialise model
model = LinearRegression()

# fit the model
model.fit(x, y)

# Parameter values from regression model
print(f"intercept: {model.intercept_}")

print(f"coefficients: {model.coef_}")


# =============================================================================
# Model 1: Ordinary linear regression - statsmodel variant
# =============================================================================

# this line of code adds an intercept into the regression model. Without it, the model only has a slope parameter
x = sm.add_constant(x)  

# fit the model and print the results
model_sm = sm.OLS(y, x)
results = model_sm.fit()
print(results.summary())

# =============================================================================
# Model 2: varying intercept multilevel model - statsmodel variant

# The statsmodel package implementation of linear multilevel models closely follows the implementation used in the lme4 package (outlined in Lindstrom & Bates, JASA, 1988). Hence the results should be identical. The model below has varying intercepts specificed for each member of the ppid group (i.e., an intercept for each participant).

# In the statsmodel package, the random effect for each participant is highlighted in the main table and is titled "Group Var". This refers to the estimated variance (sigma sqaured) of the participant specific randon intercepts. 
# =============================================================================

mod_2 = smf.mixedlm("TLC_takeover ~ TLC_failure", data_RTs_cens_NA_removed, groups = data_RTs_cens_NA_removed["ppid"])
results_mod_2 = mod_2.fit()
print(results_mod_2.summary())

# =============================================================================
# Model 3: varying intercept, varying slope model - statsmodel variant

# To add a varying slope with respect to the included predictor, specify a variable using the re_formula argument. The variance parameter for the varying intercept is titled "Group Var", the variance parameter for the varying slope is titled "TLC_failure Var", and the covariance parameter highlighting the correlation between the two must be calculated from these values and the "Group x TLC_failure Cov" values: (-0.005 / sqrt(0.007 * 0.005)) ~ -.83

# =============================================================================

mod_3 = smf.mixedlm("TLC_takeover ~ TLC_failure", data_RTs_cens_NA_removed, groups = data_RTs_cens_NA_removed["ppid"], re_formula = "~TLC_failure")
results_mod_3 = mod_3.fit()
print(results_mod_3.summary())

# =============================================================================
# Model 4: varying intercept, varying slope model (with Goodridge et al, 2024 data) - statsmodel variant
# =============================================================================

# Loading Goodridge et al (2024) data
goodridge_2024_dat = pd.read_csv(here('OneDrive - University of Leeds\\ITS\\Multilevel models paper\\Mole et al (2020) data and analysis\\goodridge_2024_dat.csv'))

# python doesn't like dot notation in variable names so here we change the same of the e.norm  to e_norm
goodridge_2024_dat = goodridge_2024_dat.rename(columns = {"e.norm": "e_norm"})

mod_4 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back")
results_mod_4 = mod_4.fit()
print(results_mod_4.summary())

# =============================================================================
# Model 5: maximal model with the Goodridge et al (2024) data - statsmodel variant
# =============================================================================

mod_5 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back * lead")
results_mod_5 = mod_5.fit()
print(results_mod_5.summary())


# =============================================================================
# Model 6: model without correlaton parameters using Goodridge et al (2024) data - statsmodel variant

# TO DO - find out what np.ones and np.eye actually mean. This page (https://github.com/statsmodels/statsmodels/issues/1946) suggests that ones means number of fixed effects, whilst eye means number of random effects? Not sure though. 
# =============================================================================

mod_6 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back * lead")
free = sm.regression.mixed_linear_model.MixedLMParams.from_components(np.ones(4), np.eye(4))
results_mod_6 = mod_6.fit(free = free)
print(results_mod_6.summary())
