
import io
from typing import List, Tuple, Dict
import pandas as pd

MAX_CELLS = 200_000       # guardrail on size
MAX_BYTES = 5_000_000     # ~5 MB worth of raw CSV text

def load_excels_to_frames(uploaded_files) -> Dict[str, pd.DataFrame]:
    """
    Reads multiple Excel files (all sheets). Returns dict key "filename::sheetname"
    """
    dfs = {}
    for f in uploaded_files:
        try:
            xls = pd.ExcelFile(f)
            for sheet in xls.sheet_names:
                df = xls.parse(sheet)
                key = f"{getattr(f,'name','uploaded') }::{sheet}"
                dfs[key] = df
        except Exception as e:
            raise RuntimeError(f"Failed to read {getattr(f,'name','uploaded')}: {e}")
    return dfs

def frames_to_compact_text(dfs: Dict[str, pd.DataFrame], max_rows_per_sheet: int = 2000) -> Tuple[str, int, int]:
    """
    Turn DataFrames to a compact text suitable for LLM context.
    Returns (text, total_cells, total_bytes)
    """
    parts = []
    total_cells = 0
    total_bytes = 0
    for name, df in dfs.items():
        # Basic info
        total_cells += int(df.shape[0]) * int(df.shape[1])
        head = df.head(max_rows_per_sheet)
        csv_buf = io.StringIO()
        head.to_csv(csv_buf, index=False)
        csv_text = csv_buf.getvalue()
        total_bytes += len(csv_text.encode("utf-8"))
        parts.append(f"### SHEET: {name}\n{csv_text}\n")
    return "\n".join(parts), total_cells, total_bytes

def technical_overflow_message(total_cells: int, total_bytes: int) -> str:
    return (
        "Request exceeds in-app processing limits.\n\n"
        f"- Observed size: ~{total_cells:,} cells; ~{total_bytes/1_000_000:.2f} MB serialized.\n"
        f"- Limits: {MAX_CELLS:,} cells OR {MAX_BYTES/1_000_000:.2f} MB.\n\n"
        "To continue: reduce row count, select fewer sheets, or summarize columns. "
        "You can also switch to a model that supports tool-based chunking outside the context window."
    )

