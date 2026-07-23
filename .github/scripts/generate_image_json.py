import os
import json
import re

def natural_key(filename):
    name = os.path.splitext(filename)[0]
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r'(\d+)', name)
    ]

def generate_json():
    image_folder = "iconSet"

    json_data = {
        "name": "Tutu图标订阅",
        "description": "Icon Set for Surge",
        "icons": []
    }

    files = sorted(
        (
            f for f in os.listdir(image_folder)
            if f.lower().endswith(".png")
        ),
        key=natural_key
    )

    repository = os.environ["GITHUB_REPOSITORY"]

    for filename in files:
        image_path = os.path.join(image_folder, filename).replace("\\", "/")

        json_data["icons"].append({
            "name": filename,
            "url": f"https://raw.githubusercontent.com/{repository}/main/{image_path}"
        })

    output_path = os.path.join(os.getcwd(), "iconSet.json")

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    if "GITHUB_STATE" in os.environ:
        with open(os.environ["GITHUB_STATE"], "a") as state_file:
            state_file.write(f"ICONS_JSON_PATH={output_path}\n")

if __name__ == "__main__":
    generate_json()
