import json
from unstructured.partition.pdf import partition_pdf
import pandas as pd

def extract_tables_from_pdf(filename, strategy='hi_res'):
    """
    Extracts all tables from the given PDF file.

    Args:
        filename (str): Path to the PDF file.
        strategy (str): Strategy for table extraction ('hi_res' or other supported strategies).

    Returns:
        Tuple[List[pd.DataFrame], List[str]]: A tuple containing a list of DataFrames for each table 
        and a list of HTML representations of the tables.
    """
    elements = partition_pdf(
        filename=filename,
        infer_table_structure=True,
        strategy=strategy,
    )

    # Filter out all elements categorized as "Table"
    tables = [el for el in elements if el.category == "Table"]
    
    if not tables:
        print("No tables found in the PDF.")
        return [], []

    # Extract HTML from each table's metadata and convert to DataFrame
    tables_html = [table.metadata.text_as_html for table in tables]
    dfs = []
    for idx, html in enumerate(tables_html, start=1):
        try:
            # pd.read_html returns a list of DataFrames; take the first one
            df = pd.read_html(html)[0]
            dfs.append(df)
            print(f"Table {idx} extracted successfully.")
        except ValueError as ve:
            print(f"Failed to parse HTML for Table {idx}: {ve}")
            continue

    return dfs, tables_html
