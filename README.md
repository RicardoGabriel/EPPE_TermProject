# EPPE Term Project - Synth Package
Term Project for the Effective Programming Practices for Economists course at University of Bonn

The deliverables of this project besides all the coding are the research_paper.pdf and the project_documentation.pdf which can be obtained by running the waf.py feature.

All remaining errors are exclusively my own.

## Disclosure
This package was first created by @gnazareths (https://github.com/gnazareths/synth) and I will try to improve it and utilize it for my term paper in EPPE (University of Bonn) by March 7th, 2019.

Firstly, I will try to face current limitation number 2 by implementing a change in the code which will transform an excel file in a panda dataframe using the method read_excel() find in https://pythonspot.com/read-excel-with-pandas/.

Secondly, I will provide a minimum working example with a real dataset for 32 OECD countries. I will provide a computation of a synthetic control group for Japan by trying to mimic its real per capita gdp series using its real per capita gdp as predictor.

Thirdly, I will add some flexibility to the package by allowing a manual imputation of an initial guess for the weights matrix and some tests for a more complete and correct addition.

Fourthly, I will provide a more complete working example with the same dataset. Following Born et al. (2018) I will provide a computation of a synthetic control group for Great Britain to evaluate the Brexit impact on GDP by trying to mimic its real per capita gdp series using itself as a predictor jointly with real per capita government consumption, unemployment rate, and debt-to-GDP ratio.

Finally, I will finish the project by providing a reproducible research template following @hmgaudecker - http://hmgaudecker.github.io/econ-project-templates/.

## Introduction

synth is a Python package for implementing the Synthetic Control Method for comparative case studies.

The Synthetic Control Method has been used in studies estimating effect of an intervention when a singly unit is exposed to it. Jens Hainmueller, the maintainer of Synth’s R package, here describes the method as a “procedure to construct synthetic control units based on a convex combination of comparison units that approximates the characteristics of the unit that is exposed to the intervention.”

## How Synth works

This version of Synth takes as inputs two matrices: outcomes_matrix and predictors_matrix. The former matrix is exactly on what a researcher would like to measure effect. Conversely, the latter matrix is comprised of data that can effectively predict the outcomes for a unit.

To illustrate this, allow me to cite Abadie, Diamond, and Hainmueller (2010), who estimate the effects of California’s Proposition 99 (tobacco control program) in the per capita consumption of cigarettes. In this study, the outcomes_matrix would have data on the per capita consumption of cigarettes for unit and every year. If the study looks at t time periods, a treated unit, and j control units, the outcomes_matrix would have shape (t, j+ 1). Meanwhile, predictors_matrix is comprised of variables that can predict a unit’s outcomes. For example, the authors of the paper included Log(GDP per capita), retail price of cigarettes, and consumption of beer, among others. If the study looks at k predictors, the predictors_matrix would have shape (k, j+1).

The Synthetic Control Method uses both matrices to find 1) how important each predictor is in determining the outcome, and 2) how to construct a synthetic unit that best represents the treated one in terms of control units. For representing the importance of each predictor, Synth constructs a diagonal matrix V of length k by k, in which the term V.item(i,i) is the importance of the ith predictor for i in [0, 1, ..., k - 1]. For representing the weight of each control unit in the construction of the optimal synthetic one, Synth creates a vector W of length j, in which W[i] is the weight of the ith control unit for i in [0, 1, ..., j - 1].

To find the two unknowns, matrix V and vector W.

W* is the set of weights that minimizes (X0 W - X1)'V(X0  W - X1), in which X0 is the matrix of predictors for control units, X1is the vector of predictors for the treated unit, and V is the matrix with the importance of each predictor. As one can see, W* is a function of V: different matrices V yield different optimal weights. On the other hand, V* minimizes (Z0 W*(V) - Z1)'(Z0  W*(V) - Z1), in which Z0 is the matrix of outcomes for control units, Z1is the matrix of outcomes for the treated unit, and W*(V) is the optimal combination of weights given the matrix V.

In this implementation, Synth uses a nested optimization with SciPy quadratic programming minimization functions optimize.minimize and optimize.fmin_slsqp. To achieve this, I call my function get_v_1, which finds the variable v that minimizes the function get_v_0, which in turn calls the function get_w and returns the residual sum of squares associated with given values of v and w. This last function, get_w, finds the variable w that minimizes the rss associated with v and any values of w.

    def w_rss(w, v, x0, x1):
      k = len(x1)
      importance = np.zeros((k,k))
      np.fill_diagonal(importance, v)
      predictions = np.dot(x0,w)
      errors = x1 - predictions
      weighted_errors = np.dot(importance, errors)
      weighted_rss = sum(weighted_errors**2)[0]
      return weighted_rss

    def w_constraint(w, v, x0, x1):
      return np.sum(w) - 1

    def v_rss(w, z0, z1):
      predictions = np.dot(z0,w)
      errors = z1 - predictions
      rss = sum(errors ** 2)[0]
      return rss

    def get_w(w, v, x0, x1):
      weights = fmin_slsqp(w_rss, w, f_eqcons=w_constraint, 
             bounds=[(0.0, 1.0)]*len(w),
             args=(v, x0, x1), disp=False, full_output=True)[0]
      return weights

    def get_v_0(v, w, x0, x1, z0, z1):
      weights = get_w(w,v,x0,x1)
      rss = v_rss(weights, z0, z1)
      return rss

    def get_v_1(v, w, x0, x1, z0, z1):  
      result = fmin_slsqp(get_v_0, v, args=(w, x0, x1, z0, z1), 
              bounds=[(0.0, 1.0)]*len(v))
      return result

    def get_estimate(x0, x1, z0, z1, y0, w):
      (k,j) = x0.shape
      v = [1.0]*k
      predictors = get_v_1(v, w, x0, x1, z0, z1)
      controls = np.array(get_w(w, predictors, x0, x1)).transpose()
      estimates = np.dot(y0,controls)
      return estimates, predictors, controls

Upon finding the optimal vector W (and, by definition, V as well), Synth multiplies the Z0 (outcomes of the control units) by W to find an estimate (or a counterfactual) of the Z1 vector. Synth can plot both the estimate Z1 and the actual Z1, so the researcher can compare how well the model represents the actual data.

## Why Synth is awesome

The breakthrough here is that Synth often returns an extremely well-fitted model of the actual data during the periods for which it optimizes. Imagine this scenario: you want to study the effects of an event that happened in 1999 by plotting the outcomes of the synthetic controls against the actual outcomes between 1990 and 2010. It only makes sense to optimize Synth for the periods [1990:1998]. This way, you will see how much the actual data will deviate from the synthetic once, which was calibrated with outcomes and predictors before the event.

## How to call Synth


    def synth_tables( df,                       ## dataframe imported from excel and already treated
                           predictors,          ## list of predictor variables
                           treated_unit,        ## string with the index of the treated unit
                           control_units,       ## list of strings with indexes of all control units
                           index_variable,      ## string which tells us which variable is the index we used before
                           measured_variable,   ## string with the outcome variable
                           Weights,             ## initial guess for weights (np.ndarray)
                           time_variable,       ## string with the time variable 
                           predict_time,        ## these are the time periods for which you are predicting the measured variable
                           optimize_time,       ## these are the time periods for which you are optimizing the RSS
                           plot_time            ## years which you want to plot
                     )

      control_units.sort()
      predictors.sort()
      plot_time.sort()

      X0, X1, Y0, Y1, Z0, Z1 = dataprep(foo, 
                 predictors, 
                 treated_unit, 
                 control_units, 
                 index_variable, 
                 measured_variable,
                 Weights,
                 time_variable,
                 predict_time, 
                 optimize_time, 
                 plot_time, 
                 function="mean")

      (est, predict, ctrls) = get_estimate(X0, X1, Z0, Z1, Y0, Weights)
      predict = [ round(elem,6) for elem in predict ]
      ctrls = [ round(elem,6) for elem in ctrls ]
      estimated_predictors = np.dot(X0,ctrls).transpose()
      predictors_table = pd.DataFrame({'Synthetic':estimated_predictors, 'Actual': X1.transpose()[0]}, index=predictors)
      estimated_outcomes = np.dot(Y0,ctrls)
      outcomes_table = pd.DataFrame({'Synthetic':estimated_outcomes, 'Actual':Y1.transpose()[0]},index=plot_time)
      predictors_weights = pd.DataFrame({'Weight':predict}, index=predictors)
      controls_weights = pd.DataFrame({'Weight':ctrls}, index=control_units)

      print ("Predictors Table")
      print ("---")
      print (predictors_table)
      print (" ")
      print ("Outcomes Table")
      print ("---")
      print (outcomes_table)
      print (" ")
      print ("Predictors' Weights")
      print ("---")
      print (predictors_weights)
      print (" ")
      print ("Controls' Weights")
      print ("---")
      print (controls_weights)

    
      estimates = estimated_outcomes
      actual_values = Y1.transpose()[0]
      plt.plot(range(len(estimates)),estimates, 'r--', label="Synthetic Control")
      plt.plot(range(len(estimates)),actual_values, 'b-', label="Actual Data")
      plt.axvline(x=predict_time[-1])
      plt.title("Synthetic Control Model")
      plt.ylabel(measured_variable)
      plt.xlabel(time_variable)
      plt.legend(loc='upper left')
      plt.savefig('Synthetic_Control_Method.png')
      plt.show()
    
      return controls_weights


    
## References: if you want to know more about Synth

[Package Synth (Hainmueller and Diamond, 2015)](https://cran.r-project.org/web/packages/Synth/Synth.pdf)

[Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California’s Tobacco Control Program (Abadie, Diamond and Hainmueller, 2012)](http://web.stanford.edu/~jhain/Paper/JASA2010.pdf)

[The Economic Costs of Conflict: A Case Study of the Basque Country (Abadie and Gardeazabal, 2003)](https://www.aeaweb.org/articles?id=10.1257/000282803321455188)

[The Costs of Economic Nationalism: Evidence from the Brexit Experiment (Born, Müller, Schularick and Sedlacek, 2018)](http://www.benjaminborn.de/publication/bmss2017/)
