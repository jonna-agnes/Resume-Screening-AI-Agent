import gspread
from datetime import datetime

def connect_sheet():
    gc = gspread.service_account(filename="service_account.json")
    return gc.open("Resume_Screening_DB").sheet1


def save_ranked_results(results):
    sheet = connect_sheet()

    # Get existing rows
    existing = sheet.get_all_records()
    existing_map = {row["Candidate"]: row for row in existing}

    # Insert/update values in consistent format
    for r in results:
        existing_map[r["filename"]] = {
            "Candidate": r["filename"],
            "Score": int(r["fit_score"]),
            "Match Level": r["match_level"],
            "Best Role": r["best_role"],
            "Status": r["status"],
            "Similarity": r["similarity"],
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    # Sort correctly
    sorted_rows = sorted(
        existing_map.values(),
        key=lambda x: int(x["Score"]) if str(x["Score"]).isdigit() else 0,
        reverse=True
    )

    # Assign rank numbers
    for i, row in enumerate(sorted_rows, start=1):
        row["Rank"] = i

    # Clear previous sheet content
    sheet.clear()

    # Write header row
    sheet.append_row(["Rank", "Candidate", "Score", "Match Level", "Best Role", "Status", "Similarity", "Timestamp"])

    # Write updated rows
    for row in sorted_rows:
        sheet.append_row([
            row["Rank"],
            row["Candidate"],
            row["Score"],
            row["Match Level"],
            row["Best Role"],
            row["Status"],
            row["Similarity"],
            row["Timestamp"]
        ])
