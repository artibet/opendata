import geopandas as gpd

gdf = gpd.read_file('amea.kmz')
gdf.to_file('amea.geojson', driver='GeoJSON')