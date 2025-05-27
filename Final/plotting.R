library(tidyverse)

power <- read_csv("power_results.csv")
dem <- read_csv("dem_results.csv")
demcon <- read_csv("demcons_results.csv")

clean <- function(df) {
  df |> rename(consol_lvl = `Consolidation Level`,
               dem_lvl = `Democracy Level`) |>
    mutate(dems = Democracies / num_nodes,
           autos = Autocracies / num_nodes,
           greys = Grey / num_nodes)
}

power_results <- power |>
  clean() |>
  group_by(Step, power_change) |>
  summarize(dem_lvl = mean(dem_lvl, na.rm = TRUE),
            consol_lvl = mean(consol_lvl, na.rm = TRUE),
            dems = mean(dems),
            autos = mean(autos),
            greys = mean(greys))

power_results |> group_by(power_change) |>
  ggplot(aes(x = Step, y = dem_lvl, color = factor(power_change))) +
  geom_line() +
  scale_color_grey(name = "Variability in Power") +
  ylab("Democracy Level") +
  labs(title = "Democracy Level for Increasing Power Variability",
       caption = paste("Number of Runs:", length(unique(power$RunId))))

power_results |> group_by(power_change) |>
  ggplot(aes(x = Step, y = consol_lvl, color = factor(power_change))) +
  geom_line() +
  scale_color_grey(name = "Variability in Power") +
  ylab("Consolidation Level") +
  labs(title = "Consolidation Level for Increasing Power Variability",
       caption = paste("Number of Runs:", length(unique(power$RunId))))

demsimp_results <- demcon |> clean() |>
  group_by(Step, dem_levels) |>
  summarize(dem_lvl = mean(dem_lvl, na.rm = TRUE),
            consol_lvl = mean(consol_lvl, na.rm = TRUE),
            dems = mean(dems),
            autos = mean(autos),
            greys = mean(greys))

demsimp_results |> group_by(dem_levels) |>
  ggplot(aes(x = Step, y = dem_lvl, color = factor(dem_levels))) +
  geom_line() +
  scale_color_grey(name = "Initial Democracies") +
  ylab("Democracy Level") +
  labs(title = "Democracy Level Based on Starting Level of Democracies",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))
demsimp_results |> group_by(dem_levels) |>
  ggplot(aes(x = Step, y = consol_lvl, color = factor(dem_levels))) +
  geom_line() +
  scale_color_grey(name = "Initial Democracies") +
  ylab("Consolidation Level") +
  labs(title = "Consolidation Level Based on Starting Level of Democracies",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))

con_results <- demcon |> clean() |>
  group_by(Step, consol_levels) |>
  summarize(dem_lvl = mean(dem_lvl, na.rm = TRUE),
            consol_lvl = mean(consol_lvl, na.rm = TRUE),
            dems = mean(dems),
            autos = mean(autos),
            greys = mean(greys))

con_results |> group_by(consol_levels) |>
  ggplot(aes(x = Step, y = dem_lvl, color = factor(consol_levels))) +
  geom_line() +
  scale_color_grey(name = "Initial Democracies") +
  ylab("Democracy Level") +
  labs(title = "Democracy Level Based on Starting Consolidation Levels",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))
con_results |> group_by(consol_levels) |>
  ggplot(aes(x = Step, y = consol_lvl, color = factor(consol_levels))) +
  geom_line() +
  scale_color_grey(name = "Initial Democracies") +
  ylab("Consolidation Level") +
  labs(title = "Consolidation Level Based on Starting Consolidation Levels",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))


dem_results <- dem |>
  clean() |>
  group_by(Step, dem_levels) |>
  summarize(dem_lvl = mean(dem_lvl, na.rm = TRUE),
            consol_lvl = mean(consol_lvl, na.rm = TRUE),
            dems = mean(dems),
            autos = mean(autos),
            greys = mean(greys))

dem_results |> group_by(dem_levels) |>
  ggplot(aes(x = Step, y = dem_lvl, color = factor(dem_levels))) +
  geom_line() +
  scale_color_grey() +
  theme(legend.position = "none") +
  ylab("Democracy Level") +
  labs(title = "Democracy Level Based on Starting Level of Democracies",
       caption = paste("Number of Runs:", length(unique(dem$RunId))))
dem_results |> group_by(dem_levels) |>
  ggplot(aes(x = Step, y = consol_lvl, color = factor(dem_levels))) +
  geom_line() +
  scale_color_grey() +
  theme(legend.position = "none") +
  ylab("Consolidation Level") +
  labs(title = "Consolidation Level Based on Starting Level of Democracies",
       caption = paste("Number of Runs:", length(unique(dem$RunId))))

gen_results <- demcon |> clean() |> group_by(Step) |>
  summarize(dem_lvl = mean(dem_lvl, na.rm = TRUE),
            consol_lvl = mean(consol_lvl, na.rm = TRUE),
            dems = mean(dems),
            autos = mean(autos),
            greys = mean(greys))

gen_results |>
  ggplot(aes(x = Step, y = dem_lvl)) +
  geom_smooth() +
  ylab("Democracy Level") +
  labs(title = "Mean Democracy Level Across Runs",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))

gen_results |>
  ggplot(aes(x = Step, y = consol_lvl)) +
  geom_smooth() +
  ylab("Consolidation Level") +
  labs(title = "Mean Consolidation Level Across Runs",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))

gen_results |>
  ggplot(aes(x = Step)) +
  geom_smooth(aes(y = autos, color = "Autocracies")) +
  geom_smooth(aes(y = dems, color = "Democracies")) +
  geom_smooth(aes(y = greys, color = "Grey Area States")) +
  scale_color_manual(name = "Regime Type",
                     values = c("darkblue", "darkred", "darkgrey")) +
  ylab("Proportion of Regimes") +
  labs(title = "Average Proportion of States Across Runs",
       caption = paste("Number of Runs:", length(unique(demcon$RunId))))