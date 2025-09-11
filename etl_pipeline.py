#!/usr/bin/env python3
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Config
INPUT_GLOB = "./unzipped_folder/*"
OUTPUT_FILE = "transformed_data.csv"
LOG_FILE = "log_file.txt"

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} - {msg}\n")
    print(msg)

# --- Extract helpers ---
def extract_csv(fp):
    return pd.read_csv(fp)

def extract_json(fp):
    try:
        return pd.read_json(fp, lines=True)
    except ValueError:
        return pd.read_json(fp)

def extract_xml(fp):
    tree = ET.parse(fp)
    root = tree.getroot()
    rows = []
    for rec in root:
        row = {}
        for child in rec:
            row[child.tag] = child.text
        rows.append(row)
    return pd.DataFrame(rows)

# --- Normalize column names and map variants ---
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Lower-case key for matching
    mapping = {}
    for col in df.columns:
        key = col.strip().lower()
        if key in ("height", "height_in", "height(in)", "height_inches", "inches", "ht", "height_inches "):
            mapping[col] = "Height"
        elif key in ("weight", "weight_lbs", "weight_lb", "weight(pounds)", "lbs", "pounds", "wt"):
            mapping[col] = "Weight"
        else:
            mapping[col] = col.strip().title()
    return df.rename(columns=mapping)

# --- Master extract ---
def extract():
    log("Extraction started")
    files = glob.glob(INPUT_GLOB)
    if not files:
        log(f"No files found for pattern {INPUT_GLOB}")
        return pd.DataFrame()

    dfs = []
    for f in files:
        try:
            if f.lower().endswith(".csv"):
                df = extract_csv(f)
            elif f.lower().endswith(".json"):
                df = extract_json(f)
            elif f.lower().endswith(".xml"):
                df = extract_xml(f)
            else:
                log(f"Skipped (unsupported): {f}")
                continue

            df = normalize_columns(df)
            dfs.append(df)
            log(f"Extracted {len(df)} rows from {Path(f).name}")
        except Exception as e:
            log(f"Failed to read {f}: {e}")

    combined = pd.concat(dfs, ignore_index=True, sort=False) if dfs else pd.DataFrame()
    log("Extraction completed")
    log(f"Columns after extract: {combined.columns.tolist()}")
    return combined

# --- Transform ---
def transform(df: pd.DataFrame) -> pd.DataFrame:
    log("Transformation started")
    if df.empty:
        log("No data to transform")
        return df

    # Convert to numeric safely, coerce errors -> NaN
    if "Height" in df.columns:
        df["Height"] = pd.to_numeric(df["Height"], errors="coerce") * 0.0254  # inches -> meters
        log("Converted Height to meters")
    else:
        log("Height column not found; skipping height conversion")

    if "Weight" in df.columns:
        df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce") * 0.453592  # pounds -> kg
        log("Converted Weight to kg")
    else:
        log("Weight column not found; skipping weight conversion")

    log("Transformation completed")
    return df

# --- Load ---
def load(df: pd.DataFrame):
    log("Loading started")
    df.to_csv(OUTPUT_FILE, index=False)
    log(f"Saved transformed data to {OUTPUT_FILE}")
    log("Loading completed")

# --- ETL ---
def etl_process():
    log("ETL Job Started")
    df = extract()
    df = transform(df)
    load(df)
    log("ETL Job Completed")

if __name__ == "__main__":
    etl_process()


