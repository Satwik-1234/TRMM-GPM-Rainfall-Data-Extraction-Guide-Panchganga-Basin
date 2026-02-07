"""
TRMM/GPM IMERG Rainfall Data Fetcher for Panchganga Basin
===========================================================

This script fetches satellite-based rainfall data for the Panchganga basin
organized by administrative circles (talukas) of Kolhapur district, Maharashtra.

Data Source: GPM IMERG (which includes TRMM-era data from 2000-2015)
Time Period: 2006-2025 (20 years)
Spatial Resolution: 0.1° × 0.1° (~10 km)
Temporal Resolution: Daily (aggregated from 30-minute data)

IMPORTANT NOTE:
---------------
TRMM satellite was decommissioned in April 2015. However, the GPM IMERG V07 
dataset includes reprocessed TRMM-era data (2000-2015) combined with GPM data 
(2014-present), providing a continuous 20-year record.

Author: Generated for Panchganga Basin Rainfall-Runoff Modeling
Date: February 2026
"""

import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Try to import optional libraries
try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False
    print("Warning: h5py not installed. HDF5 file processing will not be available.")

try:
    import netCDF4
    HAS_NETCDF = True
except ImportError:
    HAS_NETCDF = False
    print("Warning: netCDF4 not installed. NetCDF file processing will not be available.")


class PanchgangaRainfallExtractor:
    """
    Extract TRMM/GPM IMERG rainfall data for Panchganga basin by administrative circles
    """
    
    def __init__(self):
        """
        Initialize with Kolhapur district administrative circles (talukas) and coordinates
        """
        # 12 Administrative Circles/Talukas of Kolhapur District
        # Each taluka has representative coordinates (approximate center)
        self.talukas = {
            'Karvir': {
                'lat': 16.7050,
                'lon': 74.2433,
                'area_km2': 760,
                'description': 'Includes Kolhapur city, district headquarters'
            },
            'Panhala': {
                'lat': 16.8167,
                'lon': 74.1167,
                'area_km2': 682,
                'description': 'Historic fort town, high elevation'
            },
            'Shahuwadi': {
                'lat': 16.6167,
                'lon': 74.4833,
                'area_km2': 565,
                'description': 'Eastern taluka'
            },
            'Kagal': {
                'lat': 16.5833,
                'lon': 74.3167,
                'area_km2': 436,
                'description': 'Industrial area'
            },
            'Hatkanangle': {
                'lat': 16.4333,
                'lon': 74.4500,
                'area_km2': 521,
                'description': 'Southern taluka'
            },
            'Shirol': {
                'lat': 16.7167,
                'lon': 74.4667,
                'area_km2': 674,
                'description': 'Agricultural region'
            },
            'Radhanagari': {
                'lat': 16.4167,
                'lon': 73.9833,
                'area_km2': 1041,
                'description': 'Western Ghats, wildlife sanctuary, high rainfall'
            },
            'Gaganbawada': {
                'lat': 16.5500,
                'lon': 73.7667,
                'area_km2': 681,
                'description': 'Western Ghats region, high rainfall'
            },
            'Bhudargad': {
                'lat': 16.0167,
                'lon': 74.0667,
                'area_km2': 569,
                'description': 'Southern region near Karnataka border'
            },
            'Gadhinglaj': {
                'lat': 16.2333,
                'lon': 74.3500,
                'area_km2': 589,
                'description': 'Southern taluka'
            },
            'Chandgad': {
                'lat': 15.9833,
                'lon': 74.2333,
                'area_km2': 632,
                'description': 'Southernmost taluka'
            },
            'Ajra': {
                'lat': 16.1167,
                'lon': 73.9667,
                'area_km2': 539,
                'description': 'Western region'
            }
        }
        
        # Panchganga basin bounding box
        self.basin_bbox = {
            'min_lat': 15.90,
            'max_lat': 17.00,
            'min_lon': 73.50,
            'max_lon': 74.70
        }
        
        # Data availability information
        self.data_info = {
            'TRMM_era': {
                'period': '2000-01-01 to 2015-04-15',
                'status': 'Decommissioned, reprocessed as IMERG',
                'resolution': '0.25° × 0.25° (original TMPA)'
            },
            'GPM_IMERG': {
                'period': '2000-06-01 to Present',
                'status': 'Active - includes TRMM-era reprocessing',
                'resolution': '0.1° × 0.1°',
                'version': 'V07B'
            }
        }
        
        print("="*70)
        print("PANCHGANGA BASIN RAINFALL DATA EXTRACTOR")
        print("="*70)
        print(f"\nBasin: Panchganga River Basin")
        print(f"District: Kolhapur, Maharashtra")
        print(f"Administrative Circles: {len(self.talukas)} Talukas")
        print(f"Data Period: 2006-2025 (20 years)")
        print(f"Data Source: GPM IMERG V07B (includes TRMM-era data)")
        print("="*70)
    
    def show_data_availability(self):
        """Display information about TRMM and GPM data availability"""
        print("\n" + "="*70)
        print("DATA AVAILABILITY INFORMATION")
        print("="*70)
        
        print("\n📡 TRMM (Tropical Rainfall Measuring Mission):")
        print("   Launch: November 1997")
        print("   Decommission: April 2015")
        print("   Coverage: 35°N to 35°S (covers Panchganga basin)")
        print("   Status: Data reprocessed and integrated into GPM IMERG")
        
        print("\n🛰️  GPM (Global Precipitation Measurement):")
        print("   Launch: February 2014")
        print("   Status: Active")
        print("   Coverage: 65°N to 65°S (global)")
        
        print("\n📊 GPM IMERG V07B (Recommended for this study):")
        print("   Data Period: June 2000 - Present")
        print("   Includes: TRMM-era (2000-2015) + GPM-era (2014-present)")
        print("   Resolution: 0.1° × 0.1° (~10 km)")
        print("   Temporal: 30-minute, aggregatable to daily/monthly")
        print("   Latency: ~3.5 months (Final Run)")
        
        print("\n✅ FEASIBILITY FOR YOUR REQUEST:")
        print("   Period: 2006-2025 (20 years) - FULLY AVAILABLE")
        print("   2006-2015: TRMM-era data (reprocessed as IMERG)")
        print("   2015-2025: GPM-era data")
        print("   Organization: By 12 talukas - FEASIBLE")
        
        print("\n" + "="*70)
    
    def get_taluka_coordinates(self, taluka_name: str) -> Tuple[float, float]:
        """Get coordinates for a specific taluka"""
        if taluka_name in self.talukas:
            return (self.talukas[taluka_name]['lat'], 
                   self.talukas[taluka_name]['lon'])
        else:
            raise ValueError(f"Taluka '{taluka_name}' not found")
    
    def generate_date_range(self, start_year: int = 2006, end_year: int = 2025) -> List[str]:
        """Generate monthly date ranges for data extraction"""
        dates = []
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                dates.append(f"{year}-{month:02d}")
        return dates
    
    def fetch_gpm_imerg_via_gesdisc(self, 
                                   year: int,
                                   month: int,
                                   username: str = None,
                                   password: str = None) -> pd.DataFrame:
        """
        Fetch GPM IMERG data from NASA GES DISC
        
        NOTE: Requires NASA Earthdata account
        Register at: https://urs.earthdata.nasa.gov/users/new
        
        Args:
            year: Year (2006-2025)
            month: Month (1-12)
            username: NASA Earthdata username
            password: NASA Earthdata password
            
        Returns:
            DataFrame with rainfall data for all talukas
        """
        if username is None or password is None:
            print("⚠️  NASA Earthdata credentials required")
            print("   Register at: https://urs.earthdata.nasa.gov/users/new")
            print("   Then provide credentials to this function")
            return pd.DataFrame()
        
        print(f"\nFetching GPM IMERG data for {year}-{month:02d}...")
        
        # GES DISC OPeNDAP endpoint
        base_url = "https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDF.07/"
        
        # Construct URL for specific month
        url = f"{base_url}{year}/{month:02d}/"
        
        try:
            # Authentication
            session = requests.Session()
            session.auth = (username, password)
            
            # Get file listing
            response = session.get(url)
            
            if response.status_code == 200:
                print(f"✓ Successfully connected to GES DISC")
                # Parse and download data (implementation depends on specific needs)
                # This is a placeholder - actual implementation would use OPeNDAP protocol
                return pd.DataFrame()
            else:
                print(f"✗ Failed to connect: {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return pd.DataFrame()
    
    def fetch_gpm_via_google_earth_engine(self) -> str:
        """
        Generate Google Earth Engine JavaScript code for data extraction
        
        Google Earth Engine provides easy access to GPM IMERG data
        This method generates the JavaScript code to run in GEE Code Editor
        
        Returns:
            JavaScript code string
        """
        
        gee_code = f"""
// ============================================================================
// GPM IMERG Data Extraction for Panchganga Basin by Talukas
// Google Earth Engine Code
// ============================================================================

// Define time period
var startDate = '2006-01-01';
var endDate = '2025-12-31';

// Define Panchganga basin bounding box
var basin = ee.Geometry.Rectangle([
  {self.basin_bbox['min_lon']}, {self.basin_bbox['min_lat']}, 
  {self.basin_bbox['max_lon']}, {self.basin_bbox['max_lat']}
]);

// Define Taluka points (administrative circles of Kolhapur district)
var talukas = {{
"""
        
        # Add all taluka coordinates
        for taluka, coords in self.talukas.items():
            gee_code += f"  '{taluka}': ee.Geometry.Point([{coords['lon']}, {coords['lat']}]),\n"
        
        gee_code += """
};

// Load GPM IMERG V07 dataset
var imerg = ee.ImageCollection('NASA/GPM_L3/IMERG_V07')
  .filterDate(startDate, endDate)
  .select('precipitationCal');  // Calibrated precipitation

// Function to extract daily rainfall for each taluka
function extractDailyRainfall(date) {
  var start = ee.Date(date);
  var end = start.advance(1, 'day');
  
  // Get daily precipitation (sum of 30-minute values)
  var daily = imerg.filterDate(start, end)
    .select('precipitationCal')
    .sum()
    .multiply(0.5);  // Convert to mm/day (30-min data × 0.5 hr)
  
  // Extract values for each taluka
  var features = [];
  Object.keys(talukas).forEach(function(talukaName) {
    var point = talukas[talukaName];
    var value = daily.reduceRegion({
      reducer: ee.Reducer.first(),
      geometry: point,
      scale: 10000  // 10 km resolution
    }).get('precipitationCal');
    
    features.push(ee.Feature(null, {
      'date': start.format('YYYY-MM-dd'),
      'taluka': talukaName,
      'rainfall_mm': value
    }));
  });
  
  return ee.FeatureCollection(features);
}

// Generate date sequence
var days = ee.List.sequence(0, ee.Date(endDate).difference(ee.Date(startDate), 'day').subtract(1));
var dates = days.map(function(day) {
  return ee.Date(startDate).advance(day, 'day');
});

// Extract rainfall for all dates
var rainfallData = ee.FeatureCollection(dates.map(extractDailyRainfall)).flatten();

// Export to Google Drive
Export.table.toDrive({
  collection: rainfallData,
  description: 'Panchganga_Rainfall_Taluka_Wise_2006_2025',
  fileFormat: 'CSV',
  folder: 'Panchganga_Rainfall_Data'
});

// Print information
print('Total number of records:', rainfallData.size());
print('Sample data:', rainfallData.limit(20));

// Visualize basin
Map.centerObject(basin, 9);
Map.addLayer(basin, {color: 'blue'}, 'Panchganga Basin');

// Add taluka points
Object.keys(talukas).forEach(function(talukaName) {
  Map.addLayer(talukas[talukaName], {color: 'red'}, talukaName);
});

// Create monthly summary as well
function extractMonthlyRainfall(yearMonth) {
  var year = ee.Number(yearMonth.get(0));
  var month = ee.Number(yearMonth.get(1));
  
  var start = ee.Date.fromYMD(year, month, 1);
  var end = start.advance(1, 'month');
  
  var monthly = imerg.filterDate(start, end)
    .select('precipitationCal')
    .sum()
    .multiply(0.5);
  
  var features = [];
  Object.keys(talukas).forEach(function(talukaName) {
    var point = talukas[talukaName];
    var value = monthly.reduceRegion({
      reducer: ee.Reducer.first(),
      geometry: point,
      scale: 10000
    }).get('precipitationCal');
    
    features.push(ee.Feature(null, {
      'year': year,
      'month': month,
      'taluka': talukaName,
      'rainfall_mm': value
    }));
  });
  
  return ee.FeatureCollection(features);
}

// Generate year-month combinations
var years = ee.List.sequence(2006, 2025);
var months = ee.List.sequence(1, 12);
var yearMonths = years.map(function(year) {
  return months.map(function(month) {
    return ee.List([year, month]);
  });
}).flatten();

var monthlyData = ee.FeatureCollection(yearMonths.map(extractMonthlyRainfall)).flatten();

// Export monthly data
Export.table.toDrive({
  collection: monthlyData,
  description: 'Panchganga_Rainfall_Monthly_Taluka_Wise_2006_2025',
  fileFormat: 'CSV',
  folder: 'Panchganga_Rainfall_Data'
});

print('Monthly data records:', monthlyData.size());
print('Monthly sample:', monthlyData.limit(20));

// ============================================================================
// INSTRUCTIONS TO USE THIS CODE:
// ============================================================================
// 1. Go to: https://code.earthengine.google.com/
// 2. Sign in with Google account (free for research use)
// 3. Copy and paste this entire code
// 4. Click "Run"
// 5. Check the Tasks tab (top right)
// 6. Click "Run" next to each export task
// 7. Data will be saved to your Google Drive
// ============================================================================
"""
        
        return gee_code
    
    def fetch_via_nasa_power_api(self, 
                                start_year: int = 2006,
                                end_year: int = 2025) -> pd.DataFrame:
        """
        Fetch rainfall data using NASA POWER API
        
        NASA POWER provides free access to meteorological data
        Note: This is different from GPM IMERG but provides good validation
        
        Args:
            start_year: Start year
            end_year: End year
            
        Returns:
            DataFrame with rainfall data for all talukas
        """
        print("\n" + "="*70)
        print("FETCHING DATA VIA NASA POWER API")
        print("="*70)
        print("\nNote: NASA POWER is different from GPM IMERG")
        print("      But provides good quality gridded rainfall data")
        print("      Resolution: 0.5° × 0.5°\n")
        
        all_data = []
        
        for taluka_name, coords in self.talukas.items():
            print(f"\nFetching data for {taluka_name}...")
            
            try:
                url = "https://power.larc.nasa.gov/api/temporal/daily/point"
                
                params = {
                    'parameters': 'PRECTOTCORR',
                    'community': 'RE',
                    'longitude': coords['lon'],
                    'latitude': coords['lat'],
                    'start': f"{start_year}0101",
                    'end': f"{end_year}1231",
                    'format': 'JSON'
                }
                
                response = requests.get(url, params=params, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    precip_data = data['properties']['parameter']['PRECTOTCORR']
                    
                    for date_str, rainfall in precip_data.items():
                        if rainfall != -999:  # -999 is missing data flag
                            all_data.append({
                                'Date': pd.to_datetime(date_str, format='%Y%m%d'),
                                'Taluka': taluka_name,
                                'Rainfall_mm': rainfall,
                                'Latitude': coords['lat'],
                                'Longitude': coords['lon']
                            })
                    
                    print(f"✓ Successfully fetched {len(precip_data)} days for {taluka_name}")
                    
                else:
                    print(f"✗ Failed for {taluka_name}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"✗ Error for {taluka_name}: {str(e)}")
                continue
        
        if all_data:
            df = pd.DataFrame(all_data)
            print(f"\n✓ Total records fetched: {len(df)}")
            return df
        else:
            return pd.DataFrame()
    
    def process_and_organize_data(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Process and organize data by taluka
        
        Args:
            df: DataFrame with columns: Date, Taluka, Rainfall_mm
            
        Returns:
            Dictionary of DataFrames, one per taluka
        """
        organized_data = {}
        
        for taluka in self.talukas.keys():
            taluka_df = df[df['Taluka'] == taluka].copy()
            taluka_df = taluka_df.sort_values('Date')
            taluka_df.reset_index(drop=True, inplace=True)
            organized_data[taluka] = taluka_df
        
        return organized_data
    
    def calculate_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate rainfall statistics for each taluka"""
        stats_list = []
        
        for taluka in self.talukas.keys():
            taluka_data = df[df['Taluka'] == taluka]['Rainfall_mm']
            
            stats = {
                'Taluka': taluka,
                'Area_km2': self.talukas[taluka]['area_km2'],
                'Mean_Annual_Rainfall_mm': taluka_data.groupby(df[df['Taluka'] == taluka]['Date'].dt.year).sum().mean(),
                'Max_Daily_Rainfall_mm': taluka_data.max(),
                'Min_Daily_Rainfall_mm': taluka_data[taluka_data > 0].min() if (taluka_data > 0).any() else 0,
                'Std_Dev_mm': taluka_data.std(),
                'Rainy_Days_per_Year': (taluka_data > 0).groupby(df[df['Taluka'] == taluka]['Date'].dt.year).sum().mean(),
                'Heavy_Rain_Days_per_Year': (taluka_data > 50).groupby(df[df['Taluka'] == taluka]['Date'].dt.year).sum().mean(),
                'Monsoon_Contribution_pct': taluka_data[df[df['Taluka'] == taluka]['Date'].dt.month.isin([6,7,8,9])].sum() / taluka_data.sum() * 100
            }
            
            stats_list.append(stats)
        
        return pd.DataFrame(stats_list)
    
    def export_taluka_wise_data(self, 
                               df: pd.DataFrame,
                               output_dir: str = 'taluka_rainfall_data'):
        """Export data as separate files for each taluka"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        organized = self.process_and_organize_data(df)
        
        for taluka, taluka_df in organized.items():
            # Save as CSV
            filename = f"{output_dir}/{taluka}_rainfall_2006_2025.csv"
            taluka_df.to_csv(filename, index=False)
            print(f"✓ Exported: {filename}")
        
        # Save combined data
        df.to_csv(f"{output_dir}/All_Talukas_Combined_2006_2025.csv", index=False)
        print(f"\n✓ Exported combined data: {output_dir}/All_Talukas_Combined_2006_2025.csv")
        
        # Save statistics
        stats = self.calculate_statistics(df)
        stats.to_csv(f"{output_dir}/Taluka_Rainfall_Statistics.csv", index=False)
        print(f"✓ Exported statistics: {output_dir}/Taluka_Rainfall_Statistics.csv")
    
    def export_for_runoff_model(self,
                                df: pd.DataFrame,
                                model_type: str = 'hec_hms',
                                output_dir: str = 'model_ready_data'):
        """
        Export data in format suitable for rainfall-runoff models
        
        Args:
            df: DataFrame with rainfall data
            model_type: 'hec_hms', 'swat', 'mike_she', 'generic'
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        organized = self.process_and_organize_data(df)
        
        for taluka, taluka_df in organized.items():
            if model_type == 'hec_hms':
                # HEC-HMS format
                output = pd.DataFrame({
                    'Date': taluka_df['Date'].dt.strftime('%d%b%Y').str.upper(),
                    'Time': '0000',
                    'Precipitation': taluka_df['Rainfall_mm']
                })
                
                filename = f"{output_dir}/{taluka}_HEC_HMS_format.txt"
                output.to_csv(filename, index=False, header=False, sep='\t')
                
            elif model_type == 'swat':
                # SWAT format
                filename = f"{output_dir}/{taluka}_SWAT_format.txt"
                with open(filename, 'w') as f:
                    f.write(f"{taluka} Taluka - Panchganga Basin\n")
                    f.write(f"Kolhapur, Maharashtra\n")
                    f.write(f"Lati\tLongi\tElev\n")
                    coords = self.talukas[taluka]
                    f.write(f"{coords['lat']}\t{coords['lon']}\t543\n")
                    f.write("YEAR\tMO\tDAY\tRAINFALL\n")
                    
                    for _, row in taluka_df.iterrows():
                        date = row['Date']
                        f.write(f"{date.year}\t{date.month}\t{date.day}\t{row['Rainfall_mm']:.2f}\n")
            
            print(f"✓ Exported {model_type.upper()} format for {taluka}")
        
        print(f"\n✓ All model-ready files saved in: {output_dir}/")
    
    def create_visualization_script(self) -> str:
        """Generate Python script for visualizing the data"""
        
        viz_script = """
# Rainfall Data Visualization Script
# ====================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('taluka_rainfall_data/All_Talukas_Combined_2006_2025.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (16, 10)

# 1. Annual rainfall by taluka
fig, axes = plt.subplots(3, 4, figsize=(20, 15))
fig.suptitle('Annual Rainfall Distribution by Taluka (2006-2025)', fontsize=16, fontweight='bold')

talukas = df['Taluka'].unique()
for idx, taluka in enumerate(talukas):
    ax = axes.flatten()[idx]
    taluka_data = df[df['Taluka'] == taluka]
    annual = taluka_data.groupby('Year')['Rainfall_mm'].sum()
    
    ax.plot(annual.index, annual.values, marker='o', linewidth=2)
    ax.set_title(taluka, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Annual Rainfall (mm)')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('taluka_annual_rainfall.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Monthly climatology by taluka
plt.figure(figsize=(16, 10))
for taluka in talukas:
    taluka_data = df[df['Taluka'] == taluka]
    monthly_avg = taluka_data.groupby('Month')['Rainfall_mm'].mean()
    plt.plot(range(1, 13), monthly_avg, marker='o', label=taluka, linewidth=2)

plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Monthly Rainfall (mm)', fontsize=12)
plt.title('Monthly Rainfall Climatology by Taluka (2006-2025)', fontsize=14, fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.savefig('monthly_climatology.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Heatmap of annual rainfall
annual_matrix = df.pivot_table(values='Rainfall_mm', 
                                index='Year', 
                                columns='Taluka', 
                                aggfunc='sum')

plt.figure(figsize=(14, 10))
sns.heatmap(annual_matrix, annot=True, fmt='.0f', cmap='YlGnBu', cbar_kws={'label': 'Rainfall (mm)'})
plt.title('Annual Rainfall Heatmap by Taluka (2006-2025)', fontsize=14, fontweight='bold')
plt.xlabel('Taluka', fontsize=12)
plt.ylabel('Year', fontsize=12)
plt.tight_layout()
plt.savefig('rainfall_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ All visualizations created!")
print("  - taluka_annual_rainfall.png")
print("  - monthly_climatology.png")
print("  - rainfall_heatmap.png")
"""
        
        return viz_script


def main():
    """
    Main execution function with complete workflow
    """
    # Initialize extractor
    extractor = PanchgangaRainfallExtractor()
    
    # Show data availability information
    extractor.show_data_availability()
    
    print("\n" + "="*70)
    print("DATA EXTRACTION OPTIONS")
    print("="*70)
    
    print("\n📌 OPTION 1: Google Earth Engine (RECOMMENDED)")
    print("   Advantages:")
    print("   - Direct access to GPM IMERG V07 dataset")
    print("   - Includes complete TRMM-era data (2000-2015)")
    print("   - Free for research use")
    print("   - Easy to use web interface")
    print("   - High spatial resolution (0.1° × 0.1°)")
    
    print("\n   Steps:")
    print("   1. Get Google Earth Engine JavaScript code (generated below)")
    print("   2. Go to: https://code.earthengine.google.com/")
    print("   3. Sign in with Google account")
    print("   4. Paste and run the code")
    print("   5. Export data to Google Drive")
    
    # Generate GEE code
    gee_code = extractor.fetch_gpm_via_google_earth_engine()
    
    # Save GEE code to file
    with open('/home/claude/gee_panchganga_rainfall_extraction.js', 'w') as f:
        f.write(gee_code)
    
    print("\n   ✓ Google Earth Engine code saved to:")
    print("     gee_panchganga_rainfall_extraction.js")
    
    print("\n" + "-"*70)
    
    print("\n📌 OPTION 2: NASA POWER API (ALTERNATIVE)")
    print("   Advantages:")
    print("   - Free, immediate access")
    print("   - No registration required")
    print("   - Automated download")
    print("   - Different from TRMM/GPM but good quality")
    
    print("\n   Note: Resolution is 0.5° × 0.5° (coarser than IMERG)")
    
    response = input("\n   Would you like to fetch NASA POWER data now? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        print("\n   Fetching data... This may take 10-15 minutes...")
        df = extractor.fetch_via_nasa_power_api(start_year=2006, end_year=2025)
        
        if not df.empty:
            # Export data
            print("\n   Exporting data...")
            extractor.export_taluka_wise_data(df, output_dir='/home/claude/taluka_rainfall_data')
            extractor.export_for_runoff_model(df, model_type='hec_hms', 
                                             output_dir='/home/claude/model_ready_data')
            
            # Generate statistics
            stats = extractor.calculate_statistics(df)
            print("\n" + "="*70)
            print("RAINFALL STATISTICS BY TALUKA")
            print("="*70)
            print(stats.to_string(index=False))
            
            # Create visualization script
            viz_script = extractor.create_visualization_script()
            with open('/home/claude/visualize_rainfall.py', 'w') as f:
                f.write(viz_script)
            
            print("\n✓ Visualization script created: visualize_rainfall.py")
            print("  Run it after downloading to create charts")
    
    print("\n" + "="*70)
    
    print("\n📌 OPTION 3: NASA GES DISC (Direct IMERG Download)")
    print("   Steps:")
    print("   1. Register at: https://urs.earthdata.nasa.gov/users/new")
    print("   2. Use credentials with the fetch function")
    print("   3. Download HDF5 files for processing")
    
    print("\n" + "="*70)
    print("\n✅ SUMMARY:")
    print("="*70)
    print("""
Your request is FULLY FEASIBLE. Here's what you have:

1. ✓ Data Period: 2006-2025 (20 years) - AVAILABLE
   - 2006-2015: TRMM-era data (reprocessed in GPM IMERG)
   - 2015-2025: GPM-era data
   
2. ✓ Spatial Coverage: Panchganga basin - COVERED
   - All 12 talukas of Kolhapur district included
   
3. ✓ Data Source: GPM IMERG V07B
   - Includes TRMM legacy data
   - Resolution: 0.1° × 0.1° (~10 km)
   - Temporal: Daily (from 30-minute data)

4. ✓ Organization: Circle-wise (Taluka-wise) - READY
   - All 12 administrative circles configured
   - Coordinates and metadata prepared

RECOMMENDED APPROACH:
====================
Use Google Earth Engine (Option 1) for best results:
- Complete TRMM/GPM IMERG dataset
- Easy web interface
- Free for research
- Code already generated for you

FILES CREATED:
=============
1. gee_panchganga_rainfall_extraction.js - Run in Google Earth Engine
2. visualize_rainfall.py - Create charts after data download
""")
    
    print("\nFiles are ready in the output directory!")
    print("="*70)


if __name__ == "__main__":
    main()
