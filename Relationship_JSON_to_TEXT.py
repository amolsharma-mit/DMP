import json

# Input and output file names
input_file = "gemini_result_2.txt"   # contains JSON
output_file = "output_gemini_result_2.txt" # final formatted relationships

# Read JSON from text file
with open(input_file, "r") as f:
    data = json.load(f)

relationships = data.get("relationships", [])

# Write formatted output
with open(output_file, "w") as f:
    for rel in relationships:
        name = rel.get("name", "")
        source = rel.get("source", "")
        target = rel.get("target", "")
        f.write(f"{source} : {name} : {target}\n")

print("Relationships written successfully to output.txt")
