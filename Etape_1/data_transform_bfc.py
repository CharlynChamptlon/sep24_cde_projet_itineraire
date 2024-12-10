import json
import pandas as pd

fichier_json = "flux-22456-202412091226.jsonld"

def get_value(obj, *keys):
    for key in keys:
        if isinstance(obj, dict):
            obj = obj.get(key, {})
        elif isinstance(obj, list) and obj:
            obj = obj[0]
        else:
            return None
    return obj if obj != {} else None

def determine_category(types):
    if isinstance(types, str):
        types = [types]
    for type in types:
        if "SportsAndLeisurePlace" in type:
            return "SportsAndLeisurePlace"
        elif "Landform" in type:
            return "Landform"
        elif "CulturalSite" in type:
            return "CulturalSite"
    return "Autre"

try:
    with open(fichier_json, 'r', encoding='utf-8') as fichier:
        data = json.load(fichier)

    rows = []

    for item in data["@graph"]:
        identifier = get_value(item, "dc:identifier")
        label = get_value(item, "rdfs:label", "@value")
        types = item.get("@type", [])
        description = get_value(item, "owl:topObjectProperty", "dc:description", "@value")
        locality = get_value(item, "isLocatedAt", "schema:address", "schema:addressLocality")
        postal_code = get_value(item, "isLocatedAt", "schema:address", "schema:postalCode")
        latitude = get_value(item, "isLocatedAt", "schema:geo", "schema:latitude", "@value")
        longitude = get_value(item, "isLocatedAt", "schema:geo", "schema:longitude", "@value")

        category = determine_category(types)

        rows.append({
            "Identifier": identifier,
            "Label": label,
            "Category": category,
            "Description": description,
            "Locality": locality,
            "Postal Code": postal_code,
            "Latitude": latitude,
            "Longitude": longitude
        })

    df = pd.DataFrame(rows)
    df = df.dropna(axis = 0, how = 'all', subset=['Latitude','Longitude'])
    print(df)
    df.to_csv("POI_BFC.csv", index=False, encoding="utf-8")

except FileNotFoundError:
    print(f"Erreur : Le fichier '{fichier_json}' est introuvable.")
except json.JSONDecodeError:
    print(f"Erreur : Le fichier '{fichier_json}' n'est pas un JSON valide.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")