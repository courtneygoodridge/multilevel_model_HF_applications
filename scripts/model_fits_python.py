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
from scipy.stats import chi2
from statsmodels.stats.anova import AnovaRM

# =============================================================================
# Model fits accompanying the Multilevel Models: A Tutorial on Applications and Uses in Human Factors Research

# This .py file is the R version of the analysis script that accompanies the manuscript Multilevel Models: A Tutorial on Applications and Uses in Human Factors Research. Within this file, you will find each of the models fitted in manuscript. Each model can be linked to the corresponding place in the manuscript with an equation number that highlights the model and section number that it is associated with. This script also contains some extra detail that was superfluous for the main manuscript, but is nonetheless important for understanding MLMs. 
# =============================================================================

# =============================================================================
# The sklearn has functionality for fitting linear regressions. However, the summary of cofficients, standard errors, and statistical tests is limited.  As such, there is no equivalent to the summary() function in R. Parameter values have to be extracted manually. One explanation for this is that this package is more focused on machine learning and thus using the model for prediction. However, model building requires some inspection of the model itself before using it for prediction. Hence, for the main model fitting, we concentrate on statsmodel package which provides a more classical statistical approach when summarising model parameters. 
# =============================================================================

### Study 1: Mole, C., Pekkanen, J., Sheppard, W., Louw, T., Romano, R., Merat, N., ... & Wilkie, R. (2020). Predicting takeover response to silent automated vehicle failures. PLoS One, 15(11), e0242825.

## Loading data
file_path_mole = here() / "data" / "data_RTs_cens_NA_removed.csv"

data_RTs_cens_NA_removed = pd.read_csv(file_path_mole)

# sklearn variant. As mentioned above - this model fit is quite an involved process. Which is why statsmodel is used for all remaining models. 

# =============================================================================
# Section 2.2 - Ordinary linear regression (Equation 1 and 2)
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

# statsmodel variant

# =============================================================================
# Section 2.2 - Ordinary linear regression (Equation 1 and 2) 
# =============================================================================

# this line of code adds an intercept into the regression model. Without it, the model only has a slope parameter
x = sm.add_constant(x)  

# fit the model and print the results
model_sm = sm.OLS(y, x)
results = model_sm.fit()
print(results.summary())

# =============================================================================
# Section 2.3 - Varying intercept-fixed slope model (Equation 3)

# The statsmodel package implementation of linear multilevel models closely follows the implementation used in the lme4 package (outlined in Lindstrom & Bates, JASA, 1988). Hence the results should be identical. The model below has varying intercepts specificed for each member of the ppid group (i.e., an intercept for each participant).

# In the statsmodel package, the random effect for each participant is highlighted in the main table and is titled "Group Var". This refers to the estimated variance (sigma sqaured) of the participant specific randon intercepts. 

# Here we fit a varying intercept model. The "groups = data_RTs_cens_NA_removed["ppid"]" part of the model equations fits an intercept for each participant. This accounts for the non-independence of observations by constraining the non-independent clusters to the same intercept. Remember, this is something we need to do as each member of the random effects group has multiple observations. 
# =============================================================================

mod_2 = smf.mixedlm("TLC_takeover ~ TLC_failure", data_RTs_cens_NA_removed, groups = data_RTs_cens_NA_removed["ppid"])
results_mod_2 = mod_2.fit()
print(results_mod_2.summary())

# =============================================================================
# Section 2.4 - Varying intercept-varying slope model (Equation 4)

# To add a varying slope with respect to the included predictor, specify a variable using the re_formula argument. The variance parameter for the varying intercept is titled "Group Var", the variance parameter for the varying slope is titled "TLC_failure Var", and the covariance parameter highlighting the correlation between the two must be calculated from these values and the "Group x TLC_failure Cov" values: (-0.005 / sqrt(0.007 * 0.005)) ~ -.83. This is obviously more involved than using lme4 in R. 

# Here we fit a varying intercept, varying slope model. The "re_formula = "~TLC_failure"" part of the model allows each participants slope to vary. This accounts for the non-independence of observations by constraining the non-independent clusters to the same intercept, and models the differences in sensitivity between different people in the sample. 

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
# Section 3.2 - MLMs with dummy coded variables (Equation 5)

# Note in the summary of this model that the effect of n_back and lead vehicle are presenting as "n_back[T.True]" and "lead[T.True]". As highlighted in the manuscript, this is because these coefficients represent the effect of N-back or lead vehicle when the other variable is held at "0" (e.g., when the manipulation is not present). 

# =============================================================================

mod_4 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back")
results_mod_4 = mod_4.fit()
print(results_mod_4.summary())

# =============================================================================
# Section 3.5 - Maximal models and singular random effects (Equation 7)

# A maximal model contains a random slope for each fixed effect alongside all possible correlations between random effect parameters. In the model below, the standard deviation for the effect of lead vehicle is the lowest of all the parameters. Y You can also see that the correlation between the N-back slope and the interaction slope is -0.99. This could be considered a borderline singular estimate as such high correlations indicate that the random effects structure might be over parameterised. 

# =============================================================================

mod_5 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back * lead").fit(reml=False)
print(mod_5.summary())


# =============================================================================
# Section 3.5 - LRT for lead vehicle and interaction random effects

# There is currently no dedicated function that computes an LRT for models fitted using mixed.lm. However, you can compute this manually by returning the attribute called 'llf'.

# In *mod_5_1* we remove the the random effect for the interaction. We get a warning when fitting this model; that we have a boundary (singular) fit. The summary of the model indicates that this is from the correlation between the intercept and lead vehicle random effects. This singular random effect may be a consequence of the lack of variance associated with the effect of lead vehicle. 

# Firstly, we compare the original model (*mod_5*) against the model with the random interaction effect removed (*mod_5_1*). The LRT reveals a non-significant effect indicating that the addition of the random interaction effect does not significantly improve the model fit. 

# In *mod_5_2* we remove the lead vehicle random effect - we then compare this against the original model. Once again, we find a non-significant effect indicating the lead vehicle random effect was not improving the model fit. 

# Just for illustration, in *mod_5_3* we remove the N-back random effect. We established in Section 3.4 for that the effect of N-back on gaze behaviour was highly variable. As such, we might expect that including the N-back random effect should improve the model fit relative to *mod_5_2* - the significant LRT tests demonstrates this. 

# =============================================================================

# mod_5 - mod_5_1
mod_5_1 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back + lead").fit(reml=False)
print(mod_5_1.summary())

lr_stat = 2 * (mod_5.llf - mod_5_1.llf)
df_diff = mod_5.df_modelwc - mod_5_1.df_modelwc
p_value = chi2.sf(lr_stat, df_diff)

print(f"LR = {lr_stat:.3f}")
print(f"df = {df_diff}")
print(f"p = {p_value:.5f}")

# mod_5 - mod_5_2
mod_5_2 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back").fit(reml=False)
print(mod_5_2.summary())

lr_stat = 2 * (mod_5.llf - mod_5_2.llf)
df_diff = mod_5.df_modelwc - mod_5_2.df_modelwc
p_value = chi2.sf(lr_stat, df_diff)

print(f"LR = {lr_stat:.3f}")
print(f"df = {df_diff}")
print(f"p = {p_value:.5f}")

# mod_5_2 - mod_5_3
mod_5_3 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"]).fit(reml=False)
print(mod_5_3.summary())

lr_stat = 2 * (mod_5_2.llf - mod_5_3.llf)
df_diff = mod_5_2.df_modelwc - mod_5_3.df_modelwc
p_value = chi2.sf(lr_stat, df_diff)

print(f"LR = {lr_stat:.3f}")
print(f"df = {df_diff}")
print(f"p = {p_value:.5f}")

# =============================================================================
# Section 4 - Comparing MLM outputs to RM ANOVAs
# =============================================================================

# RM ANOVA

# Below we reproduce the write up in the manuscript for the RM ANOVA before providing the code that generated these values.

# "A 2 x2 Repeated Measures ANOVA was conducted to investigate the effect of lead vehicle and N-back on H_s. There was a significant main effect of N-back [F (1, 36) = 50.372, p < 0.001]. This suggests that the gaze of drivers was significantly less dispersed when completing N-back (M = 0.313, SD = 0.142) versus when monitoring a hands-off Level 2 system (M = 0.443, SD = 0.143) with a very large effect size (η_p^2 = 0.58). This significant effect suggests that the distribution of driver’s gaze is reduced when they are under high MWL. As such, H_s is a variable that shows great promise in estimating high MWL in drivers using Level 2 driving systems"

# aggregating data
anova_dat = (
    goodridge_2024_dat
    .groupby(["ppid", "n_back", "lead"], as_index=False)
    .agg(e_norm=("e_norm", "mean"))
)

# checking complete cells
cell_counts = anova_dat.groupby("ppid").size()
print(cell_counts.value_counts())

# removing incomplete participants
complete_ppids = cell_counts[cell_counts == 4].index

anova_dat_complete = anova_dat[
    anova_dat["ppid"].isin(complete_ppids)
]

# running anova
rm_anova = AnovaRM(
    data=anova_dat_complete,
    depvar="e_norm",
    subject="ppid",
    within=["n_back", "lead"],
).fit()

print(rm_anova)

# sample means of e_norm for N-back and no N-back conditions
summary = (
    goodridge_2024_dat
    .groupby("n_back")
    .agg(
        mean_e=("e_norm", "mean"),
        mean_sd=("e_norm", "std")
    )
    .reset_index()
)

print(summary)

# MLM

# Below we reproduce the write up in the manuscript for the MLM before providing the code that generated these values.

# A multilevel model was fitted to investigate the effect of lead vehicle and N-back on H_s. The model revealed a significant main effect of MWL on H_s (β_N  = -0.141, CI_95 = [-0.180, -0.102], p < .001). This suggests that a typical driver’s gaze is significantly less dispersed when completing N-back (M = 0.313, SD = 0.142) versus when monitoring a hands-off Level 2 system (M = 0.443, SD = 0.143). For the average driver this effect is expected to be a reduction of H_s of around 14 percentage points. However, the multilevel model revealed that this effect is not expected to be homogenous across the population. The random effects within the model imply that some drivers can be expected to have reductions in H_s of 33 percentage points, whilst other drivers are expected to have no change in H_s or even slight reversals of the average effect (HI_95 = [-0.331, 0.047]). Whilst H_s seems suitable for estimating MWL for the typical driver, there are many drivers in the population who may experience high MWL but would not be detected using this metric".

# running MLM
mod_4 = smf.mixedlm("e_norm ~ n_back * lead", goodridge_2024_dat, groups = goodridge_2024_dat["ppid"], re_formula = "~n_back")
results_mod_4 = mod_4.fit()
print(results_mod_4.summary())

# Fixed effect for n_back
beta_n = results_mod_4.fe_params["n_back[T.True]"]

# SD of random slope for n_back
sigma_beta_n = np.sqrt(results_mod_4.cov_re.loc["n_back[T.True]", "n_back[T.True]"])

# Heterogeneity interval
lower = beta_n - 1.96 * sigma_beta_n
upper = beta_n + 1.96 * sigma_beta_n

print(f"Fixed effect (n_back): {beta_n:.3f}")
print(f"Random slope SD: {sigma_beta_n:.3f}")
print(f"95% heterogeneity interval: [{lower:.3f}, {upper:.3f}]")




