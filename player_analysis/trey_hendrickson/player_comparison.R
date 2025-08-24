# R Script to calculate prediction intervals for a polynomial fit of sack and tackle data for
# players found to have similar seasons to Trey Hendricksons's 2023 and 2024 seasons

# All data was found/calculated in python files that can be found in "player_comparison.ipynb"
# R was an easier place to calculate this prediction interval for me

library(ggplot2)
library(tidyverse)
library(readr) 
library(tibble)

# All players in this dataset started with age no lower than 22
FIRST_AGE = 22
MAX_AGE=36
TREY_HENDRICKSON_AGE = 30

# Sacks
x <- FIRST_AGE:MAX_AGE
y <- c(5.0, 5.25, 10.285714285714286, 10.642857142857142, 11.785714285714286, 15.083333333333334, 9.416666666666666, 11.75, 13.0, 9.0, 9.1, 5.875, 6.875, 1.6666666666666667, 9.0)

sacks_model = lm(y ~ poly(x, 2))

# I wanted to predict Trey's PI for future sacks
sack_predictions <- predict(sacks_model, interval="prediction")
trey_future_sacks <- tail(sack_predictions, MAX_AGE-TREY_HENDRICKSON_AGE)

# Results for those who don't want to run R Scripts
# fit        lwr      upr
# 10.580452  4.3403662 16.82054
# 9.734926  3.5269620 15.94289
# 8.617284  2.3980582 14.83651
# 7.227525  0.8983661 13.55668
# 5.565649 -1.0356331 12.16693
# 3.631656 -3.4630163 10.72633 

ggplot(tibble(x, y), aes(x=x, y=y)) +
       geom_point() +
       stat_smooth(method='lm', formula='y ~ poly(x, 2)')

# TACKLES
y <- c(17.5, 28.5, 47.285714285714285, 42.714285714285715, 39.142857142857146, 41.166666666666664, 37.166666666666664, 34.833333333333336, 42.5, 36.4, 35.8, 25.25, 29.0, 21.666666666666668, 45.0)

tackles_model = lm(y ~ poly(x, 2))

# I wanted to predict Trey's PI for future tackles
tackles_predictions <- predict(tackles_model, interval="prediction")
trey_future_tackles <- tail(tackles_predictions, MAX_AGE-TREY_HENDRICKSON_AGE)

# Results for those who don't want to run R Scripts
# fit       lwr      upr
# 37.78762 17.610088 57.96516
# 36.66865 16.594981 56.74232
# 35.13640 15.026311 55.24648
# 33.19086 12.725300 53.65641
# 30.83203  9.486558 52.17751
# 28.05993  5.119057 51.00080

ggplot(tibble(x, y), aes(x=x, y=y)) +
  geom_point() +
  stat_smooth(method='lm', formula='y ~ poly(x, 2)')