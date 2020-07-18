from sys import argv
import pandas as pd

# Check if correct args passed
if len(argv) != 2:
    print("Pass path to one csv data file")
    exit(1)

# Read csv file from args
df = pd.read_csv(argv[1])
print(df)

# Drop columns not needed
df = df.drop(['V1', 'allbed_lower','allbed_upper', 'ICUbed_lower', 'ICUbed_upper', 'InvVen_lower','InvVen_upper', 'admis_lower', 'admis_upper', 'newICU_lower', 'newICU_upper', 'bedover_lower', 'bedover_upper', 'icuover_lower', 'icuover_upper', 'deaths_lower', 'deaths_upper', 'totdea_lower', 'totdea_upper', 'deaths_mean_smoothed', 'deaths_lower_smoothed', 'deaths_upper_smoothed', 'totdea_mean_smoothed', 'totdea_lower_smoothed', 'totdea_upper_smoothed', 'est_infections_lower', 'est_infections_upper', 'mobility_data_type', 'total_tests_data_type'], axis=1)

# Create data frame copies and filter for countries
df_ger = df[df.location_name == "Germany"]
df_it = df[df.location_name == "Italy"]
df_us = df[df.location_name == "United States of America"]

# Drop projected (at least future) data
df_ger = df_ger[df_ger.date <= "2020-07-14"]
df_it = df_it[df_it.date <= "2020-07-14"]
df_us = df_us[df_us.date <= "2020-07-14"]

# Write new file
df_ger.to_csv("covid-ger.csv")
df_it.to_csv("covid-it.csv")
df_us.to_csv("covid-us.csv")