import pandas as pd
import geopandas as gpd

class Maps():
	def __init__(self):
		self.geofile = "C:\\Users\\Admin\\Desktop\\program\\Pythonist\\tubes-alpro-politik\\pages\\indonesia.geojson"
		self.gdf = gpd.read_file(self.geofile)

	# def showMap(self):
	# 	m = folium.Map(location=[self.gdf.centroid.y.mean(), self.gdf.centroid.x.mean()], zoom_start=5)
	# 	folium.GeoJson(self.gdf,
	# 		tooltip=folium.GeoJsonTooltip(fields=['state']),
	# 		popup=folium.GeoJsonPopup(fields=['state'])
	# 	).add_to(m)
	# 	folium_static(m)

	def getState(self):
		return self.gdf["state"].to_numpy().flatten()