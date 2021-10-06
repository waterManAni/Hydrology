# Hydrology

workflow:

- Clip raster to desired area
- Get flow accumulation just filling by the lidar precision (0.1m)
- For known culverts: extend known_culvert.shp to the flow accumulation and burn stream at road using whitebox tools
- Get embankment mapping to delineate roads, detect road center line (also used for material delineation and zsh p in tuflow)->compare with the approx draw, rotate, snap to highest, method
- for unknown culvert, detect culverts and bridges: https://www.tandfonline.com/doi/full/10.1080/13658816.2018.1530353#
- maybe detect road using machine learning???https://github.com/waterManAni/robosat
- use whitebox for delineation etc https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html
- if possible- kerbs, table drains and stormwater networks for minor events: https://scholarsarchive.byu.edu/josh/vol3/iss2/2/
- if possible consider land usage for delineation: https://www.mdpi.com/2220-9964/9/11/634/pdf
