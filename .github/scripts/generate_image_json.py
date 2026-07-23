import os
import json
import re

def natural_key(filename):
    name = os.path.splitext(filename)[0]
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', name)
    ]

def generate_json():
    image_folder = 'iconSet'
    json_data = {
        "name": "Tutu图标订阅",
        "description": "Icon Set for Surge",
        "icons": []
    }

    files = sorted(
        [f for f in os.listdir(image_folder) if f.endswith(".png")],
        key=natural_key
    )

    for filename in files:
        image_path = os.path.join(image_folder, filename)
        raw_url = f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/main/{image_path}"

        json_data["icons"].append({
            "name": filename,
            "url": raw_url
        })

    output_path = os.path.join(os.getcwd(), 'iconSet.json')

    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    with open(os.environ['GITHUB_STATE'], 'a') as state_file:
        state_file.write(f"ICONS_JSON_PATH={output_path}\n")

if __name__ == "__main__":
    generate_json()
