
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

def fetch_data():
    """Fetch wine quality dataset."""
    print("Fetching data for EDA...")
    wine_quality = fetch_ucirepo(id=186)
    df = wine_quality.data.features.copy()
    df['quality'] = wine_quality.data.targets
    return df

def plot_histograms(df):
    """Plot histograms for all features."""
    print("Generating histograms...")
    df.hist(bins=20, figsize=(15, 10), color='#800020', grid=False)
    plt.tight_layout()
    plt.savefig('eda_histograms.png')
    plt.close()
    print("Saved eda_histograms.png")

def plot_correlation_matrix(df):
    """Plot correlation matrix heatmap."""
    print("Generating correlation matrix...")
    plt.figure(figsize=(12, 10))
    corr = df.corr()
    mask = correlation_matrix = corr # Just for naming
    sns.heatmap(corr, annot=True, cmap='RdBu_r', fmt=".2f", center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title("Correlation Matrix", fontsize=16)
    plt.tight_layout()
    plt.savefig('eda_correlation.png')
    plt.close()
    print("Saved eda_correlation.png")

def plot_quality_distribution(df):
    """Plot quality score distribution."""
    print("Generating quality distribution...")
    plt.figure(figsize=(8, 6))
    sns.countplot(x='quality', data=df, palette="Reds_r", hue='quality', legend=False)
    plt.title("Wine Quality Distribution", fontsize=16)
    plt.xlabel("Quality Score")
    plt.ylabel("Count")
    plt.savefig('eda_quality_dist.png')
    plt.close()
    print("Saved eda_quality_dist.png")

if __name__ == "__main__":
    try:
        df = fetch_data()
        plot_histograms(df)
        plot_correlation_matrix(df)
        plot_quality_distribution(df)
        print("EDA plots generated successfully.")
    except Exception as e:
        print(f"Error generating EDA plots: {e}")
