import csv
import re


def parse_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all entries along with their Entry IDs
    entries = re.split(r'(Entry #\d+[-]+)', content)
    # entries will be something like ['', 'Entry #3-----', 'content', 'Entry #4-----', 'content', ...]

    rows = []
    for i in range(1, len(entries), 2):
        entry_id_line = entries[i]
        entry_content = entries[i + 1]

        # Extract Entry ID number
        entry_id_match = re.search(r'Entry #(\d+)', entry_id_line)
        entry_id = entry_id_match.group(1) if entry_id_match else ''

        # Extract Gold
        gold_match = re.search(r'Gold:\s*(.+)', entry_content)
        gold = gold_match.group(1).strip() if gold_match else ''

        # Extract Pred
        pred_match = re.search(r'Pred:\s*(.+)', entry_content)
        pred = pred_match.group(1).strip() if pred_match else ''

        # Extract Question (the line starting with "Question:")
        question_match = re.search(r'Question:\s*(.+)', entry_content)
        question = question_match.group(1).strip() if question_match else ''

        # Extract ERROR_ANALYSIS (last line starting with ERROR_ANALYSIS:)
        error_match = re.search(r'ERROR_ANALYSIS:\s*(.+)', entry_content)
        error_analysis = error_match.group(1).strip() if error_match else ''

        rows.append({
            'entry_id': entry_id,
            'pred': pred,
            'gold': gold,
            'question': question,
            'error_analysis': error_analysis
        })

    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['entry_id', 'pred', 'gold', 'question', 'error_analysis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# Example usage:
parse_file('private-sql-error-analysis.txt', 'output.csv')
