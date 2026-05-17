import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import re

df = pd.read_excel(r"C:\Users\Admin\Downloads\Dataset\New folder\IEX_Weather_final.xlsx")

print(df.head())

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
stats.to_excel(r"C:\Users\Admin\Downloads\statistics_summary.xlsx")


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


print(df.columns.tolist())



mcp_col = "MCP (Rs/MWh) *"
mcv_col = "MCV (MW)"
purchase_col = "Purchase Bid (MW)"
sell_col = "Sell Bid (MW)"


count = 0

for col in df.columns:

    col_lower = col.lower()

    if df[col].dtype == "O":
        continue

    if col == mcp_col:
        x, y = df[mcp_col], df[mcv_col]

    elif col == mcv_col:
        x, y = df[mcv_col], df[mcp_col]

    elif col == purchase_col:
        x, y = df[purchase_col], df[mcp_col]

    elif col == sell_col:
        x, y = df[sell_col], df[mcp_col]

    elif "temperature" in col_lower:
        x, y = df[col], df[mcp_col]

    elif "humidity" in col_lower:
        x, y = df[col], df[purchase_col]

    elif "cloud" in col_lower:
        x, y = df[col], df[mcp_col]

    elif "wind" in col_lower:
        x, y = df[col], df[mcv_col]

    elif "radiation" in col_lower:
        x, y = df[col], df[mcp_col]

    else:
        continue

    temp_df = pd.concat([x, y], axis = 1).dropna()
    if temp_df.shape[0] == 0:
        continue

    x_clean = temp_df.iloc[:, 0]
    y_clean = temp_df.iloc[:, 1]

    plt.figure(figsize=(6,5))
    plt.scatter(x_clean, y_clean, alpha=0.5)

    plt.xlabel(x_clean.name)
    plt.ylabel(y_clean.name)
    plt.title(f"{x_clean.name} vs {y_clean.name}")


    plt.show()
    plt.close()

    count += 1



output_folder = "column_wise_multivariate_scatterplots"
os.makedirs(output_folder, exist_ok=True)

numeric_df = df.select_dtypes(include=["int64", "float64"]).dropna(axis = 1, how = "all")
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

    plot_df = numeric_df[[x_col, target_col, color_col]].dropna()

    plt.figure(figsize=(8, 6))

    sns.scatterplot(
        data=plot_df,
        x=x_col,
        y=target_col,
        hue=color_col,
        palette="viridis",
        alpha=0.7
    )

    plt.title(f"{target_col} vs {x_col} colored by {color_col}")
    plt.xlabel(x_col)
    plt.ylabel(target_col)
    plt.legend(title=color_col, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    file_name = clean_name(target_col)
    plt.savefig(
        f"{output_folder}/{file_name}_multivariate_scatterplot.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

print("Done. Scatterplot graphs saved in:", output_folder)
print("Total graphs created:", len(os.listdir(output_folder)))


#data preprocessing

import numpy as np

pd.set_option('display.max_rows', None)
df.dtypes

duplicate=df.duplicated()
duplicate

df.drop_duplicates()

num_cols = df.select_dtypes(include=['int64','float64']).columns

IQR = df[num_cols].quantile(0.75) - df[num_cols].quantile(0.25)

lower_limit = df[num_cols].quantile(0.25) - (1.5 * IQR)
upper_limit = df[num_cols].quantile(0.75) + (1.5 * IQR)

df[num_cols] = np.where(
    df[num_cols] > upper_limit,
    upper_limit,
    np.where(df[num_cols] < lower_limit, lower_limit, df[num_cols])
)

col = "MCP (Rs/MWh) *"

df["mcp_new"] = pd.cut(
    df[col],
    bins=[
        df[col].min(),
        df[col].median(),
        df[col].max()
    ],
    include_lowest=True,
    labels=["Low", "High"]
)

cols_to_convert = [col for col in df.columns 
                   if any(x in col.lower() for x in ['humidity', 'cloud', 'shortwave'])]

df[cols_to_convert] = df[cols_to_convert].astype('int64')
df.dtypes

df.isna().sum()


df.to_csv(r"C:\Users\Admin\OneDrive\Desktop\final_dataset.csv", index=False)



