import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"D:\InksAndTech\content\posts"
attachments_dir = r"D:\Obsidian Notes\Obsidian Notes\Obsidian Notes\Personl Notes\images"
static_images_dir = r"D:\InksAndTech\static\images"

# Step 1: Process each markdown file in the posts directory AND its subdirectories
for root, dirs, files in os.walk(posts_dir):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Step 2: Find all image links in the format [[filename.png]] or [[filename.jpg]]
            images = re.findall(r'\[\[([^]]*\.png)\]\]', content) or re.findall(r'\[\[([^]]*\.jpg)\]\]', content)
            
            # Step 3: Replace image links and ensure URLs are correctly formatted
            for image in images:
                # Prepare the Markdown-compatible link with %20 replacing spaces
                markdown_image = f"[Image Description](/images/{image.replace(' ', '%20')})"
                content = content.replace(f"[[{image}]]", markdown_image)
                
                # Step 4: Copy the image to the Hugo static/images directory if it exists
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, static_images_dir)
                    
            # Step 5: Write the updated content back to the markdown file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

print("Markdown files processed and images copied successfully.")