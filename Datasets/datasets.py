import pandas as pd
#Datasets
df1 = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
df3 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

datasets = [df1,df2,df3]
dataset_names = ['Country_indicators', 'Iris_dataset', 'GDP_dataset']
dataset_dict = dict(zip(dataset_names,datasets))

