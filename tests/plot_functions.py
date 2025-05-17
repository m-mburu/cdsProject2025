import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_facet_metrics(
        df,
        id_vars=("size", "scenario"),
        facet_col="test_type",           # <— default changed!
        hue="scenario",
        #style="tree",                    # distinguish TST vs B-tree
        ci=None,                         # turn off opaque CI band
):
    """
    Plot a facet grid of metrics from a DataFrame.
    The DataFrame should have a column for each metric, and the
    columns should be named in a way that can be extracted by
    the `extract` method.
    :param df: DataFrame with metrics
    :param id_vars: Columns to use as id_vars in melt
    :param facet_col: Column to use for facetting
    :param hue: Column to use for coloring
    :param ci: Confidence interval to use for error bars
    """
    df_m = (
        df.melt(id_vars=id_vars, var_name="metric", value_name="value")
          .assign(tree=lambda d: d["metric"].str.extract(r'^(tst|bst)'))
          .assign(test_type=lambda d: d["metric"].str.extract(r'^[a-z]+_(.*)$'))
          .drop(columns="metric")
    )

    g = sns.relplot(
        data=df_m,
        x="size", y="value",
        col=facet_col, hue=hue,
        kind="line", errorbar=None if ci is None else ci,
        facet_kws={"sharey": False, "sharex": True},
        height=4, aspect=1.2
    )
    g.set_axis_labels("Number of Words", "Value (s   /   MB)")
    g.set_titles("{col_name}")
    #g._legend.set_title(hue)
    plt.tight_layout()
