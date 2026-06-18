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
# The sklearn has functionality for fitting linear regressions. However, the summary of cofficients, standard errors, and statistical tests is limited.  As such, there is no equivalent to the summary() function in R. Parameter values have to be extracted manually. One explanation for this is that this package is more focused on machine learning and thus using the model for prediction. However, model building requires some inspection of the model itself before using it for prediction. Hence, for the main model fitting, we concentrate on statsmodel package which provides a more classical statistical approach when summarising model parameters. 
# =============================================================================

### Study 1: Mole, C., Pekkanen, J., Sheppard, W., Louw, T., Romano, R., Merat, N., ... & Wilkie, R. (2020). Predicting takeover response to silent automated vehicle failures. PLoS One, 15(11), e0242825.

## Loading data
file_path_mole = here() / "data" / "data_RTs_cens_NA_removed.csv"

data_RTs_cens_NA_removed = pd.read_csv(file_path_mole)
# =============================================================================
# Equation 1 and 2 - Section 2.2 - Ordinary linear regression - sklearn variant
# As mentioned above - this model fit is quite an involved process. Which is why statsmodel is used for all remaining models. 
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
# Equation 1 and 2 - Section 2.2 - Ordinary linear regression - statsmodel variant
# =============================================================================

# this line of code adds an intercept into the regression model. Without it, the model only has a slope parameter
x = sm.add_constant(x)  

# fit the model and print the results
model_sm = sm.OLS(y, x)
results = model_sm.fit()
print(results.summary())

# =============================================================================
# Equation 3 - Section 2.3 - Varying intercept-fixed slope model - statsmodel variant

# The statsmodel package implementation of linear multilevel models closely follows the implementation used in the lme4 package (outlined in Lindstrom & Bates, JASA, 1988). Hence the results should be identical. The model below has varying intercepts specificed for each member of the ppid group (i.e., an intercept for each participant).

# In the statsmodel package, the random effect for each participant is highlighted in the main table and is titled "Group Var". This refers to the estimated variance (sigma sqaured) of the participant specific randon intercepts. 
# =============================================================================

mod_2 = smf.mixedlm("TLC_takeover ~ TLC_failure", data_RTs_cens_NA_removed, groups = data_RTs_cens_NA_removed["ppid"])
results_mod_2 = mod_2.fit()
print(results_mod_2.summary())

# =============================================================================
# Equation 4 - Section 2.4 - Varying intercept-varying slope model - statsmodel variant

# To add a varying slope with respect to the included predictor, specify a variable using the re_formula argument. The variance parameter for the varying intercept is titled "Group Var", the variance parameter for the varying slope is titled "TLC_failure Var", and the covariance parameter highlighting the correlation between the two must be calculated from these values and the "Group x TLC_failure Cov" values: (-0.005 / sqrt(0.007 * 0.005)) ~ -.83. This is obviously more involved than using lme4 in R. 

# =============================================================================

mod_3 = smf.mixedlm("TLC_takeover ~ TLC_failure", data_RTs_cens_NA_removed, groups = data_RTs_cens_NA_removed["ppid"], re_formula = "~TLC_failure")
results_mod_3 = mod_3.fit()
print(results_mod_3.summary())

### Study 2: Goodridge, C. M., Goncalves, R. C., Arabian, A., Horrobin, A., Solernou, A., Lee, Y. T., ... & Merat, N. (2024). Gaze entropy metrics for mental workload estimation are heterogenous during hands-off level 2 automation. Accident Analysis & Prevention, 202, 107560.

## Loading data
file_path_goodridge = here() / "data" / "goodridge_2024_dat.csv"

goodridge_2024_dat = pd.read_csv(file_path_goodridge)

# python doesn't like dot notation in variable names so here we change the same of the e.norm  to e_norm
goodridge_2024_dat = goodridge_2024_dat.rename(columns = {"e.norm": "e_norm"})

# =============================================================================
# Equation 5 - Section 3.2 - MLMs with dummy coded variables - statsmodel variant
# =============================================================================

mod_4 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back")
results_mod_4 = mod_4.fit()
print(results_mod_4.summary())

# =============================================================================
# Equation 7 - Section 3.5 - Maximal models and singular random effects - statsmodel variant
# =============================================================================

mod_5 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back * lead").fit(reml=False)
print(mod_5.summary())


# =============================================================================
# Section 3.5 - LRT for lead vehicle and interaction random effects - statsmodel variant

# In *mod_5_1* we remove the the random effect for the interaction. We get a warning when fitting this model; that we have a boundary (singular) fit. The summary of the model indicates that this is from the correlation between the intercept and lead vehicle random effects. This singular random effect may be a consequence of the lack of variance associated with the effect of lead vehicle. 

# Firstly, we compare the original model (*mod_5*) against the model with the random interaction effect removed (*mod_5_1*). The LRT reveals a non-significant effect indicating that the addition of the random interaction effect does not significantly improve the model fit. 

# In *mod_5_2* we remove the lead vehicle random effect - we then compare this against the original model. Once again, we find a non-significant effect indicating the lead vehicle random effect was not improving the model fit. 

# Just for illustration, in *mod_5_3* we remove the N-back random effect. We established in Section 3.4 for that the effect of N-back on gaze behaviour was highly variable. As such, we might expect that including the N-back random effect should improve the model fit relative to *mod_5_2* - the significant LRT tests demonstrates this. 

# =============================================================================


## TO DO

# explain that for the statsmodel package there is no direct anova(mod_5, mod_5_1) equivalent function. So you have to computer the LRT manually. This gives the same result, but is more involved. 

# continue this example for the other two mod_5 comparisons. 

mod_5_1 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back + lead").fit(reml=False)
print(mod_5_1.summary())

lr_stat = 2 * (mod_5.llf - mod_5_1.llf)

df_diff = mod_5.df_modelwc - mod_5_1.df_modelwc

p_value = chi2.sf(lr_stat, df_diff)

print(f"LR = {lr_stat:.3f}")
print(f"df = {df_diff}")
print(f"p = {p_value:.5f}")
