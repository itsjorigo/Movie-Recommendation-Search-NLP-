import pandas as pd
import ast  # To convert string representations of lists to actual lists


def load_and_clean_data(movies_csv, keywords_csv):
    """Load, clean, and merge movies and keywords datasets."""

    # Load the main movies dataset
    movies_df = pd.read_csv(movies_csv, low_memory=False)

    # Load the keywords dataset
    keywords_df = pd.read_csv(keywords_csv, low_memory=False)

    # Convert 'id' to string in both DataFrames to avoid merging issues
    movies_df['id'] = movies_df['id'].astype(str)
    keywords_df['id'] = keywords_df['id'].astype(str)

    # Convert 'genres' and 'keywords' from JSON-like format to readable strings
    def parse_json_list(json_str):
        """Extracts 'name' field from list of dictionaries stored as a string."""
        try:
            items = ast.literal_eval(json_str)  # Convert string to list of dicts
            return ', '.join([item['name'] for item in items]) if isinstance(items, list) else ""
        except:
            return ""

    movies_df['genres'] = movies_df['genres'].apply(parse_json_list)
    movies_df['production_companies'] = movies_df['production_companies'].apply(parse_json_list)
    keywords_df['keywords'] = keywords_df['keywords'].apply(parse_json_list)

    # Merge movies and keywords on 'id'
    merged_df = movies_df.merge(keywords_df, on='id', how='left')

    # Keep only relevant columns
    merged_df = merged_df[['id', 'title', 'overview', 'genres', 'keywords', 'runtime',
                           'original_language', 'production_companies', 'popularity',
                           'vote_average', 'vote_count']]

    # Drop rows where overview is missing
    merged_df.dropna(subset=['overview'], inplace=True)

    return merged_df


def save_cleaned_data(movies_csv, keywords_csv, output_file):
    """Preprocesses movie data and saves the cleaned dataset."""
    cleaned_df = load_and_clean_data(movies_csv, keywords_csv)
    cleaned_df.to_csv(output_file, index=False)
    print(f"✅ Data preprocessed & saved to {output_file}!")


# Run preprocessing
if __name__ == "__main__":
    movies_file = r"data\movies_metadata.csv"
    keywords_file = r"data\keywords.csv"
    output_file = "cleaned_movies_2.csv"

    save_cleaned_data(movies_file, keywords_file, output_file)
