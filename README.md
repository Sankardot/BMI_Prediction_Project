# BMI Prediction Project

## Overview
This project performs ETL (Extract, Transform, Load) on health data and visualizes BMI (Body Mass Index) trends across ages and genders.

## Folder Structure
- `data/` : Contains raw and processed CSV files
- `src/` : Python scripts for ETL and visualization
- `visuals/` : Generated plots
- `notebooks/` : Optional Jupyter notebooks

## Scripts
- `etl.py` : Cleans and processes raw data
- `visualize.py` : Generates plots for BMI distribution and Age vs BMI

## How to Run
```bash
# Install requirements
pip install -r requirements.txt

# Run ETL
python src/etl.py

# Run Visualization
python src/visualize.py
