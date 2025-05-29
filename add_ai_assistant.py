import os
import re

def add_ai_assistant_script(html_file_path):
    """Add the AI assistant script tag to an HTML file if it doesn't already have it."""
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Skip if the file already has the ai_assistant.js script
    if 'ai_assistant.js' in content:
        print(f"Skipping {html_file_path} - Already contains AI assistant")
        return
    
    # Find the closing body tag
    body_end_match = re.search(r'</body>', content, re.IGNORECASE)
    
    if body_end_match:
        # Insert the script tag before the closing body tag
        insert_position = body_end_match.start()
        new_content = (
            content[:insert_position] + 
            '\n    <!-- AI Assistant Script -->\n' +
            '    <script src="/static/js/ai_assistant.js"></script>\n' +
            content[insert_position:]
        )
        
        # Write the modified content back to the file
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Added AI assistant to {html_file_path}")
    else:
        print(f"Could not find </body> tag in {html_file_path}")

def process_directory(directory_path):
    """Process all HTML files in the given directory."""
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.html'):
                # Skip the ai_assistant.html file itself
                if filename == 'ai_assistant.html':
                    continue
                    
                file_path = os.path.join(root, filename)
                add_ai_assistant_script(file_path)

if __name__ == "__main__":
    frontend_path = r"c:\Users\dulat\eroqa\EasyStay\FrontEnd"
    process_directory(frontend_path)
    print("Finished adding AI assistant to all HTML files")
