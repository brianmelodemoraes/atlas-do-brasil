import json, sys, subprocess
camada, zmin_detail, keep = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(",") if len(sys.argv) > 3 else None
raw = subprocess.run(["tippecanoe-decode", "-Z", str(zmin_detail), "-z", str(zmin_detail), f"../tiles/{camada}.pmtiles"], capture_output=True, text=True).stdout
j = json.loads(raw)
feats = []
for tile in j["features"]:
    for lyr in tile["features"]:
        for f in lyr["features"]:
            p = f["properties"]
            if keep: p = {k: p[k] for k in keep if k in p}
            feats.append({"type":"Feature","properties":p,"geometry":f["geometry"]})
json.dump({"type":"FeatureCollection","features":feats}, open(f"{camada}.geojson","w"), ensure_ascii=False)
print(camada, "features:", len(feats))
