import json
import os
import re

log_path = r"C:\Users\User\.gemini\antigravity-ide\brain\60e0e3f1-0518-4d85-90d0-f96c9080c672\.system_generated\logs\transcript.jsonl"
output_path = r"C:\Users\User\.gemini\antigravity-ide\brain\60e0e3f1-0518-4d85-90d0-f96c9080c672\scratch\stats_header_full.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

best_content = ""

for line in lines:
    try:
        data = json.loads(line)
        
        # Look for view_file output
        tool_results = data.get('tool_results', [])
        for result in tool_results:
            name = result.get('name')
            content = result.get('content', '')
            if name == 'default_api:view_file' and 'StatsHeader.astro' in content:
                # If we see it, save it
                if len(content) > len(best_content):
                    best_content = content
                    
        # Look for edit file operations that could show the content
        tool_calls = data.get('tool_calls', [])
        for call in tool_calls:
            name = call.get('function', {}).get('name')
            args = call.get('function', {}).get('arguments', '')
            if name in ('default_api:multi_replace_file_content', 'default_api:replace_file_content', 'default_api:write_to_file'):
                if 'StatsHeader.astro' in args:
                    best_content += f"\n\n--- EDIT OPERATION ---\n{args}\n"

    except Exception as e:
        pass

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(best_content)

print("Done")
