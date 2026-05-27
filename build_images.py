#!/usr/bin/env python3
"""Map Higgsfield job IDs to semantic names and emit a JSON URL manifest."""
import json, os, sys

SHOW = sys.argv[1]
OUT_JSON = "assets/img/manifest.json"
os.makedirs("assets/img", exist_ok=True)

MAPPING = {
    # Hero (10)
    "5dd37092-c999-458c-b612-5440a5aed47f": "hero-01",
    "6072e7fd-3734-49b9-b9fe-c3d2250e8d02": "hero-02",
    "8c88b0ae-e939-43f4-ba6f-eeab7a86879c": "hero-03",
    "09aad1f6-2e87-41c8-aad6-76e37c90cc7b": "hero-04",
    "b44b69ef-961d-4f68-add3-57c39d82c30c": "hero-05",
    "31492d71-8838-4798-9c17-ec9f7125d84a": "hero-06",
    "39713f1c-8f3d-4039-b976-df4f554c33d3": "hero-07",
    "779872b1-b23d-46ce-b942-60f5407f276e": "hero-08",
    "af2141da-efd0-4d3c-adfd-295aea122c77": "hero-09",
    "90d93c00-0a2c-4fcf-ba01-e5bb91f5d142": "hero-10",
    # Services (3 each)
    "4d7aaafe-38c2-4bcc-b796-4f37a6cda47c": "custom-home-01",
    "8abfc4ab-e789-4bdd-9ed9-07472bd74e18": "custom-home-02",
    "6849d0c8-e4e4-4ceb-8813-ffb73f54f629": "custom-home-03",
    "c9644431-ddee-4bdf-93b9-4dbb39bae2aa": "whole-home-01",
    "74861bd4-06b2-44e2-a3ef-1d4ec61af35e": "whole-home-02",
    "307b6c93-7ec9-4fc4-9ac9-ca6aea50f370": "whole-home-03",
    "5890d5b1-73c1-4a4c-bdd2-a099bdf9e52a": "kitchen-01",
    "281b850f-6a79-4052-94d8-880c79b11951": "kitchen-02",
    "a40d328a-ac4b-41e5-a032-fe633a01b6e2": "kitchen-03",
    "402f4652-5f05-4d6b-a762-60c7395a8379": "bathroom-01",
    "0264ec22-c555-4bc7-9b14-3aa57ac8afa1": "bathroom-02",
    "4bcc417c-e23a-468b-b98e-861c3c12d56b": "bathroom-03",
    "18f45ed1-3ae1-412b-b1f0-fcf64a6967c5": "basement-01",
    "6c4d5d19-459b-4626-a83f-a90ea2d02aef": "basement-02",
    "4489a6eb-3957-4241-8a22-a2dea4d23a72": "basement-03",
    "3246b247-11c8-4d55-900d-afa7147a0e7c": "additions-01",
    "a5d1efad-e85f-491a-9e2a-dfc0fa359a02": "additions-02",
    "6f62e3f3-998f-4139-94f5-853b22f9154b": "additions-03",
    "e20bb6a6-fb05-4a2f-88cc-6df5b69a54b8": "outdoor-01",
    "cc4c606d-233a-4a2e-99ee-8f6e8bc09b3f": "outdoor-02",
    "15de6b8a-4559-4ad5-9b8d-3dec04cb6648": "outdoor-03",
    "994b2453-5b6c-4cbd-b451-e23f99ca315a": "commercial-01",
    "8bfbdc8e-c7ee-48f3-bb0f-9b8bb62881fe": "commercial-02",
    "0270cd31-0a84-4201-b4d3-1d9702162fd1": "commercial-03",
    "2d9792bf-f10f-4514-a70d-78cb48a685fa": "design-build-01",
    "93bd0590-5121-4a92-9c3d-535f6b462edd": "design-build-02",
    "23c3c6a0-e76a-450c-89f2-4e5c7aef9f33": "design-build-03",
    "82029889-e127-4179-b9cd-fc5103e2ab8b": "teardown-01",
    "b911801f-07ae-44ed-a6d1-e6f35090f0e7": "teardown-02",
    "be78adc9-124d-4a73-9d1e-66afdae36d9f": "teardown-03",
}

with open(SHOW) as f:
    data = json.load(f)
by_id = {item["id"]: item for item in data["items"]}

manifest = {}
missing = []
for jid, name in MAPPING.items():
    item = by_id.get(jid)
    if not item or item.get("status") != "completed":
        missing.append(name)
        continue
    manifest[name] = item["results"]["rawUrl"]

with open(OUT_JSON, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest entries: {len(manifest)} / {len(MAPPING)}")
if missing:
    print("Missing:", missing)
