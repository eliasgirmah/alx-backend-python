# test.py — Fully clean CSV with messy double quotes
input_path = 'user_data.csv'
output_path = 'data.csv'

with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8', newline='') as outfile:
    for line in infile:
        # Remove ALL double quotes and extra whitespace
        clean_line = line.replace('"', '').strip()
        # Write cleaned line back with proper comma separation
        outfile.write(clean_line + '\n')

print(f"Cleaned CSV saved to: {output_path}")
