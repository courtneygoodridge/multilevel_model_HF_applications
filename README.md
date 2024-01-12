# Multilevel model applications

**Disclaimer**: *This is a working repository and so information and code may change*

## Overview: Multilevel models

Multilevel models are extensions of normal linear regression. They allow a researcher or scientist to model the inherent variability between related clusters in a wider population. As an example, lets assume there is a variable X that we believe to be related to a variable Y:

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

This repository contains the code that produces the analysis and plots for the larger manuscript that I am currently working on. This particular analysis focuses on Frequentist multilevel models using the `lme4` package to fit them. This is probably the most common package in the literature. Some people may use the `lmerTest` package in order to obtain p values; the `lme4` package does not provide these. The reasons for this have been detailed extensively by [Douglas Bates](https://stat.ethz.ch/pipermail/r-help/2006-May/094765.html), one of the creators of the `lme4` package and the person who wrote the `lmer()` function. Personally, I am an advocate of the "new statistics" movement; moving away from null hypothesis signifiance testing and towards estimatation, quantifying variability, and meta analysis (Geoff Cumming's paper, ["The new statistics: Why and how"](https://journals.sagepub.com/doi/full/10.1177/0956797613504966) is well worth a read if people are interested in this approach). Therefore, I do not focus on p values in analysis script (or the manuscript itself). 





