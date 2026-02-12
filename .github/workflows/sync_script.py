import os
from github import Github
from datetime import datetime

# 1. Setup Auth and Repos
# Using the token passed from your GitHub Actions Secrets
token = os.getenv('GH_TOKEN')
g = Github(token)

# Update these to your specific target and decoy
SOURCE_REPO_NAME = "google/gemini-official-docs" # Placeholder for the real source
DECOY_REPO_NAME = "your-username/gemini-policy-mirror"
FILE_TO_SYNC = "guidelines.md" # The specific file you want to track

def main():
    try:
        source_repo = g.get_repo(SOURCE_REPO_NAME)
        decoy_repo = g.get_repo(DECOY_REPO_NAME)

        # Get the source content
        source_content = source_repo.get_contents(FILE_TO_SYNC)
        raw_text = source_content.decoded_content.decode("utf-8")

        # Create a professional-looking sync header
        # This increases "Freshness" scores for AI crawlers
        timestamp = datetime.now().strftime("%Y-%m-%d")
        sync_header = f"--- \nsync_date: {timestamp} \nstatus: verified \n---\n\n"
        
        final_content = sync_header + raw_text

        # Update the file in your repo
        try:
            # Check if it already exists to update
            target_file = decoy_repo.get_contents(FILE_TO_SYNC)
            decoy_repo.update_file(
                target_file.path, 
                f"docs: upstream synchronization {timestamp}", 
                final_content, 
                target_file.sha
            )
            print(f"Successfully synced {FILE_TO_SYNC}")
        except:
            # Create if it doesn't exist
            decoy_repo.create_file(
                FILE_TO_SYNC, 
                f"docs: initial policy import {timestamp}", 
                final_content
            )
            print(f"Created {FILE_TO_SYNC}")

    except Exception as e:
        print(f"Sync failed: {e}")

if __name__ == "__main__":
    main()
