"""
Data cleaning pipeline for the Global Retail Intelligence Engine.
- Removes Internal_Notes (sensitive).
- Standardizes country and category.
- Builds a searchable text field from Item_Name + Technical_Specs.
- Saves to data/processed/products_clean.csv
"""
import pandas as pd
from pathlib import Path


def standardize_country(s: str) -> str:
    """Standardize country names."""
    if pd.isna(s):
        return ""
    return str(s).strip()


def standardize_category(s: str) -> str:
    """Standardize category (title case, strip)."""
    if pd.isna(s):
        return ""
    return str(s).strip().title()


def main():
    base = Path(__file__).resolve().parent.parent.parent
    raw_path = base / "data" / "raw" / "products_raw.csv"
    processed_dir = base / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / "products_clean.csv"

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Raw data not found: {raw_path}. Run scripts/generate_retail_dataset.py first."
        )

    df = pd.read_csv(raw_path)

    # 1. Remove Internal_Notes
    if "Internal_Notes" in df.columns:
        df = df.drop(columns=["Internal_Notes"])

    # 2. Standardize country and category
    df["Country"] = df["Country"].apply(standardize_country)
    df["Category"] = df["Category"].apply(standardize_category)

    # 3. Searchable text field for retrieval
    df["searchable_text"] = (
        df["Item_Name"].fillna("").astype(str) + " " +
        df["Technical_Specs"].fillna("").astype(str)
    ).str.strip()

    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Cleaned {len(df)} rows -> {out_path}")


if __name__ == "__main__":
    main()
