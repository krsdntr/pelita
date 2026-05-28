import json
import os

log_path = r"C:\Users\User\.gemini\antigravity-ide\brain\60e0e3f1-0518-4d85-90d0-f96c9080c672\.system_generated\logs\transcript.jsonl"
output_path = r"C:\Users\User\.gemini\antigravity-ide\brain\60e0e3f1-0518-4d85-90d0-f96c9080c672\scratch\stats_header_history.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

history = []
for line in lines:
    try:
        data = json.loads(line)
        content = data.get('content', '')
        if isinstance(content, str) and 'StatsHeader.astro' in content:
            history.append(content)
        
        # Also check tool calls for read/write
        tool_calls = data.get('tool_calls', [])
        for call in tool_calls:
            call_args = call.get('function', {}).get('arguments', '')
            if isinstance(call_args, str) and 'StatsHeader.astro' in call_args:
                history.append(f"TOOL CALL ARGS: {call_args}")
            
        tool_results = data.get('tool_results', [])
        for result in tool_results:
            result_content = result.get('content', '')
            if isinstance(result_content, str) and 'StatsHeader.astro' in result_content:
                history.append(f"TOOL RESULT: {result_content}")
                
    except Exception as e:
        pass

with open(output_path, 'w', encoding='utf-8') as f:
    for item in history[-50:]:  # get last 50 mentions
        f.write(item + "\n\n" + "="*80 + "\n\n")

print(f"Saved to {output_path}")
