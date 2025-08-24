# Evaluate the upper and lower bounds of the chance of a defensive player remaining in the NFL after 4 years

# CSV generated from data in longevity.ipynb
df = read_csv("./player_analysis/trey_hendrickson/retired_players_over_30.csv")

# Turn each age in df into a percentage of players who retired at that age
retirement_ages = df %>% group_by(age) %>%
  summarize(retired_players = n()) %>%  mutate(total_players = sum(retired_players)) %>%
  mutate(retirement_rate = retired_players / total_players)

retirement_model <- lm(retirement_rate ~ poly(age, 2), data=retirement_ages)

ggplot(retirement_ages, aes(x=age, y=retirement_rate)) +
  geom_point()

retirement_predictions <- as.data.frame(predict(retirement_model, interval="prediction"))

survival_lower <- 1-retirement_predictions$lwr
survival_upper <- 1-retirement_predictions$upr

# Multiply the survival values to each other for the first four seasons 
lb_chance_of_lasting_4_seasons <- prod(head(survival_lower, 4))
ub_chance_of_lasting_4_seasons <- prod(head(survival_upper, 4))

# Switch upper and lower because this is survival rate
cat(ub_chance_of_lasting_4_seasons, 'to', lb_chance_of_lasting_4_seasons)