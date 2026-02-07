
// ============================================================================
// GPM IMERG Data Extraction for Panchganga Basin by Talukas
// Google Earth Engine Code
// ============================================================================

// Define time period
var startDate = '2006-01-01';
var endDate = '2025-12-31';

// Define Panchganga basin bounding box
var basin = ee.Geometry.Rectangle([
  73.5, 15.9, 
  74.7, 17.0
]);

// Define Taluka points (administrative circles of Kolhapur district)
var talukas = {
  'Karvir': ee.Geometry.Point([74.2433, 16.705]),
  'Panhala': ee.Geometry.Point([74.1167, 16.8167]),
  'Shahuwadi': ee.Geometry.Point([74.4833, 16.6167]),
  'Kagal': ee.Geometry.Point([74.3167, 16.5833]),
  'Hatkanangle': ee.Geometry.Point([74.45, 16.4333]),
  'Shirol': ee.Geometry.Point([74.4667, 16.7167]),
  'Radhanagari': ee.Geometry.Point([73.9833, 16.4167]),
  'Gaganbawada': ee.Geometry.Point([73.7667, 16.55]),
  'Bhudargad': ee.Geometry.Point([74.0667, 16.0167]),
  'Gadhinglaj': ee.Geometry.Point([74.35, 16.2333]),
  'Chandgad': ee.Geometry.Point([74.2333, 15.9833]),
  'Ajra': ee.Geometry.Point([73.9667, 16.1167]),

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
