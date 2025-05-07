import csv
import os
from datetime import datetime
import markdown

os.makedirs("posts", exist_ok=True)

with open("blog_data.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    posts = list(reader)

# Generate individual posts
for post in posts:
    md_content = open("post.md", "r").read()
    html_content = md_content \
        .replace("{{ title }}", post["Title"]) \
        .replace("{{ date }}", post["Date"]) \
        .replace("{{ author }}", post["Author"]) \
        .replace("{{ label }}", post["Label"]) \
        .replace("{{ image_url }}", post["Image_URL"]) \
        .replace("{{ content }}", markdown.markdown(post.get("Content", "Coming soon...")))

    filename = f"posts/{post['Title'].lower().replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

# Generate index.html
index_template = open("index.html", "r").read()
posts_html = ""

for post in posts:
    post_card = f"""
    <article class="post-card">
        <img src="{post['Image_URL']}" alt="{post['Title']}">
        <h2><a href="posts/{post['Title'].lower().replace(' ', '_')}.html">{post['Title']}</a></h2>
        <p class="meta">Published on {post['Date']} by {post['Author']} in {post['Label']}</p>
        <p>{post['Description']}</p>
    </article>
    """
    posts_html += post_card

final_index = index_template.replace("<!-- Posts will be inserted here by generator -->", posts_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_index)

print("✅ Blog generated successfully in /posts and index.html updated.")
