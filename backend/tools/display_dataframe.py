import pandas as pd
import numpy as np
pd.set_option('display.float_format', lambda x: '%.2f' % x)

from collections.abc import Iterable


dtype_map = {
    'int64': 'Int64',
    'float64': 'Float64',
    'bool': 'boolean',
}

def is_iterable(obj):
    return isinstance(obj, Iterable)


def round_nested(value, decimal_precision):
    """Helper function to round numbers in nested structures"""
    if type(value) in [np.ndarray, np.array]:
        return value.round(decimal_precision)
    elif isinstance(value, float):
        return round(value, decimal_precision)
    return value


def truncate_value(value, array_max_length=50, string_max_length=5000):
    """Helper function to truncate values based on their type"""
    if isinstance(value, (list, tuple, np.ndarray)):
        if len(str(value)) <= array_max_length:
            return value
        # Convert all elements to strings for consistent display
        str_elements = [str(x) for x in value]
        truncated = []
        current_length = 0
        for elem in str_elements:
            if current_length + len(elem) + 5 > array_max_length:  # +5 for ", ..." 
                truncated.append('...')
                break
            truncated.append(elem)
            current_length += len(elem) + 2  # +2 for ", "
        return f"[{', '.join(truncated)}]"
    elif isinstance(value, str):
        if len(value) <= string_max_length:
            return value
        return value[:string_max_length-4] + "..."
    return value


def display_dataframe(df: pd.DataFrame, mode="markdown", display_rows: int = 20, decimal_precision: int = 4, index=False) -> str:
    # Create a copy to avoid modifying the original dataframe
    df = df.copy()
    
    original_shape = df.shape

    truncated_df = df.head(display_rows).reset_index(drop=True)
    if index:
        truncated_df = truncated_df.reset_index(names='')

    if original_shape[0] > display_rows:
        additional_row_index = min(display_rows, truncated_df.shape[0])
        additional_row = pd.DataFrame({col: ['...'] for col in truncated_df.columns}, index=[additional_row_index])
        truncated_df = pd.concat([truncated_df, additional_row])
    
    dtypes = truncated_df.dtypes
    for column in truncated_df.columns:
        truncated_df[column] = truncated_df[column].map(lambda x: round_nested(x, 4)) # First round the numbers
        truncated_df[column] = truncated_df[column].map(lambda x: truncate_value(x)) # Then truncate all values
    truncated_df = truncated_df.astype(dtypes.map(lambda x: dtype_map.get(str(x), str(x))))
    
    if mode == "markdown":
        df_string = truncated_df.to_markdown(index=False, floatfmt='')
        df_string += f"\n\n[{df.shape[0]} rows x {df.shape[1]} columns]"
    else:
        df_string = truncated_df.to_csv(index=False, sep='\t')
        df_string += f"\n\n[{df.shape[0]} rows x {df.shape[1]} columns]"

    return df_string
