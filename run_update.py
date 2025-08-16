# run_update.py

import argparse
from data_pipeline import update_company_data

def main():
    """
    Main function to run the data update pipeline for a specific company.
    """
    # Set up an argument parser to accept a company name from the command line
    parser = argparse.ArgumentParser(description="Update company intelligence data and create a local FAISS index.")
    parser.add_argument(
        "--company",
        type=str,
        required=True,
        help="The name of the company to fetch news for (e.g., 'Tesla', 'NVIDIA')."
    )
    args = parser.parse_args()
    
    company_name = args.company

    print(f"🚀 Starting data update for: {company_name}...")
    
    try:
        # Call the main data pipeline function
        update_company_data(company_name, max_articles=8)
        print(f"✅ Successfully updated data for {company_name}.")
        print(f"You can now launch the Streamlit app to query information about {company_name}.")
        
    except Exception as e:
        print(f"❌ An error occurred during the update: {e}")

if __name__ == "__main__":
    main()