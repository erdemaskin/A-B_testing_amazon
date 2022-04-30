################################################ ###
# Comparison of A/B Test and Conversion of Bidding Methods
################################################ ###

################################################ ###
# Business Problem
################################################ ###

# Facebook recently available alternative to the bidding type called "maximum bidding"
# Introduced a new type of bid, "average bidding" as #. One of our customers, bombbambomba.com,
# decided to test this new feature and have more conversions of average bidding than maximum bidding
# He wants to do an A/B test to see if it returns #. The A/B test has been going on for 1 month and
# bombabomba.com is now waiting for you to analyze the results of this A/B test.
# ultimate success criterion is Purchase. Therefore, the focus should be on Purchase metric for statistical testing.


################################################ ###
# Dataset Story
################################################ ###

# What users see and click in this dataset, which includes a company's website information
# There is information such as the number of advertisements, as well as the earnings information from here. Control and Test
# There are two separate data sets, the # group. These datasets are on separate pages of ab_testing.xlsxexcel.
# takes. Maximum Bidding was applied to the control group and AverageBidding was applied to the test group.

# impression: Number of ad views
# Click: Number of clicks on the displayed ad
# Purchase: The number of products purchased after the ads clicked
# Earning: Earnings after purchased products

################################################ ###
# Project Tasks
################################################ ###

################################################ ###
# Task 1: Preparing and Analyzing Data
################################################ ###

# Step 1: Read the dataset ab_testing_data.xlsx consisting of control and test group data. Assign control and test group data to separate variables.

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("week_4/ab_testing.xlsx" , sheet_name="Control Group")
dataframe_test = pd.read_excel("week_4/ab_testing.xlsx" , sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()
df_control.head()
df_test.head()
# Step 2: Analyze control and test group data.


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


# Step 3: After the analysis process, combine the control and test group data using the concat method.

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control, df_test], axis=0, ignore_index=False)
df.head()





#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Step 1: Define the hypothesis.

# H0 : M1 = M2 (There is no difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a difference between the purchasing averages of the control group and test group.)


# Step 2: Analyze the purchase averages for the control and test group

df_test["Purchase"].mean()
df_control["Purchase"].mean()
df.groupby("group").agg({"Purchase": "mean"})



################################################ ###
# TASK 3: Performing Hypothesis Testing
################################################ ###

# Step 1: Check the assumptions before testing the hypothesis. These are Assumption of Normality and Homogeneity of Variance.

# Test whether the control and test groups comply with the normality assumption, separately via the Purchase variable.
# Normality Assumption :
# H0: Assumption of normal distribution is provided.
# H1: Normal distribution assumption not provided
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED
# Is the assumption of normality according to the test result provided for the control and test groups?
# Interpret the p-values obtained.


test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
df.loc[df["group"] == "control", "Purchase"].hist()
plt.show()
# p-value=0.5891
# HO cannot be denied. The values of the control group provide the assumption of normal distribution.


# Variance Homogeneity :
# H0: Variances are homogeneous.
# H1: Variances Are Not Homogeneous.
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED
# Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.
# Is the assumption of normality provided according to the test result? Interpret the p-values obtained.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1083
# HO cannot be denied. The values of the Control and Test groups provide the assumption of variance homogeneity.
# Variances are Homogeneous.

# Step 2: Select the appropriate test according to the Normality Assumption and Variance Homogeneity results

# Since assumptions are provided, independent two-sample t-test (parametric test) is performed.
# H0: M1 = M2 (There is no mean difference between the control group and test group purchase mean.)
# H1: M1 != M2 (There is a mean difference between the control group and test group purchase mean)
# p<0.05 HO RED , p>0.05 HO CANNOT BE REJECTED

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Step 3: Purchasing control and test groups by considering the p_value obtained as a result of the test
# Comment if there is a statistically significant difference between the # means.

# p-value=0.3493
# HO cannot be denied. There is no statistically significant difference between the control and test group purchasing averages.


################################################ ############
# TASK 4 : Analysis of Results
################################################ ############

# Step 1: Which test did you use, give reasons.


# Step 2: Advise the customer according to the test results you have obtained.