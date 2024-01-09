# Multilevel model applications

**Disclaimer**: *This is a working repository and so information and code may change*

## Overview: Multilevel models

Multilevel models are extensions of normal linear regression that allow a researcher to model the inherent variability between clusters in a wider population. As an example, lets assume there is variable X that we believe to be related to variable Y:

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/6164c2a6-b6ff-4978-80eb-6982edd82cba)

Traditionally, one might fit a regression model to estimate the extent to which X predicts Y:

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/943bd0cc-af62-4859-ae52-3d4cc14f054e)

However, it's a complicated world, and not everyone or -thing is the same. There are groups within the whole that might differ in interesting ways. Perhaps for some of those groups, X predicts Y very strongly; for others, less so. When those groups are highlighted in different colours, the traditional regression model starts to look slightly inadequate to explain how X is related to Y. 

![image](https://github.com/courtneygoodridge/multilevel_model_HF_applications/assets/44811378/4e249d34-17c3-463b-aca1-6525303d88ec)

I have given numerous talks and presentations about this analysis method. I believe it to be the present and future of statistical modelling, and concur with Richard McElreath when he says that it should be the default tool (and researchers should provide strong reasoning why they are choosing to use a different method). Despite my personal efforts, the uptake of multilevel models is slow in my current research area. This is in spite of the vast improvements in computational power that allow Frequentist and Bayesian versions of these models to be fitted with relative computational ease. 

I believe that one reason for the lack of uptake in my current area of work is a lack of formal tutorials. Whilst tutorials exist, they are largely in areas of Ecology, Linguistics, or Edcuation research. This is not surprising, considering that the quantitative data produced in these research areas is naturally hierarchical (e.g., Education: pupils within classes, classes within schools, schools within counties, and so on). These tutorials are fine in and off themselves, and can undoubtedly help people under the models. However, from my own experience, the hurdle is lessened if their is a tutorial that focuses specifically on the area you are working on. In this sense, I am providing the tutorial that I wanted when I first started working on these models back in 2019.  

This repository contains the code that produces the analysis and plots for the larger manuscript. There are things in the code that are not covered in great detail in the manuscript, and vice versa. The two accompany each other. 

## Code and analysis

This particular analysis focuses on Frequentist multilevel models using the `lme4` package to fit them. This is probably the most common package in the literature. Some people may use the `lmerTest` package in order to obtain p values; the `lme4` package does not provide these. The reasons for this have been detailed extensively by [Douglas Bates](https://stat.ethz.ch/pipermail/r-help/2006-May/094765.html), one of the creators of the `lme4` package and the person who wrote the `lmer()` function. Personally, I am an advocate of the "new statistics" with a move away from null hypothesis signifiance testing, towards estimatation, quantifying variability, and meta analysis (Geoff Cumming's paper, ["The new statistics: Why and how"](https://journals.sagepub.com/doi/full/10.1177/0956797613504966) is well worth a read if people are interested in this approach). Hence I do away with p values altogether. 





