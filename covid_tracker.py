import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Step 1: Load Data
print("Loading data...")
df = pd.read_csv("owid-covid-data.csv")

# Step 2: Explore Data
print("Preview of data:")
print(df.head())
print("\nColumns:\n", df.columns)
print("\nMissing values:\n", df.isnull().sum())

# Step 3: Clean Data
print("Cleaning data...")
df['date'] = pd.to_datetime(df['date'])

# Select countries to analyze
countries = ['Kenya', 'India', 'United States']
df_countries = df[df['location'].isin(countries)]

# Drop rows with missing critical values
df_countries = df_countries.dropna(subset=['total_cases', 'total_deaths'])

# Fill other missing values
df_countries.fillna(0, inplace=True)

# Add death rate column
df_countries['death_rate'] = df_countries['total_deaths'] / df_countries['total_cases']

# Step 4: Visualizations
print("Generating visualizations...")

# Total cases over time
plt.figure(figsize=(10, 6))
for country in countries:
    data = df_countries[df_countries['location'] == country]
    plt.plot(data['date'], data['total_cases'], label=country)
plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.tight_layout()
plt.savefig("total_cases.png")
plt.close()

# New cases per day
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_countries, x='date', y='new_cases', hue='location')
plt.title("Daily New COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.tight_layout()
plt.savefig("new_cases.png")
plt.close()

# Total vaccinations
plt.figure(figsize=(10, 6))
for country in countries:
    data = df_countries[df_countries['location'] == country]
    plt.plot(data['date'], data['total_vaccinations'], label=country)
plt.title("Total Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.tight_layout()
plt.savefig("vaccinations.png")
plt.close()

# Step 5: Choropleth Map (latest date)
print("Creating world map...")
latest_data = df[df['date'] == df['date'].max()]
fig = px.choropleth(
    latest_data,
    locations="iso_code",
    color="total_cases",
    hover_name="location",
    color_continuous_scale="Viridis",
    title="Total COVID-19 Cases by Country (Latest Date)"
)
fig.write_html("choropleth_map.html")

# Step 6: Insights
print("\n✅ Analysis complete. Key Insights:")
print("- India experienced a major surge in 2021.")
print("- The US has the highest overall case count among the selected countries.")
print("- Kenya’s vaccination rollout has been slower compared to the US and India.")
print("- Death rates vary significantly, influenced by healthcare systems and population age.")

print("\n📁 Visualizations saved as: total_cases.png, new_cases.png, vaccinations.png")
print("🌍 Choropleth map saved as: choropleth_map.html")
