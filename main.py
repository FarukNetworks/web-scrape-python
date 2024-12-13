from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep
import csv
import os

with sync_playwright() as p:

    fileDate = datetime.now().strftime("%Y-%m-%d")

    ## ENTER THE SITE NAME HERE 
    sitename = 'wolf-news'

    browser = p.chromium.launch()
    page = browser.new_page()

    ## ENTER THE URL HERE 
    page.goto("https://eggsmedia.dev/wolf/articles/news/")

    ## ENTER THE ARTICLE SELECTOR HERE 
    articles = page.query_selector_all("div.grid.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-4.gap-14.max-sm\\:gap-y-5.gsap-animated.gsap-fade-in-up-stagger article")
    
    # Prepare to store links and content
    data = []

    for article in articles[:1]:

        ## INSERT THE LOGIC TO SCRAPE THE DATA
        link = article.query_selector("a").get_attribute("href")
        # Open each article page
        article_page = browser.new_page()
        article_page.goto(link)
        
        # Scrape the content (assuming the content is within a specific selector)
        title = article_page.query_selector("h1.postH1.mb-5.uppercase").inner_text()

        featured_image = article_page.query_selector("div.editorSinglePost img:first-child").get_attribute("src") if article_page.query_selector("div.editorSinglePost img:first-child") else None

        images = article_page.query_selector_all("div.editorSinglePost img") if article_page.query_selector("div.editorSinglePost img") else []
        images = ', '.join(img.get_attribute("src") for img in images) if images else ''

        content = article_page.query_selector("div.editorSinglePost").inner_html()  # Adjust the selector as needed

        slug = link.split("/")[-2] # Assuming the slug is the last part of the URL without the .html extension


    
        data.append([slug, title, content, featured_image, images])  # Store link and content
        
        article_page.close()  # Close the article page after scraping

    # Create directories if they don't exist
    os.makedirs(f'csv/{sitename}', exist_ok=True)
    
    with open(f'csv/{sitename}/{fileDate}-articles.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Slug', 'Title', 'Content', 'Featured Image', 'Images'])
        writer.writerows(data)

    browser.close()
