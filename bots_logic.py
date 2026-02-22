import webbrowser
import time

import yt_dlp
import os

from pdf2docx import Converter
import tempfile

import requests
from bs4 import BeautifulSoup

import io
from rembg import remove
from PIL import Image

import qrcode
from PyPDF2 import PdfMerger
import io

from youtube_transcript_api import YouTubeTranscriptApi
import re

from gtts import gTTS
from PIL import Image
import io

from faker import Faker

import google.generativeai as genai
import requests
from urllib.parse import urlparse

from cryptography.fernet import Fernet



def open_tabs(url, count):
    for i in range(int(count)):
        webbrowser.open_new_tab(url)
        time.sleep(2)


def download_media(url):
    try:
        # Downloads folder ka path set karna
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # yt-dlp ki settings
        ydl_opts = {
            "format": "best",  # Sab se achi quality
            "outtmpl": f"{download_path}/%(title)s.%(ext)s",  # File name aur location
            "noplaylist": True,  # Agar playlist ho toh sirf ek video
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            ydl.download([url])

        return "Success! Video aapke 'Downloads' folder mein save ho gayi hai."

    except Exception as e:
        return f"Error: {str(e)}"


def check_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        # Amazon/Flipkart ke price selectors (Ye waqt ke sath badal sakte hain)
        # Hum common selectors check kar rahe hain
        price_selectors = [
            ".a-price-whole",
            ".a-offscreen",
            "._30jeq3._16Jk6d",
            "span.price",
            "#priceblock_ourprice",
        ]

        price = "Price Not Found"
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price = element.get_text().strip()
                break

        # Product Title nikalna
        title = soup.find(id="productTitle")
        if not title:
            title = soup.find("span", {"class": "B_NuCI"})  # Flipkart title

        product_name = title.get_text().strip() if title else "Product"

        return {"name": product_name[:50] + "...", "price": price}

    except Exception as e:
        return {"name": "Error", "price": str(e)}


def remove_background(input_file):
    try:
        # Image ko open karna
        input_image = Image.open(input_file)

        # AI ke zariye background remove karna
        output_image = remove(input_image)

        # Output ko bytes mein convert karna taake website par wapas bheja ja sake
        img_io = io.BytesIO()
        output_image.save(img_io, "PNG")
        img_io.seek(0)

        return img_io
    except Exception as e:
        print(f"Error removing background: {e}")
        return None


# --- 5. QR Code Generator Logic ---
def generate_qr(text):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return img_io
    except Exception as e:
        print(f"QR Error: {e}")
        return None


# --- 6. PDF Merger Logic ---
def merge_pdfs(pdf_list):

    try:
        merger = PdfMerger()
        for pdf in pdf_list:
            merger.append(pdf)

        pdf_io = io.BytesIO()
        merger.write(pdf_io)
        pdf_io.seek(0)
        return pdf_io
    except Exception as e:
        print(f"PDF Error: {e}")
        return None


# --- 7. YouTube Transcript Logic ---
def get_yt_transcript(url):
    try:
        # Video ID nikalne ka behtareen tareeqa (Regex)
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not video_id_match:
            return "Error: Link sahi nahi hai. Video ID nahi mili."

        video_id = video_id_match.group(1)

        # Library call
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Text jama karna
        full_text = " ".join([segment["text"] for segment in transcript_list])
        return full_text

    except Exception as e:
        return f"Error: Transcript nahi mil saki. Wajah: Captions is video par band ho sakte hain."


# --- 9. AI Text-to-Speech Logic ---
def text_to_speech(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        return audio_io
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


# --- 10. Image Compressor Logic ---
def compress_image(input_file, quality=20):
    try:
        img = Image.open(input_file)
        # Agar image RGBA (transparent) hai toh usay RGB mein convert karna (Optional)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img_io = io.BytesIO()
        # Quality kam karke save karna
        img.save(img_io, "JPEG", optimize=True, quality=quality)
        img_io.seek(0)
        return img_io
    except Exception as e:
        print(f"Compress Error: {e}")
        return None


# --- 16. Fake Identity Generator Logic ---
def generate_fake_profile():
    fake = Faker()
    return {
        "name": fake.name(),
        "address": fake.address().replace("\n", ", "),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "job": fake.job(),
        "country": fake.country(),
    }


# --- 17. AI Content Writer Logic ---
GOOGLE_API_KEY = "AIzaSyDIsolWsptduPjwO5BZaqmog4WUCn6KbeQ"


# --- 17. AI Content Writer Logic ---
# --- 17. AI Content Writer Logic (Updated) ---
def ask_ai(prompt):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)

        # Available model khud dhundne ki koshish karein
        model_name = "gemini-1.5-flash"  # Default try

        # Fallback: Agar default fail ho jaye to safe model use karein
        try:
            # List check karke pehla valid model utha lo
            available_models = [
                m.name
                for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
            ]
            # Prefer flash or pro
            for m in available_models:
                if "flash" in m:
                    model_name = m
                    break
                elif "pro" in m:
                    model_name = m
                    break
        except:
            pass  # Agar list fail hui to default "gemini-1.5-flash" hi try karega

        # Model initialize karein
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


# --- 18. IP/Website Locator Logic ---
def locate_target(target):
    try:
        # Agar URL hai toh domain nikalna, warna direct IP use karna
        if "http" in target or "www" in target:
            # Agar http nahi hai to lagayein taake urlparse kaam kare
            if not target.startswith("http"):
                target = "http://" + target
            target = urlparse(target).netloc

        url = f"http://ip-api.com/json/{target}"
        response = requests.get(url).json()

        if response["status"] == "success":
            return {
                "status": "success",
                "country": response.get("country"),
                "city": response.get("city"),
                "isp": response.get("isp"),
                "lat": response.get("lat"),
                "lon": response.get("lon"),
                "ip": response.get("query"),
                "region": response.get("regionName"),
            }
        return {"status": "fail", "msg": "Invalid IP or Website"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}


# --- 21. Image Converter Logic (PNG to JPG) ---
def convert_image_format(image_file, target_format="JPEG"):
    try:
        img = Image.open(image_file)
        # Transparency hatana (PNG -> JPG ke liye)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        output_io = io.BytesIO()
        img.save(output_io, format=target_format, quality=95)
        output_io.seek(0)
        return output_io
    except Exception as e:
        print(e)
        return None


# --- 22. Secret Message Encryptor Logic ---
def encrypt_message(message):
    try:
        # Key generate karein
        key = Fernet.generate_key()
        f = Fernet(key)

        # Message ko bytes mein convert karke encrypt karein
        token = f.encrypt(message.encode())

        # Return: Key aur Encrypted Message dono string format mein
        return {"key": key.decode(), "secret_msg": token.decode()}
    except Exception as e:
        return {"error": str(e)}


def decrypt_message(token, key):
    try:
        f = Fernet(key.encode())
        # Decrypt karein
        message = f.decrypt(token.encode())
        return message.decode()
    except Exception as e:
        return "Error: Wrong Key or Corrupted Message!"


import requests
from bs4 import BeautifulSoup
import difflib
import re

def check_plagiarism(text):
    try:
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        plagiarised_count = 0
        total_checked = 0

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        for sentence in sentences[:5]:  # Limit to avoid blocking
            query = sentence[:100]
            url = f"https://www.google.com/search?q=\"{query}\""

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            results = soup.find_all("span")

            for result in results:
                similarity = difflib.SequenceMatcher(None, sentence.lower(), result.text.lower()).ratio()
                if similarity > 0.8:
                    plagiarised_count += 1
                    break

            total_checked += 1

        if total_checked == 0:
            return {"score": 0, "status": "Not enough text"}

        percentage = (plagiarised_count / total_checked) * 100

        return {
            "score": round(percentage, 2),
            "status": "High plagiarism" if percentage > 50 else "Low plagiarism"
        }

    except Exception as e:
        return {"error": str(e)}

# instaram bio generator logic
def generate_instagram_bio(niche, tone, keywords, emoji=True):
    try:
        emoji_text = "Include emojis." if emoji else "Do not include emojis."

        prompt = f"""
        Generate 5 unique Instagram bios.
        Niche: {niche}
        Tone: {tone}
        Keywords: {keywords}
        {emoji_text}

        Keep each bio under 150 characters.
        Make them stylish and creative.
        """

        result = ask_ai(prompt)
        return result

    except Exception as e:
        return f"Error: {str(e)}"
    
# hashtag generator logic
def generate_hashtags(topic, platform, tone):
    try:
        prompt = f"""
        Generate 30 SEO optimized hashtags for {platform}.
        Topic: {topic}
        Tone: {tone}

        Format:
        🔥 High Reach (10 hashtags)
        🎯 Medium Reach (10 hashtags)
        💎 Niche (10 hashtags)

        Only return hashtags.
        """

        result = ask_ai(prompt)
        return result

    except Exception as e:
        return f"Error: {str(e)}"


# summary shortener logic 
def summarize_text(text, mode="short", percentage=50):
    try:
        if mode == "short":
            instruction = "Summarize this text in a short paragraph."
        elif mode == "detailed":
            instruction = "Provide a detailed summary of this text."
        elif mode == "bullet":
            instruction = "Summarize this text in clear bullet points."
        elif mode == "insights":
            instruction = "Extract key insights and important points from this text."
        elif mode == "percentage":
            instruction = f"Summarize this text and reduce it to approximately {percentage}% of its original length."
        else:
            instruction = "Summarize this text."

        prompt = f"""
        {instruction}

        Text:
        {text}
        """

        result = ask_ai(prompt)
        return result

    except Exception as e:
        return f"Error: {str(e)}"

# pdf to word converter logic 
def convert_pdf_to_word(pdf_file):
    try:
        # Temporary file save
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            pdf_file.save(temp_pdf.name)
            temp_pdf_path = temp_pdf.name

        temp_docx_path = temp_pdf_path.replace(".pdf", ".docx")

        # Convert PDF → DOCX
        cv = Converter(temp_pdf_path)
        cv.convert(temp_docx_path, start=0, end=None)
        cv.close()

        # Read docx into memory
        with open(temp_docx_path, "rb") as f:
            docx_io = io.BytesIO(f.read())

        docx_io.seek(0)

        # Cleanup
        os.remove(temp_pdf_path)
        os.remove(temp_docx_path)

        return docx_io

    except Exception as e:
        print("PDF to Word Error:", e)
        return None


