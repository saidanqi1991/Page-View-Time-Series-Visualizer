import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import calendar 

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=True)

# Clean data
quantile_low = df.index[int(len(df)*0.025)]
quantile_high = df.index[int(len(df)*0.975)]
df = df.loc[(df.index > quantile_low) & (df.index < quantile_high)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['value'])
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().groupby([df.index.year, df.index.month]).mean()
    df_bar.index.names=['Years', 'Months']
    # Draw bar plot
    df_bar = df_bar.reset_index()
    df_bar = df_bar.pivot(index='Years', columns='Months', values='value')
    df_bar.columns = [calendar.month_name[i] for i in df_bar.columns]
    ax = df_bar.plot(kind='bar', figsize=(12,8))
    ax.set_ylabel('Average Page Views')
    fig = ax.get_figure()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig, ax=plt.subplots(nrows=1, ncols=2, figsize=(15,8))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_yticks(range(0, 200001, 20000))

    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], order=month_order)
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_yticks(range(0, 200001, 20000))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
