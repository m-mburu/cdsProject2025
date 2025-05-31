import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def plot_facet_metrics(
        df,
        id_vars=("size", "case"),
        facet_col="test_type",
        facet_row=None, 
        hue="tree",
        metric_pattern=None
):
    """
    Plot metrics for different test cases.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing columns:
            'size', 'case', and metrics columns
    
    id_vars : tuple of str
        Columns to keep when melting; default is ('size', 'case').
    
    facet_col : str
        The column name that will produce separate facets (subplots) by column. Default is 'test_type'.
    
    facet_row : str or None
        The column name that will produce separate facets (subplots) by row. Default is None.
    
    hue : str
        The column to use for color grouping. Default is 'case'.
    
    metric_pattern : dict or None
        If provided, a dictionary with 'prefix': ['metric1', 'metric2'...] to identify metrics columns
        If None, tries to use the standard pattern (tst_*, bst_*)
    """
    # Print columns for debugging
    print("DataFrame columns:", df.columns.tolist())
    
    # Determine which columns to melt (value variables)
    if metric_pattern:
        # Use provided patterns
        value_vars = []
        for prefix, metrics in metric_pattern.items():
            for metric in metrics:
                col_name = f"{prefix}_{metric}"
                if col_name in df.columns:
                    value_vars.append(col_name)
    else:
        # Use standard pattern or look for numeric columns
        # First try standard pattern
        pattern = re.compile(r'^(tst|bst)_')
        value_vars = [col for col in df.columns if pattern.match(col)]
        
        # If no standard pattern matches, use any numeric columns except id_vars
        if not value_vars:
            value_vars = [col for col in df.columns 
                         if col not in id_vars 
                         and df[col].dtype.kind in 'ifc']  # integer, float, complex
            print(f"Using numeric columns as metrics: {value_vars}")
    
    # Ensure we have columns to melt
    if not value_vars:
        raise ValueError("No metric columns found to plot")
        
    print("Value vars to melt:", value_vars)
    
    # Melt the DataFrame
    try:
        df_m = df.melt(id_vars=id_vars, value_vars=value_vars, 
                      var_name="metric", value_name="value")
        
        # Try to extract tree and test_type from metric column
        # This may fail if the column names don't follow expected pattern
        try:
            df_m = df_m.assign(
                tree=lambda d: d["metric"].str.extract(r'^(tst|bst|[a-z]+)'),
                test_type=lambda d: d["metric"].str.extract(r'^[a-z]+_(.*)$')
            )
        except Exception as e:
            # Create simple test_type if extraction fails
            print(f"Could not extract test_type from metrics: {e}")
            df_m["tree"] = "unknown"
            df_m["test_type"] = df_m["metric"]
        
        df_m = df_m.drop(columns="metric")
    except Exception as e:
        print(f"Error during melting: {e}")
        raise
    
    print("Melted DataFrame:\n", df_m.head())
    
    # Handle missing test_type values
    if df_m["test_type"].isna().any():
        print("Warning: Some test_type values are NaN. Using metric names instead.")
        df_m["test_type"] = df_m["metric"] if "metric" in df_m.columns else "unknown"
    
    # Create the facet plot - now with support for both row and column facets
    g = sns.relplot(
        data=df_m,
        x="size",
        y="value",
        col=facet_col, 
        row=facet_row, 
        hue=hue,
        kind="line", 
        errorbar=None,
        facet_kws={"sharey": False, "sharex": True},
        height=4, aspect=1.2
    )
    g.set_axis_labels("Number of Words", "Value (s / MB)")
    
    # Set titles differently based on whether we have row facets
    if facet_row:
        g.set_titles(row_template="{row_name}", col_template="{col_name}")
    else:
        g.set_titles("{col_name}")
        
    plt.tight_layout()
    
    return g

