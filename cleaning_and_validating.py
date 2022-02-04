# -*- coding: utf-8 -*-
"""CLEANING AND VALIDATING.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A2Uw-sUxi6iu-OmeodPQaW5vRTfpMQwS

#**2 CLEANING AND VALIDATING**

##**2.1 HANDLING MISSING VALUES**
"""

# Plot the missing values
msno.matrix(df)

"""Matrix plot is a great tool to understand the presence and distribution of missing values in our data. As seen in the resultant plot, while there are no missing values in 'year' and 'region' columns, drink features ('wine', 'beer', 'vodka', 'champagne', and 'brandy') show a similar pattern where data is missing. I investigate this by grouping the same matrix plot based on region and year."""

# Plot the same matrix based on region and year
msno.matrix(df.sort_values(['region','year']))

"""The second matrix plot shows us the data is mostly missing as a whole in some regions and particular years. Let's create a pivot table to have a better understanding of missing values in the data."""

# Create a list of drink features
drinks= ['wine','beer','vodka','champagne','brandy']
nan_df = df[df.loc[:,drinks].isnull().any(axis=1)]
# Add missing values counter column to insepect better
nan_df['nan_count'] = nan_df.loc[:,drinks].isnull().sum(axis=1)
# Create pivot table to have all data in one look
nan_piv = nan_df.pivot_table(index='region', columns='year', 
                               values='nan_count', aggfunc='sum').fillna(0)

"""**Conclusion**:

*   We have missing values in four regions of Russia: *Chechen Republic, Republic of Crimea, Republic of Ingushetia, and Sevastopol*.

*   Missing values in "*Republic of Crimea*" and "*Sevastopol*" are due to [The annexation of these two regions by the Russian Federation](https://en.wikipedia.org/wiki/Annexation_of_Crimea_by_the_Russian_Federation) in 2014. Since then,
the data is present, but it is not enough. Thus I decide to remove these regions.

*   The "*Chechen Republic*" and "*Republic of Ingushetia*" are majority Muslim regions where there was a de facto ban on the sale of alcohol for a long time. In recent years, [the number of alcohol shops in these regions has reduced](https://www.reuters.com/article/us-russia-ingushetia-alcohol-idUSTRE7112Z820110202) due to the fear of attacks from local people. So I drop these two regions as well.


"""

# Removing any region with missing values
df = df[~df.region.isin(nan_piv.index.to_list())]

"""##**2.2 VALIDATING DATA**"""

# Install and load pandora to create schema
!pip install pandera
import pandera as pa

"""The DataFrameSchema class enables the specification of a schema that verifies the columns and index of a pandas DataFrame object. My schema assures that all of our columns have a proper datatype and, in some cases, are between specific scopes."""

# Create a schema to validate
schema = pa.DataFrameSchema({'year': pa.Column(pa.Int, pa.Check(lambda n: n.between(1998,2016))),
                             'region': pa.Column(pa.String),
                             'wine': pa.Column(pa.Float64, pa.Check.greater_than_or_equal_to(0)),
                             'beer': pa.Column(pa.Float64, pa.Check.greater_than_or_equal_to(0)),
                             'vodka': pa.Column(pa.Float64, pa.Check.greater_than_or_equal_to(0)),
                             'champagne': pa.Column(pa.Float64, pa.Check.greater_than_or_equal_to(0)),
                             'brandy': pa.Column(pa.Float64, pa.Check.greater_than_or_equal_to(0))})
schema.validate(df)

"""###**2.2.1 THE CASE WITH "TUVA REPUBLIC"**"""

# Summary statistics
df.describe().T

"""While checking summary statistics of our clean data, I have noticed there is/are regions where brandy consumption recorded as ZERO. I have to examine this."""

df[df['brandy'] == 0.0 ]

"""Apparently, there is no record for brandy consumption per capita in the Tuva Republic. I plot brandy consumption in this region through the years and compare it with average brandy sales in other parts of Russia."""

# Plot Tuva vs Russia brandy consumption
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(8, 5))
tuva = df[df['region'] == 'Tuva Republic']
brandy = df.groupby('year')['brandy'].mean()
sns.lineplot(x='year', y='brandy', data=tuva, label='Tuva Republic')
sns.lineplot(x='year', y=brandy, data=brandy, label='Russia')
plt.title('Per capita consumption of brandy in Russia')
plt.xticks(tuva.year, rotation=90)
plt.margins(y=0)

"""**Conclusion**:


*   Brandy consumption in the year before and after 2004 was 0.1 liter per capita in the *Tuva Republic* which can convince us that zero value in 2004 wasn't a data entry error.

*   Brandy is not very popular in Russia (maybe due to its cost). Consequently, values less than one liter per capita look normal.
"""