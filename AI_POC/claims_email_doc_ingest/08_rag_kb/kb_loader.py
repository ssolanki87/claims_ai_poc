# RAG Knowledge Base Loader
import pandas as pd
from typing import List

def load_kb(path: str) -> pd.DataFrame:
    """Load knowledge base from Delta table or CSV"""
    if path.endswith('.delta'):
        # Placeholder: use Delta Lake API
        return pd.DataFrame()  # Replace with actual Delta read
    else:
        return pd.read_csv(path)

def search_kb(df: pd.DataFrame, query: str) -> List[str]:
    """Simple keyword search in KB"""
    return df[df['text'].str.contains(query, case=False)]['text'].tolist()
