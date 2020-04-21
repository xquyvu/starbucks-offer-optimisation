import matplotlib.pyplot as plt
import seaborn as sns


def plot_feature_distribution(series, bins=20):
    fig = plt.figure(figsize=(15, 5))
    fig.add_subplot(1, 2, 1)
    plt.hist(series, bins=bins, density=True, cumulative=True)
    plt.title('{} distribution (culmulative)'.format(series.name))

    fig.add_subplot(1, 2, 2)
    plt.hist(series, bins=bins, density=True)
    plt.title('{} distribution'.format(series.name))

    plt.show()


def get_category_distribution(series):
    value_count = series.value_counts()
    value_count.plot(kind='bar')
    plt.show()

    print(value_count)


def reg_plot(x, y, data, **kwargs):
    plt.figure(figsize=(15, 7))
    sns.regplot(x, y, data=data, **kwargs)
    plt.show()
