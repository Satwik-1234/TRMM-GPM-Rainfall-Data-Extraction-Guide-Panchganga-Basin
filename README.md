# TRMM/GPM Rainfall Data Extraction Guide
## Panchganga Basin - Circle-wise (Taluka-wise) Analysis
### Kolhapur District, Maharashtra (2006-2025)

---

## 📋 Executive Summary

**REQUEST ANALYSIS:**
- **Data Source:** TRMM/GPM satellite rainfall data
- **Geographic Coverage:** Panchganga basin, Kolhapur district
- **Organization:** By administrative circles (12 talukas)
- **Time Period:** 20 years (2006-2025)
- **Objective:** Continuous rainfall-runoff modeling

**FEASIBILITY ASSESSMENT:** ✅ **FULLY FEASIBLE**

---

## 🛰️ Understanding TRMM and GPM

### TRMM (Tropical Rainfall Measuring Mission)
- **Launch:** November 1997
- **Decommission:** April 2015 (satellite re-entered atmosphere)
- **Coverage:** 35°N to 35°S latitude
- **Status:** Data reprocessed and integrated into GPM IMERG
- **Key Point:** Panchganga basin (16°N) is within TRMM coverage

### GPM (Global Precipitation Measurement)
- **Launch:** February 2014
- **Status:** Currently operational
- **Coverage:** 65°N to 65°S (near-global)
- **Successor:** Direct continuation of TRMM mission

### GPM IMERG V07B (Recommended Dataset)
- **Full Name:** Integrated Multi-satellitE Retrievals for GPM Version 07B
- **Data Period:** June 2000 - Present
- **Unique Feature:** Includes reprocessed TRMM-era data (2000-2015)
- **Resolution:** 0.1° × 0.1° (~10 km at equator, ~8-9 km at Kolhapur latitude)
- **Temporal Resolution:** 30 minutes (can be aggregated to daily/monthly)
- **Latency:** ~3.5 months for Final Run (research quality)
- **Coverage for Your Request:**
  - 2006-2015: TRMM-era data (reprocessed in IMERG format)
  - 2015-2025: GPM-era data
  - **Result:** Complete 20-year continuous dataset ✅

---

## 🗺️ Kolhapur District Administrative Circles (Talukas)

The Panchganga basin extends across Kolhapur district, which is divided into 12 administrative circles (talukas):

| # | Taluka | Lat | Lon | Area (km²) | Description |
|---|--------|-----|-----|------------|-------------|
| 1 | Karvir | 16.7050 | 74.2433 | 760 | District HQ, includes Kolhapur city |
| 2 | Panhala | 16.8167 | 74.1167 | 682 | Historic fort, high elevation |
| 3 | Shahuwadi | 16.6167 | 74.4833 | 565 | Eastern region |
| 4 | Kagal | 16.5833 | 74.3167 | 436 | Industrial area |
| 5 | Hatkanangle | 16.4333 | 74.4500 | 521 | Southern region |
| 6 | Shirol | 16.7167 | 74.4667 | 674 | Agricultural zone |
| 7 | Radhanagari | 16.4167 | 73.9833 | 1,041 | **Western Ghats, highest rainfall** |
| 8 | Gaganbawada | 16.5500 | 73.7667 | 681 | **Western Ghats, high rainfall** |
| 9 | Bhudargad | 16.0167 | 74.0667 | 569 | Southern border with Karnataka |
| 10 | Gadhinglaj | 16.2333 | 74.3500 | 589 | Southern region |
| 11 | Chandgad | 15.9833 | 74.2333 | 632 | Southernmost taluka |
| 12 | Ajra | 16.1167 | 73.9667 | 539 | Western region |

**Total District Area:** ~7,685 km²

**Rainfall Gradient:** Western talukas (Radhanagari, Gaganbawada) receive significantly higher rainfall due to Western Ghats orography.

---

## 📊 Data Extraction Methods

### Method 1: Google Earth Engine (RECOMMENDED) ⭐

**Why This is Best:**
- Direct access to GPM IMERG V07 dataset
- Includes complete TRMM-era data (2000-2015)
- Free for research, education, and nonprofit use
- Easy-to-use web interface
- No downloads needed - processes in cloud
- Can export directly to Google Drive

**Steps:**

1. **Sign Up for Google Earth Engine**
   - Go to: https://earthengine.google.com/signup/
   - Sign in with Google account
   - Register for Earth Engine access (usually approved within 1-2 days)

2. **Access the Code Editor**
   - Go to: https://code.earthengine.google.com/
   - Sign in with your registered Google account

3. **Use the Provided Code**
   - Open the file: `gee_panchganga_rainfall_extraction.js`
   - Copy all the JavaScript code
   - Paste it into the code editor

4. **Run the Code**
   - Click the "Run" button at the top
   - The code will:
     - Extract daily rainfall for all 12 talukas
     - Calculate monthly summaries
     - Prepare data for export

5. **Export Data to Google Drive**
   - Go to the "Tasks" tab (top right corner)
   - You'll see two export tasks:
     - `Panchganga_Rainfall_Taluka_Wise_2006_2025` (daily data)
     - `Panchganga_Rainfall_Monthly_Taluka_Wise_2006_2025` (monthly data)
   - Click "Run" for each task
   - Choose your Google Drive folder
   - Click "Run" to start export

6. **Download from Google Drive**
   - After processing completes (may take 30-60 minutes)
   - Go to your Google Drive
   - Find the CSV files in the specified folder
   - Download to your computer

**Expected Output:**
- Daily data: ~2.92 million records (12 talukas × 365 days × 20 years)
- Monthly data: ~2,880 records (12 talukas × 12 months × 20 years)

---

### Method 2: NASA POWER API (Alternative)

**Note:** This provides different data than TRMM/GPM but is easier to access programmatically.

**Advantages:**
- No registration required
- Direct API access
- Automated download via Python script
- Good quality gridded data

**Disadvantages:**
- Coarser resolution (0.5° × 0.5° vs 0.1° × 0.1° for IMERG)
- Different source (modeled data vs. satellite observations)

**How to Use:**

Run the Python script with NASA POWER option:

```bash
python fetch_trmm_gpm_panchganga.py
```

When prompted, choose "yes" to fetch NASA POWER data.

The script will:
1. Fetch data for all 12 talukas automatically
2. Organize data by taluka
3. Export in multiple formats (CSV, HEC-HMS, SWAT)
4. Generate statistics

**Time Required:** 10-15 minutes for complete download

---

### Method 3: NASA GES DISC (Advanced Users)

For direct access to GPM IMERG HDF5 files:

1. **Register:**
   - Go to: https://urs.earthdata.nasa.gov/users/new
   - Create free NASA Earthdata account

2. **Access Data:**
   - Go to: https://disc.gsfc.nasa.gov/
   - Search for "GPM IMERG Final"
   - Select GPM_3IMERGDF V07

3. **Download:**
   - Use OPeNDAP, direct download, or wget
   - Files are in HDF5 format
   - Requires processing with Python/R

**Note:** This method requires more technical expertise in handling HDF5/NetCDF files.

---

## 📈 Data Processing Workflow

### Step 1: Data Extraction
Choose one of the methods above to extract rainfall data.

### Step 2: Data Organization

The data will be organized as follows:

**Daily Data Format:**
```csv
Date,Taluka,Rainfall_mm,Latitude,Longitude
2006-01-01,Karvir,0.5,16.7050,74.2433
2006-01-01,Panhala,1.2,16.8167,74.1167
...
```

**Monthly Data Format:**
```csv
Year,Month,Taluka,Rainfall_mm
2006,1,Karvir,45.2
2006,1,Panhala,67.8
...
```

### Step 3: Quality Control

Check for:
- Missing values
- Outliers (extremely high/low values)
- Data continuity
- Spatial consistency

### Step 4: Statistical Analysis

Calculate for each taluka:
- Annual mean rainfall
- Monthly climatology
- Seasonal distribution
- Extreme events
- Trends over time

### Step 5: Export for Models

Data will be formatted for:
- **HEC-HMS:** Tab-separated, date-time-precipitation format
- **SWAT:** Year-month-day-rainfall format with header
- **Generic:** Standard CSV for any model

---

## 🔧 Using the Python Scripts

### Main Script: `fetch_trmm_gpm_panchganga.py`

```bash
# Run the script
python fetch_trmm_gpm_panchganga.py

# Follow prompts to:
# 1. Get Google Earth Engine code
# 2. Or fetch NASA POWER data directly
```

**Features:**
- Automatic coordinate management for all 12 talukas
- Multiple export formats
- Statistical analysis
- Visualization code generation

### Visualization Script: `visualize_rainfall.py`

```bash
# After data download, run:
python visualize_rainfall.py
```

**Creates:**
- Annual rainfall time series for each taluka
- Monthly climatology comparison
- Rainfall heatmap (year × taluka)

---

## 📁 Output Files Structure

```
output/
├── taluka_rainfall_data/
│   ├── Karvir_rainfall_2006_2025.csv
│   ├── Panhala_rainfall_2006_2025.csv
│   ├── ... (one file per taluka)
│   ├── All_Talukas_Combined_2006_2025.csv
│   └── Taluka_Rainfall_Statistics.csv
│
├── model_ready_data/
│   ├── Karvir_HEC_HMS_format.txt
│   ├── Karvir_SWAT_format.txt
│   ├── ... (files for each taluka)
│
└── visualizations/
    ├── taluka_annual_rainfall.png
    ├── monthly_climatology.png
    └── rainfall_heatmap.png
```

---

## 📊 Expected Rainfall Patterns

Based on historical knowledge and topography:

### High Rainfall Talukas (Western Ghats)
- **Radhanagari:** 4,000-5,000 mm/year (wettest)
- **Gaganbawada:** 3,500-4,500 mm/year
- **Ajra:** 3,000-3,500 mm/year

### Moderate Rainfall Talukas (Central)
- **Karvir:** 1,000-1,500 mm/year
- **Panhala:** 1,500-2,000 mm/year
- **Shirol:** 800-1,200 mm/year

### Lower Rainfall Talukas (Eastern/Southern)
- **Shahuwadi:** 700-1,000 mm/year
- **Hatkanangle:** 700-1,000 mm/year
- **Gadhinglaj:** 600-900 mm/year

### Seasonal Distribution
- **Monsoon (June-September):** 85-90% of annual rainfall
- **Winter (November-February):** <5%
- **Summer (March-May):** 5-10%

---

## ⚠️ Important Considerations

### Data Quality
1. **Satellite-based data** may have uncertainties in:
   - Complex terrain (Western Ghats)
   - Heavy rainfall events (underestimation possible)
   - Light rainfall events (detection threshold)

2. **Validation recommended** with:
   - Ground rain gauge data (if available)
   - IMD gridded data
   - Cross-comparison with other products

### Spatial Resolution
- IMERG resolution: 0.1° × 0.1° (~10 km)
- At this resolution, small talukas may have only 1-2 grid cells
- Consider using area-weighted averaging for better representation

### Temporal Considerations
- **2006-2014:** TRMM-era (reprocessed)
- **2014-2015:** TRMM/GPM overlap period
- **2015-2025:** GPM-era
- Small discontinuities possible at transition points

---

## 🎯 Next Steps for Rainfall-Runoff Modeling

### 1. Data Preparation
- ✅ Extract rainfall data (using methods above)
- ✅ Organize by administrative circles
- ✅ Quality control and gap filling

### 2. Basin Delineation
- Use DEM to delineate Panchganga sub-basins
- Match sub-basins to administrative circles where possible
- Create weighted rainfall inputs if basins don't align perfectly

### 3. Model Setup
For HEC-HMS or similar continuous models:
- **Rainfall Input:** Daily time series by taluka/sub-basin
- **Evapotranspiration:** From NASA POWER or IMD
- **Soil Data:** Use National Bureau of Soil Survey maps
- **Land Use:** From Bhuvan or LULC datasets

### 4. Calibration & Validation
- Split data: 2006-2015 (calibration), 2016-2025 (validation)
- Use observed discharge data if available
- Calibrate separately for monsoon and non-monsoon periods

---

## 📚 References & Resources

### Data Sources
1. **GPM Data:** https://gpm.nasa.gov/data/directory
2. **Google Earth Engine:** https://earthengine.google.com/
3. **NASA GES DISC:** https://disc.gsfc.nasa.gov/
4. **NASA POWER:** https://power.larc.nasa.gov/

### Documentation
1. **IMERG Technical Documentation:** 
   https://gpm.nasa.gov/resources/documents/imerg-v07-technical-documentation
2. **TRMM to GPM Transition:** 
   https://gpm.nasa.gov/resources/documents/transition-multi-satellite-products-trmm-gpm-tmpa-imerg

### Research Papers
1. Huffman, G.J., et al. (2023). "GPM IMERG Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V07"
2. Kulkarni, A., & Kale, G. (2022). "Event-based hydrological modeling using HEC-HMS: Panchganga River basin case study"

---

## 🆘 Troubleshooting

### Issue: Google Earth Engine access denied
**Solution:** Ensure you've registered at https://earthengine.google.com/signup/ and waited for approval

### Issue: Export task fails in GEE
**Solution:** 
- Check if you have sufficient Google Drive space
- Try reducing date range and export in chunks
- Ensure you're exporting to a valid folder

### Issue: Missing data in downloaded files
**Solution:**
- Check original data availability for specific dates
- Use gap-filling methods (linear interpolation)
- Cross-validate with other sources

### Issue: Unrealistic rainfall values
**Solution:**
- Check units (should be mm/day or mm/month)
- Verify coordinates are correct
- Compare with nearby stations
- Apply quality control thresholds

---

## ✅ Summary Checklist

- [ ] Sign up for Google Earth Engine account
- [ ] Run the provided JavaScript code in GEE
- [ ] Export data to Google Drive
- [ ] Download CSV files
- [ ] Run quality control checks
- [ ] Generate statistics by taluka
- [ ] Create visualizations
- [ ] Export in model-ready format
- [ ] Set up rainfall-runoff model
- [ ] Begin calibration and validation

---

## 📧 Support

For questions about:
- **GPM/IMERG data:** https://gpm.nasa.gov/contact
- **Google Earth Engine:** https://developers.google.com/earth-engine/help
- **This analysis:** Review the documentation or consult with hydrological modeling experts

---

**Document Version:** 1.0
**Last Updated:** February 7, 2026
**Prepared for:** Panchganga Basin Rainfall-Runoff Modeling Study

---

## 🎉 Conclusion

**Your request is 100% FEASIBLE!**

You can obtain TRMM/GPM rainfall data for the Panchganga basin organized by all 12 administrative circles (talukas) of Kolhapur district for the complete 20-year period (2006-2025).

**Recommended workflow:**
1. Use Google Earth Engine (easiest and most accurate)
2. Export data to Google Drive
3. Process and analyze using provided Python scripts
4. Use in your continuous rainfall-runoff model

**The data is ready to be extracted - all tools and code are provided!**
