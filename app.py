from flask import Flask, render_template, request, jsonify
import bots_logic
import threading

from flask import send_file  # Isay top par add karein
from flask import Flask
import os

app = Flask(__name__)
# --- Pages Routes ---


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/yt-viewer")
def yt_viewer_page():
    return render_template("yt_viewer.html")


@app.route("/downloader")
def downloader_page():
    return render_template("downloader.html")


@app.route("/price-tracker")
def price_tracker_page():
    return render_template("price_tracker.html")


# 1. Page Route
@app.route("/bg-remover")
def bg_remover_page():
    return render_template("bg_remover.html")


# 2. Upload & Process Route
@app.route("/api/remove-bg", methods=["POST"])
def handle_bg_removal():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "No selected file", 400

    # AI Process call karna
    result_io = bots_logic.remove_background(file)

    if result_io:
        return send_file(
            result_io,
            mimetype="image/png",
            as_attachment=True,
            download_name="no-bg.png",
        )
    else:
        return "Processing failed", 500


# --- Combined API Logic (No Duplication) ---


@app.route("/api/run-bot", methods=["POST"])
def handle_bot_requests():
    data = request.json
    bot_type = data.get("type")
    url = data.get("url")

    if not url:
        return jsonify({"msg": "URL/Link dena zaroori hai!"})

    # Logic for YouTube Viewer
    if bot_type == "yt_views":
        count = data.get("count", 1)
        # Threading taake GUI block na ho
        thread = threading.Thread(target=bots_logic.open_tabs, args=(url, count))
        thread.start()
        return jsonify({"msg": f"{count} Tabs khulna shuru ho gaye hain!"})

    # Logic for Downloader
    elif bot_type == "downloader":
        result = bots_logic.download_media(url)
        return jsonify({"msg": result})

    # Logic for Price Tracker
    elif bot_type == "price_tracker":
        result = bots_logic.check_price(url)
        return jsonify({"msg": f"Product: {result['name']} | Price: {result['price']}"})

    return jsonify({"msg": "Invalid Bot Type"})


# --- QR Generator Route ---
@app.route("/qr-generator")
def qr_page():
    return render_template("qr_gen.html")


@app.route("/api/generate-qr", methods=["POST"])
def handle_qr():
    text = request.json.get("text")
    if not text:
        return "Text is required", 400
    result_io = bots_logic.generate_qr(text)
    return send_file(
        result_io, mimetype="image/png", as_attachment=True, download_name="qrcode.png"
    )


# --- PDF Merger Route ---
@app.route("/pdf-merger")
def pdf_page():
    return render_template("pdf_merger.html")


@app.route("/api/merge-pdf", methods=["POST"])
def handle_pdf_merge():
    files = request.files.getlist("pdfs")
    if not files:
        return "Files are required", 400
    result_io = bots_logic.merge_pdfs(files)
    return send_file(
        result_io,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="merged.pdf",
    )


# --- YouTube Transcript Route ---
@app.route("/transcript-downloader")
def transcript_page():
    return render_template("transcript.html")


@app.route("/api/get-transcript", methods=["POST"])
def handle_transcript():
    url = request.json.get("url")
    text = bots_logic.get_yt_transcript(url)
    return jsonify({"text": text})


# --- TTS Route ---
@app.route("/text-to-speech")
def tts_page():
    return render_template("tts.html")


@app.route("/api/tts", methods=["POST"])
def handle_tts():
    text = request.json.get("text")
    if not text:
        return "Text is required", 400
    result_io = bots_logic.text_to_speech(text)
    return send_file(
        result_io, mimetype="audio/mpeg", as_attachment=True, download_name="speech.mp3"
    )


# --- Image Compressor Route ---
@app.route("/image-compressor")
def compress_page():
    return render_template("compressor.html")


@app.route("/api/compress", methods=["POST"])
def handle_compress():
    file = request.files.get("image")
    if not file:
        return "Image required", 400
    result_io = bots_logic.compress_image(file)
    return send_file(
        result_io,
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="compressed.jpg",
    )


# --- Fake Identity Route ---
@app.route("/fake-identity")
def fake_identity_page():
    return render_template("fake_identity.html")


@app.route("/api/generate-identity", methods=["POST"])
def handle_identity():
    profile = bots_logic.generate_fake_profile()
    return jsonify(profile)


# --- 17. AI Content Writer Routes ---
@app.route("/ai-writer")
def ai_writer_page():
    return render_template("ai_writer.html")


@app.route("/api/write-content", methods=["POST"])
def handle_ai_writer():
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"result": "Prompt is required!"})

    # Logic file se function call kiya
    result_text = bots_logic.ask_ai(prompt)
    return jsonify({"result": result_text})


# --- 18. IP/Website Locator Routes ---
@app.route("/ip-locator")
def ip_locator_page():
    return render_template("ip_locator.html")


@app.route("/api/locate-target", methods=["POST"])
def handle_location():
    data = request.json
    target = data.get("target")
    if not target:
        return jsonify({"status": "error", "msg": "Target is required!"})

    # Logic file se function call kiya
    info = bots_logic.locate_target(target)
    return jsonify(info)


# --- 21. Image Converter Routes ---
@app.route("/image-converter")
def converter_page():
    return render_template("converter.html")


@app.route("/api/convert-image", methods=["POST"])
def handle_converter():
    file = request.files.get("image")
    if not file:
        return "Image required", 400

    result_io = bots_logic.convert_image_format(file, "JPEG")
    return send_file(
        result_io,
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="converted_image.jpg",
    )


# --- 22. Secret Message Encryptor Routes ---
@app.route("/secret-message")
def secret_msg_page():
    return render_template("secret_msg.html")


@app.route("/api/encrypt-msg", methods=["POST"])
def handle_encryption():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required"})

    result = bots_logic.encrypt_message(text)
    return jsonify(result)


@app.route("/api/decrypt-msg", methods=["POST"])
def handle_decryption():
    data = request.json
    token = data.get("token")
    key = data.get("key")

    if not token or not key:
        return jsonify({"result": "Both Secret Code and Key are required!"})

    result = bots_logic.decrypt_message(token, key)
    return jsonify({"result": result})


# --- Plagiarism Checker ---
@app.route("/plagiarism-checker")
def plagiarism_page():
    return render_template("plagiarism.html")


@app.route("/api/check-plagiarism", methods=["POST"])
def handle_plagiarism():
    text = request.json.get("text")

    if not text:
        return jsonify({"error": "Text is required"})

    result = bots_logic.check_plagiarism(text)
    return jsonify(result)


# --- Instagram Bio Generator ---
@app.route("/instagram-bio")
def instagram_bio_page():
    return render_template("insta_bio.html")


@app.route("/api/generate-bio", methods=["POST"])
def handle_instagram_bio():
    data = request.json

    niche = data.get("niche")
    tone = data.get("tone")
    keywords = data.get("keywords")
    emoji = data.get("emoji", True)

    if not niche or not tone:
        return jsonify({"error": "Niche and Tone are required"})

    result = bots_logic.generate_instagram_bio(niche, tone, keywords, emoji)
    return jsonify({"result": result})


# --- Hashtag Generator ---
@app.route("/hashtag-generator")
def hashtag_page():
    return render_template("hashtag.html")


@app.route("/api/generate-hashtags", methods=["POST"])
def handle_hashtags():
    data = request.json

    topic = data.get("topic")
    platform = data.get("platform")
    tone = data.get("tone")

    if not topic or not platform:
        return jsonify({"error": "Topic and Platform required"})

    result = bots_logic.generate_hashtags(topic, platform, tone)
    return jsonify({"result": result})


# --- Text Summarizer ---
@app.route("/text-summarizer")
def summarizer_page():
    return render_template("summarizer.html")


@app.route("/api/summarize", methods=["POST"])
def handle_summarizer():
    data = request.json

    text = data.get("text")
    mode = data.get("mode", "short")
    percentage = data.get("percentage", 50)

    if not text:
        return jsonify({"error": "Text is required"})

    result = bots_logic.summarize_text(text, mode, percentage)
    return jsonify({"result": result})


# --- PDF to Word Converter ---
@app.route("/pdf-to-word")
def pdf_to_word_page():
    return render_template("pdf_to_word.html")


@app.route("/api/pdf-to-word", methods=["POST"])
def handle_pdf_to_word():
    file = request.files.get("pdf")

    if not file:
        return "PDF file required", 400

    result_io = bots_logic.convert_pdf_to_word(file)

    if result_io:
        return send_file(
            result_io,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name="converted.docx"
        )

    return "Conversion failed", 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
