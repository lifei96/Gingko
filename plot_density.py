import seaborn as sns
from matplotlib import pyplot as plt
def plot_hist(data, hist=True, kde=False):
    fig = plt.figure()
    sns.distplot(data[0], hist = hist, kde = kde, label='Credible')
    sns.distplot(data[1], hist = hist, kde = kde, label='Fake')
    plt.show()
