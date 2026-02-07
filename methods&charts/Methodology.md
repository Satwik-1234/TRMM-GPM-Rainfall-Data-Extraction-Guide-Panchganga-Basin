# 🧪 Methodology  
## Taluka-wise TRMM/GPM Rainfall Extraction for Panchganga Basin (2006–2025)

---

## 1. Study Area

The study is conducted for the **Panchganga River Basin** located in **Kolhapur district, Maharashtra, India**. The basin spans across **12 administrative talukas**, covering heterogeneous terrain that includes the **Western Ghats escarpment** and eastern lowland plains.

This spatial variability necessitates a **taluka-wise rainfall assessment** to support hydrological modeling, flood analysis, and water resource planning.

**Geographic extent:**
- Latitude: ~15.9°N to 16.9°N  
- Longitude: ~73.7°E to 74.5°E  
- Climate: Tropical monsoon  
- Dominant rainfall source: Southwest monsoon (June–September)

---

## 2. Rainfall Dataset Selection

### 2.1 GPM IMERG Final Run (Version 07B)

Rainfall data were sourced from the **GPM IMERG Final Run (V07B)** dataset, which provides a **continuous, gauge-corrected, multi-satellite precipitation product**.

**Key reasons for selection:**
- Integrates **TRMM-era (2000–2015)** and **GPM-era (2015–present)** data
- Ensures long-term temporal consistency
- Bias-adjusted using global rain gauge networks
- Widely accepted in peer-reviewed hydrological studies

**Dataset characteristics:**
- Spatial resolution: **0.1° × 0.1°**
- Temporal resolution: **30-minute**
- Study period used: **January 2006 – December 2025**

---

## 3. Administrative Boundary Processing

### 3.1 Taluka Boundary Preparation

- Taluka-level administrative boundaries for Kolhapur district were used as vector polygons.
- Boundaries were validated for geometry errors.
- Only taluka areas intersecting the **Panchganga basin boundary** were retained.

### 3.2 Basin–Taluka Overlay

Each taluka polygon was spatially intersected with the basin boundary to ensure rainfall extraction strictly represents the hydrologically relevant area.

---

## 4. Data Extraction Platform

### 4.1 Google Earth Engine (GEE)

Rainfall extraction was carried out using **Google Earth Engine**, leveraging its cloud-based geospatial processing capabilities and native access to IMERG datasets.

**Advantages of GEE:**
- No need for bulk data downloads
- Efficient handling of multi-decadal datasets
- Fully reproducible workflows
- Suitable for basin-scale hydrological applications

---

## 5. Temporal Aggregation of Rainfall

IMERG provides precipitation at a **30-minute interval**. Temporal aggregation was performed as follows:

### 5.1 Daily Rainfall

Daily rainfall was computed by summing all half-hourly values within a day:

$$
P_d = \sum_{i=1}^{48} P_i
$$

where:  
- \( P_d \) = daily rainfall (mm/day)  
- \( P_i \) = half-hourly precipitation value  

---

### 5.2 Monthly Rainfall

Monthly rainfall was obtained by aggregating daily rainfall totals:

$$
P_m = \sum_{d=1}^{n} P_d
$$

where:  
- \( P_m \) = monthly rainfall (mm/month)  
- \( n \) = number of days in a month  

---

## 6. Spatial Aggregation Method

Due to partial overlap between IMERG grid cells and taluka boundaries, **area-weighted averaging** was applied.

### 6.1 Taluka-wise Rainfall Estimation

$$
P_{taluka} = \frac{\sum (P_{cell} \times A_{cell})}{\sum A_{cell}}
$$

where:  
- \( P_{cell} \) = rainfall in an IMERG grid cell  
- \( A_{cell} \) = area of the grid cell within the taluka boundary  

This method minimizes spatial bias and ensures representative rainfall estimation.

---

## 7. Data Quality Control

The extracted rainfall time series were subjected to multiple quality checks:

- Detection of missing or discontinuous records
- Identification of extreme outliers
- Visual inspection of time-series consistency
- Verification of spatial rainfall gradients with known orographic patterns
- Cross-check with regional climatological expectations

---

## 8. Statistical Analysis

For each taluka, the following rainfall statistics were derived:

- Mean annual rainfall
- Monthly climatology
- Seasonal rainfall contribution
- Interannual variability
- Identification of extreme rainfall years
- Long-term rainfall trends

Talukas were further categorized into **high**, **moderate**, and **low rainfall zones** based on climatological means.

---

## 9. Model-Ready Data Preparation

Rainfall datasets were formatted for direct use in hydrological models:

- **HEC-HMS** continuous simulation format
- **SWAT** weather input format
- Generic CSV format for custom modeling workflows

Each taluka’s rainfall series was exported independently to enable sub-basin level calibration.

---

## 10. Rainfall–Runoff Modeling Framework

The processed rainfall data support continuous hydrological modeling using the following framework:

1. Taluka-wise rainfall input (IMERG)
2. Evapotranspiration input (NASA POWER / IMD)
3. Basin and sub-basin delineation using DEM
4. Parameter calibration using observed discharge
5. Validation using split-sample approach:
   - Calibration: 2006–2015
   - Validation: 2016–2025

---

## 11. Uncertainty and Limitations

- Satellite rainfall may underestimate intense orographic precipitation
- Coarse grid resolution may smooth localized convective events
- Minor inconsistencies may exist during the TRMM–GPM transition
- Ground gauge validation is recommended where available

Despite these limitations, IMERG Final Run is suitable for basin-scale hydrological studies.

---

## 12. Reproducibility

- All datasets are open-access
- Scripts are fully reproducible
- Workflow adheres to open science and peer-reviewed standards

---

## 📌 Summary

This methodology provides a **robust, reproducible, and model-ready framework** for extracting and analyzing long-term taluka-wise rainfall data using TRMM/GPM IMERG for the Panchganga River Basin.

---
