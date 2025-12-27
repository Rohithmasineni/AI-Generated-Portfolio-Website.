import streamlit as st
import dotenv
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
import zipfile

from dotenv import load_dotenv # this helps accessing all the variables present in .env file

load_dotenv() #* load your any .env file to your current environment, then this .py file can access all the values inside the environment

# As environment variables only can be accessed by Operating System (OS), we set the environment
import os #*
os.environ['GOOGLE_API_KEY'] = os.getenv('gemini') #*

st.set_page_config(page_title = 'AI website Creation', page_icon = '🤖')

st.title('AI-Powered Website Builder')


prompt = st.text_area('Write about the website you want to create')

if st.button('Generate'):
    message = [('system', """
                You are an expert full-stack web developer specializing in building 
                modern, responsive, mobile-friendly personal portfolio websites.

                Your task is to generate a complete frontend website (HTML, CSS, JS) 
                based strictly on the user’s instructions. 
                Follow these rules:

                ========================
                ### GENERAL REQUIREMENTS
                ========================
                1. The website must look professional, modern, and clean.
                2. Use fully responsive design (works on desktop & mobile).
                3. Include smooth animations, hover effects, and transitions.
                4. Use semantic HTML5 structure (header, section, footer, nav).
                5. Ensure clean CSS with comments and organized structure.
                6. JavaScript should enhance UI (nav toggle, animations, scroll effects).
                7. No placeholders like "Lorem Ipsum" — use meaningful custom content.
                8. No unnecessary external libraries unless the user explicitly asks.

                ========================
                ### CUSTOMIZATION LOGIC
                ========================
                Based on the user's prompt, dynamically generate:
                - A personalized "About Me" section.
                - A professional tagline/hero section.
                - Skills section (convert user skills into neat UI blocks).
                - Projects section (each with title, description, tech used).
                - Contact section (include working form structure).
                - Theme Colors (based on user taste if provided).
                - Typography (pick visually appealing Google Fonts).
                - Optional sections (Experience, Education, Services, Testimonials) if user mentions them.

                ========================
                ### OUTPUT FORMAT (MANDATORY)
                ========================
                Your response **must follow EXACTLY this structure**:

                Start the HTML code block with:
                ---html---
                [HTML CODE HERE]
                ---html---

                Start the CSS code block with:
                ---css---
                [CSS CODE HERE]
                ---css---

                Start the JavaScript code block with:
                ---js---
                [JS CODE HERE]
                ---js---

                DO NOT add any explanations or text outside the required blocks.
                DO NOT repeat the user's prompt.
                DO NOT include markdown code fences.

                ========================
                ### 📌 HTML REQUIREMENTS
                ========================
                - Include a hero section with name, title, and CTA button.
                - Navigation bar with mobile menu toggle.
                - About section with detailed bio.
                - Skills section with clean grid layout.
                - Projects with cards, images (use meaningful placeholder images).
                - Contact section with form fields.
                - Footer with social links based on user prompt.

                ========================
                ### 📌 CSS REQUIREMENTS
                ========================
                - Use modern layouts (Flexbox/Grid).
                - Responsive breakpoints for mobile.
                - Smooth hover effects & transitions.
                - A color palette matching user's style (dark theme, minimal, luxury, vibrant, etc.).

                ========================
                ### 📌 JS REQUIREMENTS
                ========================
                - Mobile menu toggle.
                - Smooth scrolling.
                - Optional animation on scroll (fade-in effects).
                - No external frameworks unless asked.

                Follow instructions exactly.
                """)] 
    
    message.append(('user', prompt))
    
    model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite')
    
    response = model.invoke(message)
    
    # to see the output
    # with open('file.txt', 'w') as file:
    #     file.write(response.content)    # We do not need this code block, as everyting is in response varibale 
    
    with open('index.html', 'w') as file:
        file.write(response.content.split('---html---')[1])
        
    with open('style.css', 'w') as file:
        file.write(response.content.split('---css---')[1])
        
    with open('script.js', 'w') as file:
        file.write(response.content.split('---js---')[1])
        
    with zipfile.ZipFile('WebSite.zip','w') as zip:
        zip.write('index.html')
        zip.write('style.css')
        zip.write('script.js')
        
    st.download_button('Click Here to Download', 
                          data = open('WebSite.zip', 'rb'),
                          file_name = 'WebSite.zip') 
        
    st.write('success')
    
        
    