import pandas as pd
import pyreadstat
import matplotlib.pyplot as plt
df, meta = pyreadstat.read_sav("GSS2018.sav")

print(meta.column_names_to_labels["abany"])
gss2018 = pd.read_spss("GSS2018.sav")
gss2021 = pd.read_spss("GSS2021.sav")
gss2022 = pd.read_spss("GSS2022.sav")
gss2024 = pd.read_spss("GSS2024.sav")

print(gss2018["abany"].value_counts(dropna=False))
print(gss2018["abany"].value_counts(normalize=True))
print("2018:", "abany" in gss2018.columns)
print("2021:", "abany" in gss2021.columns)
print("2022:", "abany" in gss2022.columns)
print("2024:", "abany" in gss2024.columns)
print("\n2018")
print(gss2018["abany"].value_counts(normalize=True))

print("\n2021")
print(gss2021["abany"].value_counts(normalize=True))

print("\n2022")
print(gss2022["abany"].value_counts(normalize=True))

print("\n2024")
print(gss2024["abany"].value_counts(normalize=True))
# Combine abortion responses from all four GSS years
combined = pd.concat([
    gss2018[["abany"]].assign(year=2018),
    gss2021[["abany"]].assign(year=2021),
    gss2022[["abany"]].assign(year=2022),
    gss2024[["abany"]].assign(year=2024)
], ignore_index=True)

# Keep only valid yes/no responses
combined = combined[combined["abany"].isin(["yes", "no"])]

# Put columns in a clean order
combined = combined[["year", "abany"]]

# Save the cleaned dataset
combined.to_csv("GSS_Abortion_Clean.csv", index=False)

print("\nClean dataset created!")
print(combined.groupby(["year", "abany"]).size())
print("\nTotal valid responses:", len(combined))

# Calculate percentage of "yes" responses by year
yes_percent = combined.groupby("year")["abany"].apply(
    lambda x: (x == "yes").mean() * 100
)
print("\nYes percentage by year:")
print(yes_percent)
# Create line graph
plt.plot(yes_percent.index, yes_percent.values, marker="o")
plt.xlabel("Year")
plt.ylabel("Percentage of Yes Responses")
plt.title("Abortion Attitudes by Survey Year")
plt.ylim(0, 100)
for year, percent in yes_percent.items():
    plt.text(year, percent + 2, f"{percent:.1f}%", ha="center")
plt.savefig("Abortion_Attitudes_by_Year.png", dpi=300, bbox_inches="tight")
plt.show()
# Calculate yes/no percentages by year
response_percent = pd.crosstab(
    combined["year"],
    combined["abany"],
    normalize="index"
) * 100
print("\nYes/No percentages by year:")
print(response_percent)

# Create stacked bar chart
response_percent[["no", "yes"]].plot(kind="bar", stacked=True)
plt.xlabel("Year")
plt.ylabel("Percentage of Responses")
plt.title("Yes and No Responses by Survey Year")
plt.ylim(0, 100)
plt.xticks(rotation=0)
plt.legend(title="Response")
plt.savefig("Abortion_Responses_Stacked.png", dpi=300, bbox_inches="tight")
plt.show()