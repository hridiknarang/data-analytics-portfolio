import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re 

df_1 = pd.read_excel(r"C:\Users\Admin\Downloads\Reports and Dashboard\Data\Reports and Dashboards Data.xlsx")
df_2 = pd.read_excel(r"C:\Users\Admin\Downloads\Reports and Dashboard\Data\mother.xlsx", skiprows=1)
df_3 = pd.read_excel(r"C:\Users\Admin\Downloads\Reports and Dashboard\Data\offspring.xlsx", skiprows=1)
df_4 = pd.read_excel(r"C:\Users\Admin\Downloads\Reports and Dashboard\Data\elisha.xlsx")
df_5  = pd.read_excel(r"C:\Users\Admin\Downloads\Reports and Dashboard\Data\Reports and Dashboards Data2.xlsx")
df_6 = pd.read_excel(r"C:\Users\Admin\Downloads\Reports and Dashboard\Data\Reports and Dashboards Data3.xlsx")

all_dfs = {
    "df_1": df_1,
    "df_2": df_2,
    "df_3": df_3,
    "df_4": df_4,
    "df_5": df_5,
    "df_6": df_6
}

for name, df in all_dfs.items():

    print("\n========================")
    print("Processing {name}")
    print("========================")


Processing : df_1
Processing : df_2
Processing : df_3
Processing : df_4
Processing : df_5
Processing : df_6


stats = pd.DataFrame()

stats["mean"] = df.mean(numeric_only=True)
stats["median"] = df.median(numeric_only=True)
stats["mode"] = df.mode().iloc[0]
stats["std_dev"] = df.std(numeric_only=True)
stats["variance"] = df.var(numeric_only=True)
stats["min"] = df.min(numeric_only=True)
stats["max"] = df.max(numeric_only=True)
stats["range"] = stats["max"] - stats["min"]
stats["skewness"] = df.skew(numeric_only=True)
stats["kurtosis"] = df.kurtosis(numeric_only=True)

stats = stats.round(2)

print(stats)

stats.to_excel(r"C:\Users\Admin\Downloads\{name}_statistics_summary_project_IVF.xlsx")


# HISTOGRAM + BOXPLOT
    

numeric_cols = df.select_dtypes(include='number').columns

for col in numeric_cols:

        plt.figure(figsize=(10,4))

        plt.subplot(1,2,1)
        plt.hist(df[col].dropna(), bins='auto')
        plt.title(f"{col} - Histogram")
        plt.xlabel(col)

        plt.subplot(1,2,2)
        plt.boxplot(df[col].dropna())
        plt.title(f"{col} - Boxplot")

        plt.tight_layout()
        plt.show()


# MULTIVARIATE SCATTERPLOTS


output_folder = f"{name}_multivariate_scatterplots"
os.makedirs(output_folder, exist_ok=True)

numeric_df = df.select_dtypes(
include=["int64", "float64"]).dropna(axis=1, how="all")

numeric_df = numeric_df.loc[:, numeric_df.nunique() > 1]
corr_matrix = numeric_df.corr()

def clean_name(name):
        name = re.sub(r'[\\/*?:"<>|]', "_", str(name))
        return name[:80]

for target_col in corr_matrix.columns:

  related_cols = (
            corr_matrix[target_col]
            .drop(target_col)
            .abs()
            .sort_values(ascending=False)
            .head(2)
            .index
            .tolist()
          )
  if len(related_cols) < 2:
     continue

x_col = related_cols[0]
color_col = related_cols[1]

plot_df = numeric_df[
            [x_col, target_col, color_col]
        ].dropna()

plt.figure(figsize=(8, 6))

sns.scatterplot(
            data=plot_df,
            x=x_col,
            y=target_col,
            hue=color_col,
            palette="viridis",
            alpha=0.7
        )

plt.title(
            f"{target_col} vs {x_col} colored by {color_col}"
        )

plt.xlabel(x_col)
plt.ylabel(target_col)

plt.legend(
            title=color_col,
            bbox_to_anchor=(1.05, 1),
            loc="upper left"
        )

plt.tight_layout()

file_name = clean_name(target_col)

plt.savefig(
            f"{output_folder}/{file_name}_multivariate_scatterplot.png",
            dpi=300,
            bbox_inches="tight"
        )

plt.close()

print("Graphs saved in:", output_folder)
print("Total graphs created:", len(os.listdir(output_folder)))


# DATA PREPROCESSING

duplicate = df.duplicated()

print("Duplicate Rows:")
print(duplicate.sum())

df = df.drop_duplicates()

num_cols = df.select_dtypes(
        include=['int64', 'float64']
    ).columns

IQR = (
        df[num_cols].quantile(0.75)
        - df[num_cols].quantile(0.25)
    )

lower_limit = (
df[num_cols].quantile(0.25)
        - (1.5 * IQR)
    )

upper_limit = (
        df[num_cols].quantile(0.75)
        + (1.5 * IQR)
    )

df[num_cols] = np.where(
        df[num_cols] > upper_limit,
        upper_limit,
        np.where(
            df[num_cols] < lower_limit,
            lower_limit,
            df[num_cols]
        )
    )

    
# COLUMN TYPE CONVERSION

cols_to_convert = [
        col for col in df.columns
        if any(
            x in col.lower()
            for x in [
                
            ]
        )
    ]

if len(cols_to_convert) > 0:
        df[cols_to_convert] = (
            df[cols_to_convert]
            .astype('int64')
        )

print("\nMissing Values:")
print(df.isna().sum())


# SAVE FINAL DATASET

df.to_csv(r"C:\Users\Admin\Downloads\{name}_final_dataset_project_IVF.csv",index=False)
























