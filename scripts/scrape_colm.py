import json

import openreview

# OpenReview Credentials (Replace with your credentials)
USERNAME = "..."
PASSWORD = "..."

# Connect to OpenReview API
client = openreview.api.OpenReviewClient(
    baseurl="https://api2.openreview.net", username=USERNAME, password=PASSWORD
)

# COLM 2024 Venue ID
VENUE_ID = "colmweb.org/COLM/2024/Conference"

# Get venue information
venue_group = client.get_group(VENUE_ID)

# Determine submission invitation name
submission_name = venue_group.content.get("submission_name", {}).get("value", "Submission")
invitation_name = f"{VENUE_ID}/-/{submission_name}"

# Fetch all submissions
print("Fetching submissions...")
submissions = client.get_all_notes(invitation=invitation_name, details="replies")

# Extract metadata and save to file
output_filename = "COLM2024_Accepted_Papers.jsonl"
with open(output_filename, "w", encoding="utf-8") as f:
    for paper in submissions:
        data = {
            "title": paper.content["title"]["value"],
            "keywords": paper.content.get("keywords", {}).get("value", []),
            "authors": paper.content["authors"]["value"],
            "abstract": paper.content["abstract"]["value"],
            "pdf_url": f"https://openreview.net/pdf?id={paper.id}",
        }

        # Print and save metadata
        print(
            f"Title: {data['title']}\nKeywords: {data['keywords']}\nAuthors: {', '.join(data['authors'])}\nAbstract: {data['abstract'][:200]}...\nPDF: {data['pdf_url']}\n{'-'*80}"
        )

        f.write(json.dumps(data) + "\n")

print(f"Metadata saved to {output_filename}")
