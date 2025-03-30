# Script by Larysa Dorokhova

import csv
import pandas as pd                        # software library written for data manipulation and analysis, for manipulating numerical tables and time series
import seaborn as sns                      # visualization library based on matplotlib
import matplotlib.pyplot as plt            # library for data visualization with two-dimensional and three-dimensional graphics

# declaring a dictionary to store a selection of data from a table
data = {
    'country': [],
    'region': [],
    'score': [],
    'gdp': []
}

# reading the necessary columns from a csv file and filling in the dictionary with them
try:
    with open('../data/data-2019.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")      # reading a csv file with a comma separator
        next(csvfile)                                    # skipping a row of table headings
        
        for row in reader:
            try:
                data['country'].append(row[0])           # where 0 is an indexes of Country columns
                data['region'].append(row[1])            # where 1 is an indexes of Region columns
                data['score'].append(float(row[3]))      # where 3 is an indexes of Score columns
                data['gdp'].append(float(row[4]))        # where 4 is an indexes of GDP columns
            except ValueError:
                print(f"Error converting data in a row: {row}")
except FileNotFoundError:
    print("The data-2019.csv file was not found.")
    exit()
except IOError:
    print("Error when opening the file.")
    exit()

# converting a dictionary to DataFrame - two-dimensional, size-mutable, potentially heterogeneous tabular data
df = pd.DataFrame(data)

# Grouping the data by region and finding the average value of the happiness index
try:
    average_happiness_score_by_region = df.groupby('region')['score'].mean()

    # Output of the grouping results and the average score for each region
    print('\nThe average happiness score for each region:')
    print(average_happiness_score_by_region)
except KeyError as e:
    print(f"Data access error: {e}")

# Sort by GDP in descending order
try:
    df_sorted = df.sort_values(by='gdp', ascending=False)

    # The 10 countries with the largest GDP and the output of the results
    top_10_gdp = df_sorted.head(10)
    print("\nThe 10 countries with the largest GDP:")
    print(top_10_gdp[['country', 'gdp']])

    # The 10 countries with the lowest GDP and the output of the results
    bottom_10_gdp = df_sorted.tail(10)
    print("\nThe 10 countries with the lowest GDP:")
    print(bottom_10_gdp[['country', 'gdp']])
except KeyError as e:
    print(f"Sorting error: {e}")

# Function for calculating Spearman correlation
def spearman_coefficient_correlation(x, y):
    try:
        # Converting the data to rank data
        rank_x = pd.Series(x).rank()
        rank_y = pd.Series(y).rank()
        
        # Calculating the difference between the ranks
        d = rank_x - rank_y
        d_squared = d ** 2
    
        # Number of elements
        n = len(x)
        if n < 2:
            raise ValueError("There is not enough data to calculate the correlation.")
         
        # The formula for Spearman's correlation coefficient
        scc = 1 - (6 * d_squared.sum()) / (n * (n**2 - 1))
    
        return scc
    except ZeroDivisionError:
        print("Error: division by zero.")
        return None
    except TypeError:
        print("Error: invalid data type.")
        return None
        

# Calculating the Spearman correlation between GDP and Score
correlation = spearman_coefficient_correlation(df['gdp'], df['score'])

# Output of Spearman correlation coefficient result
if correlation is not None:
    print(f"\nSpearman Correlation Coefficient between GDP and Score: {correlation}")

# Plotting a dot graph and saving it to a png file
try:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='gdp', y='score', data=df)
    plt.title('Dot graph: GDP vs Score')
    plt.xlabel('GDP')
    plt.ylabel('Score')
    plt.savefig('../data/gdp_vs_score.png')
    print("The graph has been successfully saved to the data/gdp_vs_score.png file")
except Exception as e:
    print(f"Error in plotting: {e}")
