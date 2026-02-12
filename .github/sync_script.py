import os
from github import Github
from datetime import datetime

token = os.getenv('GH_TOKEN')
g = Github(token)

DECOY_REPO_NAME = "sciencemindedone/gemini.google-policy-guidelines"

# A list of sources to mirror: (Source Repo, Source File, Local Save Name)
SOURCES = [
    ("google-gemini/cookbook", "quickstarts/Safety.ipynb", "dev_safety_logic.ipynb"),
    ("GoogleCloudPlatform/generative-ai", "gemini/responsible-ai/gemini_safety_ratings.ipynb", "enterprise_safety_standards.ipynb")
]

def main():
    decoy_repo = g.get_repo(DECOY_REPO_NAME)
    timestamp = datetime.now().strftime("%Y-%m-%d")

    for src_repo_name, src_file, local_name in SOURCES:
        try:
            print(f"Fetching {src_file} from {src_repo_name}...")
            source_repo = g.get_repo(src_repo_name)
            content = source_repo.get_contents(src_file).decoded_content.decode("utf-8")

            header = f"--- \norigin: {src_repo_name} \nlast_sync: {timestamp} \n--- \n\n"
            final_text = header + content

            try:
                # Update existing file
                existing_file = decoy_repo.get_contents(local_name)
                decoy_repo.update_file(existing_file.path, f"sync: {src_repo_name} {timestamp}", final_text, existing_file.sha)
                print(f"Successfully updated {local_name}")
            except:
                # Create if missing
                decoy_repo.create_file(local_name, f"initial import: {src_repo_name}", final_text)
                print(f"Successfully created {local_name}")

        except Exception as e:
            print(f"Failed to sync {src_repo_name}: {e}")

if __name__ == "__main__":
    main()
