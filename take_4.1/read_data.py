
import pandas as pd

import ast

def convert_to_list(paths):
    try:
        return ast.literal_eval(paths)  # Safely evaluate string as a Python literal
    except (ValueError, SyntaxError):
        return []  # Return an empty list if conversion fails


def extract_paths(paths):
    return [path[path.find("generated_images/"):] for path in paths if "generated_images/" in path]


import re

# Function to replace tokens in the scene settings based on the mapping
# Function to replace tokens
def replace_tokens(row):
    # Parse the strings into Python data structures
    scene_list = ast.literal_eval(row["scene_settings"])
    concept_dict = ast.literal_eval(row["concept_tokens_mapping"])

    # Replace tokens in each scene
    replaced_scenes = []
    for scene in scene_list:
        for token, description in concept_dict.items():
            scene = scene.replace(f"{{{token}}}", description)
        replaced_scenes.append(scene)

    return replaced_scenes  # Return the list directly




def parse_scene_settings(data):
    if isinstance(data, str):
        # Use ast.literal_eval to safely evaluate the string as a Python list
        return ast.literal_eval(data)
    return data  # If it's already a list, return as is


# import









def main():
    df = pd.read_csv("prossed_tom_exp_data_with_scenes_take_4.1_with_photos.csv")
    df['generated_image_paths'] = df['generated_image_paths'].apply(convert_to_list)
    df['generated_image_paths'] = df['generated_image_paths'].apply(extract_paths)
    df["scene_settings_concept_tokens"] = df.apply(replace_tokens, axis=1)
    df["scene_settings_concept_tokens"] = df["scene_settings_concept_tokens"].apply(parse_scene_settings)

    pairs = []
    for prompts, image_paths in zip(df["scene_settings_concept_tokens"], df["generated_image_paths"]):
        for img_path, prompt in zip(image_paths, prompts):
            pairs.append({"img_path": img_path, "prompt": prompt})

    output_df = pd.DataFrame(pairs)
    output_df.to_csv("img_path_prompt_pairs.csv", index=False)
















    print(1)



if __name__ == "__main__":
    main()