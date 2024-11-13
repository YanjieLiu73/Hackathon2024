from pptx import Presentation
from pptx.util import Pt
import streamlit as st
import os
import json
import sys
from fpdf import FPDF
from mistletoe import markdown
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage)
verbose_txt_sample_path = os.path.join(os.path.dirname(__file__), '..', '..', 'AutoGen', 'backend', 'ui_sample_output')
sys.path.append(verbose_txt_sample_path)

llm = AzureChatOpenAI(
    model="gpt-4o",
    azure_endpoint="https://genai-openai-quantifai.openai.azure.com/",
    openai_api_key="1b31fc4eb58c4879960c46f697d72af6",
    api_version="2024-02-01",
    verbose=False,
    temperature=0.0)

def get_summary(verbose_txt, title, testing=False):

    if testing:
        with open(verbose_txt_sample_path+'/slides_titles_text.json', 'r') as f:
            responses = json.load(f)
        concise_txt = responses.get(title, "None")
    else:
        messages = [SystemMessage(content = f"You are an expert in summarizing documents into a format which is appropriate for a single presentation slide."),
                    HumanMessage(content = f"Please provide a concise summary of the following text in bullet points: {verbose_txt}. Use at most 7 bullet points!")]
        response = llm(messages = messages, temperature = 0)
        concise_txt = response.content
    
    return concise_txt

# Function to save content to a PowerPoint file
def save_content_to_ppt(filename="result/Profiler_Slides.pptx"):
    # Ensure the result directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Create a PowerPoint presentation
    path = 'template_barclays.pptx'
    prs = Presentation(path)

    possible_slides = ["Overview", "Financials", "Geographic Mix", "Management",
                       "Recent News", "M&A Profile", "Miscellanea", "Discounted Cash Flow Analysis", "Leveraged Buyout Analysis"]

    for title in possible_slides:
        if st.session_state.get(title, False):

            # Add a slide for each section
            slide = prs.slides.add_slide(prs.slide_layouts[15])
            title_placeholder = slide.placeholders[0]
            content_placeholder = slide.placeholders[14]

            # Set the title and content
            title_placeholder.text = title
            content_placeholder.text = get_summary(st.session_state[title], title, False)

            for paragraph in content_placeholder.text_frame.paragraphs:
                paragraph.font.size = Pt(12)
                paragraph.space_before = Pt(10)

    # Save the presentation
    prs.save(filename)

# Function to save content to a PowerPoint file
def save_content_to_pdf(filename="result/Profiler_Report.pdf"):

    possible_slides = ["Overview", "Financials", "Geographic Mix", "Management",
                       "Recent News", "M&A Profile", "Miscellanea", "Discounted Cash Flow Analysis", "Leveraged Buyout Analysis"]
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("dejavu-sans", style="", fname="font/DejaVuSans.ttf")
    pdf.add_font("dejavu-sans", style="b", fname="font/DejaVuSans-Bold.ttf")
    for title in possible_slides:
        if st.session_state.get(title, False):

            html_text = markdown(st.session_state[title])
            html_text = html_text.replace('<h3>', '<h3 style="color: grey;">')
            pdf.set_font(family="dejavu-sans", style="b", size=20)
            pdf.cell(200, 10, txt = title, ln = 1, align = 'C')
            pdf.set_font(family="dejavu-sans", style="", size=12)
            pdf.write_html(html_text)
    # save the pdf with name .pdf
    pdf.output(filename)   