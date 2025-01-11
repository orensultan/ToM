import pdb

import streamlit as st
import pandas as pd
import os
import ast

def load_data(csv_file):
    """
    Load the CSV file and return the DataFrame
    """
    try:
        df = pd.read_csv(csv_file)
        # df['cands'] = df['cands'].apply(ast.literal_eval)
        df['enrich_analyzed_story'] = df['enrich_analyzed_story'].apply(ast.literal_eval)

        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None


def display_story_details(row):
    """
    Display the details of a specific story
    """
    # Story and Image Section
    st.header(f"Story {row['story_id']}")

    # Display Story
    st.subheader("Story")
    st.write(row['story_structure'])

    # Display Story
    st.subheader("Enriched Story")
    st.write(row['story_structure'])

    # Display Concept Tokens
    st.subheader('Enriched Sentences')
    enriched_sentence = [x['Enriched Sentence'] for x in row["enrich_analyzed_story"].values()][1:]
    st.write(enriched_sentence)

    # Display Concept Tokens
    st.subheader("Concept Tokens")
    st.write(row['concept_tokens_mapping'])

    # Display Scene Settings
    st.subheader("Scene Settings")
    st.write(row['scene_settings'])

    # Display Scene Captions
    st.subheader("Scene Captions")
    st.write(row['scene_captions'])

    # Display Image
    st.subheader("Story Image")
    image_path = row['combined_image_path']

    print("=========================")


    print(image_path)
    print(type(image_path))
    image_path = image_path.replace("/dccstor/knewedge/asafy/consistory/consistory/tom_exp", "/Users/osultan/PycharmProjects/ToM")
    print(image_path)
    # Check if image exists
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Image for Story {row['story_id']}")
    else:
        st.warning(f"Image not found at path: {image_path}")

    # Quiz Section
    st.subheader("Quiz Question")
    st.write(row['question'])


    # # Options
    # options = [
    #     row['cands'][0],
    #     row['cands'][1],
    # ]

    # Radio button for selecting answer
    # user_answer = st.radio("Select your answer:")

    # Reveal correct answer
    st.write(f"Correct Answer: {row['expected_answer']}")

    # # Check if user's answer is correct
    # if user_answer == row['expected_answer']:
    #     st.success("Congratulations! Your answer is correct.")
    # else:
    #     st.error("Oops! That's not the correct answer.")


def main():
    # Set page configuration
    st.set_page_config(page_title="Story Quiz App", page_icon=":book:", layout="wide")

    # Title
    st.title("Story Quiz Application")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Load the data
        df = load_data(uploaded_file)

        if df is not None:
            # Story selection
            story_number = st.number_input(
                "Enter a story number",
                min_value=1,
                max_value=len(df),
                value=1
            )

            # Adjust index to 0-based
            row = df.iloc[story_number - 1]

            # Display story details
            display_story_details(row)


if __name__ == "__main__":
    main()