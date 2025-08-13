import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import zscore
import matplotlib.pyplot as plt

def plot_graphs(
    df,
    plot_type='scatter',
    x_col=None,
    y_col=None,
    title=None,
    xlabel=None,
    ylabel=None,
    log_scale=False,
    regression=False,
    alpha=0.5,
    figsize=(10, 6),
    line_color='red',
    cmap='blue',
    annot=True,
    aggfunc='mean',
    show_corr=False,
    remove_outliers=False,
    outlier_method='iqr',
    return_data=False,
    save_path=None,
    custom_plot_func=None 
):
    sns.set(style="whitegrid")
    data = df.copy()


    # Outlier Removal
    if remove_outliers:
        cols_to_check = [x_col] if plot_type in ['hist', 'histogram'] else [x_col, y_col]
        if all(col in data.columns for col in cols_to_check):
            if outlier_method == 'iqr':
                for col in cols_to_check:
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
            elif outlier_method == 'zscore':
                z_scores = np.abs(zscore(data[cols_to_check].dropna()))
                data = data[(z_scores < 3).all(axis=1)]


    # Start Plot
    plt.figure(figsize=figsize)

    if plot_type == 'scatter':
        if regression:
            sns.regplot(
                data=data,
                x=x_col,
                y=y_col,
                scatter_kws={'alpha': alpha},
                line_kws={'color': line_color},
                ci=None
            )
        else:
            sns.scatterplot(
                data=data,
                x=x_col,
                y=y_col,
                alpha=alpha
            )
        if log_scale:
            plt.xscale('log')
            plt.yscale('log')

    elif plot_type == 'line':
        plt.plot(data[x_col], data[y_col], marker='o', color=line_color, alpha=alpha)
        if log_scale:
            plt.xscale('log')
            plt.yscale('log')

    elif plot_type == 'boxplot':
        sns.boxplot(data=data, x=x_col, y=y_col)

    elif plot_type == 'bar':
        sns.barplot(data=data, x=x_col, y=y_col, ci=None)
        plt.xticks(rotation=45)

    elif plot_type in ['hist', 'histogram']:
        if x_col:
            sns.histplot(data=data, x=x_col, bins=50, kde=True)
            if log_scale:
                plt.xscale('log')
        else:
            raise ValueError("x_col must be specified for histogram.")

    elif plot_type == 'heatmap':
        if x_col and y_col:
            pivot_table = data.pivot_table(index=y_col, columns=x_col, aggfunc=aggfunc)
            sns.heatmap(pivot_table, annot=annot, cmap=cmap)
        else:
            raise ValueError("x_col and y_col must be specified for heatmap.")

    elif plot_type == 'figure':  # <--- New case
        if custom_plot_func is not None and callable(custom_plot_func):
            custom_plot_func(data)
        else:
            raise ValueError("For plot_type='figure', you must provide a callable in custom_plot_func.")

    else:
        raise ValueError(f"Unsupported plot_type: {plot_type}")


    # Labels & Titles
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or ("Frequency" if plot_type in ['hist', 'histogram'] else y_col))
    plt.title(title or f"{plot_type.title()} Plot")


    # Show Correlation on Plot
    if show_corr and x_col and y_col:
        corr = data[[x_col, y_col]].corr().iloc[0, 1]
        plt.text(
            0.05,
            0.95,
            f"Pearson r = {corr:.2f}",
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
        )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    plt.show()

    if return_data:
        return data
