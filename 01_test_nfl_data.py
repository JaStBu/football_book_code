## import packages
## make sure you installed both packages using pip in the terminal
import pandas as pd
import nfl_data_py as nfl
import os

cols = nfl.see_pbp_cols()
print("Columns in the play by play data:")
for col in cols:
    print(col)

## Load data from the package
chap_1_file = "./data/pbp_py_chap_1.csv"

if os.path.isfile(chap_1_file):
    pbp_py = pd.read_csv(chap_1_file, low_memory=False)
else:
    pbp_py = nfl.import_pbp_data([2021])
    pbp_py.to_csv(chap_1_file)

## filter out passing data
filter_crit = 'play_type == "pass" & air_yards.notnull()'
pbp_py_p = (
    pbp_py.query(filter_crit)
    .groupby(["passer_id", "passer"])
    .agg({"air_yards": ["count", "mean", "min", "max"]})
)

# further inout: https://www.analyticsvidhya.com/blog/2020/03/groupby-pandas-aggregating-data-python/
# and: https://stackoverflow.com/questions/53943319/what-are-all-pandas-agg-functions
# and: https://pandas.pydata.org/pandas-docs/stable/reference/groupby.html#dataframegroupby-computations-descriptive-stats

## format and print data for passing plays
pbp_py_p.columns = list(map("_".join, pbp_py_p.columns.values))
sort_crit = "air_yards_count > 100"
print(
    pbp_py_p.query(sort_crit)
    .sort_values(by="air_yards_mean", ascending=[False])
    .to_string()
)