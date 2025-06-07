import streamlit as st
import time
from datetime import datetime
import pandas as pd
import numpy as np
import io
from PIL import Image
import json
import requests
import os
import random
import base64
from io import BytesIO
import google.genai as genai
from google.genai import types

def detect_emotion(text):
    """Analyze emotion from text using Gemini API, fallback to rule-based if needed"""
    api_key = st.secrets['GEMINI_API_KEY']
    prompt = (
        "Analyze the following text and return the primary emotion (one of: joy, sadness, anger, fear, surprise) "
        "and an intensity value between 0 and 1. "
        "Respond in JSON as: {\"emotion\": <emotion>, \"intensity\": <float>}\n"
        f"Text: {text}"
    )
    try:
        # Try to use Gemini AI for emotion detection
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        content = response.text
        import json as _json
        emotion_data = _json.loads(content)
        return emotion_data
    except Exception as e:
        st.warning(f"Falling back to simple emotion detection due to error: {e}")
        # Simple keyword-based fallback when API fails
        text_lower = text.lower()
        if any(word in text_lower for word in ["happy", "joy", "delight", "excited", "pleased"]):
            primary_emotion = "joy"
            intensity = 0.9
        elif any(word in text_lower for word in ["sad", "down", "unhappy", "depressed", "cry"]):
            primary_emotion = "sadness"
            intensity = 0.85
        elif any(word in text_lower for word in ["angry", "mad", "furious", "rage", "annoyed"]):
            primary_emotion = "anger"
            intensity = 0.8
        elif any(word in text_lower for word in ["afraid", "scared", "fear", "terrified", "nervous"]):
            primary_emotion = "fear"
            intensity = 0.8
        elif any(word in text_lower for word in ["surprised", "amazed", "astonished", "shocked"]):
            primary_emotion = "surprise"
            intensity = 0.75
        else:
            primary_emotion = "joy"
            intensity = 0.6
        return {"emotion": primary_emotion, "intensity": intensity}

def generate_composite_image(emotions_detected):
    """
    Generate an image using Gemini API based on the detected emotions.
    Returns a PIL Image object.
    """
    # Create a summary of emotions for the image prompt
    emotion_summary = ', '.join([f"{e['emotion']} ({int(e['intensity']*100)}%)" for e in emotions_detected])
    prompt = (
        f"Create a beautiful, artistic image that visually represents the following emotions and their intensities: {emotion_summary}. "
        f"Use a {st.session_state.animation_theme} theme. The image should be abstract, vibrant, and emotionally expressive."
    )
    
    # Create fallback image based on primary emotion
    try:
        primary_emotion = emotions_detected[0]["emotion"] if emotions_detected else "joy"
        # Map each emotion to a specific color scheme
        emotion_colors = {
            "joy": (255, 223, 0),      # Yellow
            "sadness": (0, 119, 190),  # Blue
            "anger": (214, 39, 40),    # Red
            "fear": (148, 0, 211),     # Purple
            "surprise": (44, 160, 44)  # Green
        }
        color = emotion_colors.get(primary_emotion, (200, 200, 200))
        
        # Try to use Gemini API first
        try:
            api_key = st.secrets['GEMINI_API_KEY']
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            # Extract image from response
            for part in response.candidates[0].content.parts:
                if getattr(part, 'inline_data', None) is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    return image
            raise Exception("No image data returned from Gemini API.")
        except Exception as e:
            st.error(f"Failed to generate image with Gemini: {e}")
            
            # Create a gradient fallback image when API fails
            img = Image.new("RGB", (512, 512))
            for y in range(512):
                for x in range(512):
                    # Create gradient effect based on emotion color
                    r = int(color[0] * (1 - y/512))
                    g = int(color[1] * (1 - x/512))
                    b = int(color[2] * (1 - (x+y)/1024))
                    img.putpixel((x, y), (r, g, b))
                    
            # Add text overlay
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("Arial", 20)
            except:
                font = ImageFont.load_default()
                
            # Add descriptive text
            text = f"Emotional Symphony: {primary_emotion.capitalize()}"
            draw.text((100, 240), text, fill=(255, 255, 255), font=font)
            
            theme_text = f"Theme: {st.session_state.animation_theme.capitalize()}"
            draw.text((100, 280), theme_text, fill=(255, 255, 255), font=font)
            
            draw.text((100, 320), emotion_summary, fill=(255, 255, 255), font=font)
            
            st.info("Created a custom emotional image due to Gemini API limitations.")
            return img
    except Exception as e:
        # Final fallback - plain colored image
        st.error(f"Error in image generation: {e}")
        return Image.new("RGB", (512, 512), color=(200, 200, 200))

# Set page configuration
st.set_page_config(
    page_title="Emotional Symphony",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the UI
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton button {
        background-color: #5c6bc0;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    div[data-testid="stSidebarNav"] {
        background-image: linear-gradient(#5c6bc0, #3949ab);
        color: white;
        padding: 1rem;
        border-radius: 5px;
    }
    .story-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #5c6bc0;
        margin: 10px 0px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .emotion-pill {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .emotion-joy {
        background-color: #FFEB3B;
        color: #212121;
    }
    .emotion-sadness {
        background-color: #90CAF9;
        color: #212121;
    }
    .emotion-anger {
        background-color: #EF5350;
        color: white;
    }
    .emotion-fear {
        background-color: #9C27B0;
        color: white;
    }
    .emotion-surprise {
        background-color: #66BB6A;
        color: white;
    }
    .app-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #3949ab, #5c6bc0);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'story_entries' not in st.session_state:
    st.session_state.story_entries = []
if 'emotions_detected' not in st.session_state:
    st.session_state.emotions_detected = []
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "setup"  # setup, input, generate, share
if 'animation_generated' not in st.session_state:
    st.session_state.animation_generated = False
if 'final_video' not in st.session_state:
    st.session_state.final_video = None
if 'animation_theme' not in st.session_state:
    st.session_state.animation_theme = "forest"  # default theme
if 'user_name' not in st.session_state:
    st.session_state.user_name = "You"

# Header
st.markdown("<div class='app-header'><h1>🎵 Emotional Symphony 🎶</h1><p>A music storytelling platform</p></div>", unsafe_allow_html=True)

# Sidebar for information and controls
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=ES", width=150)
    st.title("About")
    st.info("""
    Emotional Symphony is a platform where you can create unique musical stories based on your emotional expressions.
    
    Input your emotions through text, and watch as the system generates matching music and animations!
    """)

    
    if st.session_state.current_stage != "setup":
        st.subheader("⚙️ Settings")
        st.session_state.animation_theme = st.selectbox(
            "Animation Theme",
            ["forest", "ocean", "neon"],
            index=["forest", "ocean", "neon"].index(st.session_state.animation_theme)
        )

# Main content - Stage-based workflow
if st.session_state.current_stage == "setup":
    st.subheader("Let's create your Emotional Symphony!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personalize Your Experience")
        username = st.text_input("Your Name (Optional)", value="You")
        st.session_state.user_name = username if username else "You"
        
    with col2:
        st.markdown("### Choose Your Story Elements")
        st.session_state.animation_theme = st.selectbox(
            "Animation Theme",
            ["forest", "ocean", "neon"]
        )
        
        st.markdown("### Privacy Notice")
        st.checkbox("I understand that my emotional text inputs will be processed to generate content, but no personal data will be stored.", value=True)
    
    if st.button("Start Creating", key="start_create"):
        st.session_state.current_stage = "input"
        st.rerun()

elif st.session_state.current_stage == "input":
    st.markdown(f"## Your Emotional Expression")
    st.markdown("Express your current emotional state. What are you feeling right now?")
    user_text = st.text_area("Your response:", height=100)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Submit", key="submit_emotion"):
            if user_text.strip():
                # Process user input and detect emotion
                emotion_data = detect_emotion(user_text)
                entry = {
                    "user": st.session_state.user_name,
                    "text": user_text,
                    "emotion": emotion_data,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.story_entries = [entry]
                st.session_state.emotions_detected = [emotion_data]
                st.session_state.current_stage = "generate"
                st.rerun()
            else:
                st.error("Please enter some text before submitting.")
    
    # Display previous entry if exists
    if st.session_state.story_entries:
        entry = st.session_state.story_entries[0]
        emotion = entry["emotion"]["emotion"]
        intensity = entry["emotion"]["intensity"]
        emotion_class = f"emotion-{emotion}"
        st.markdown(f"""
        <div class='story-card'>
            <h4>Your Entry <span style='font-size:0.8rem;color:gray;'>{entry['timestamp']}</span></h4>
            <p>{entry['text']}</p>
            <div>
                <span class='emotion-pill {emotion_class}'>{emotion.capitalize()} ({int(intensity*100)}%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_stage == "generate":
    st.markdown("## Generating Your Emotional Symphony")
    if not st.session_state.animation_generated:
        with st.spinner(f"Creating {st.session_state.animation_theme}-themed animation..."):
            # Simulate generation process
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            # Generate image based on emotions
            final_image = generate_composite_image(st.session_state.emotions_detected)
            st.session_state.final_image = final_image
            st.session_state.animation_generated = True
            st.success("Animation creation complete!")
            
            # Play random background music
            music_dir = "static/music"
            if os.path.exists(music_dir):
                mp3_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
                if mp3_files:
                    random_music_path = os.path.join(music_dir, random.choice(mp3_files))
                    with open(random_music_path, 'rb') as f:
                        audio_bytes = f.read()
                    
                    # Encode audio for HTML5 autoplay
                    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                    
                    # Hidden audio player with autoplay
                    audio_html = f"""
                    <audio autoplay style="display:none">
                      <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.session_state.animation_generated:
        st.markdown("## Your Emotional Symphony is Ready!")
        st.image(st.session_state.final_image, use_column_width=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Continue to Share Options"):
                st.session_state.current_stage = "share"
                st.rerun()
        with col2:
            if st.button("Create a New Emotional Symphony"):
                # Reset all session states
                st.session_state.story_entries = []
                st.session_state.emotions_detected = []
                st.session_state.current_stage = "setup"
                st.session_state.animation_generated = False
                st.session_state.final_video = None
                st.rerun()

elif st.session_state.current_stage == "share":
    st.markdown("## Share Your Emotional Symphony")
    
    # Display final generated image
    st.image(st.session_state.final_image, use_column_width=True)
    
    # Play background music again for the share page
    music_dir = "static/music"
    if os.path.exists(music_dir):
        mp3_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        if mp3_files:
            random_music_file = random.choice(mp3_files)
            random_music_path = os.path.join(music_dir, random_music_file)
            with open(random_music_path, 'rb') as f:
                audio_bytes = f.read()
            
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            audio_html = f"""
            <audio autoplay style="display:none">
              <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
    
    # Display emotional journey summary
    st.markdown("### Your Emotional Journey")
    entry = st.session_state.story_entries[0]
    st.markdown(f"**Your Entry**: {entry['text']}")
    
    st.markdown("### Your Emotional Palette")
    emotion = entry["emotion"]["emotion"]
    st.markdown(f"- **{emotion.capitalize()}**")
    
    # Download options
    st.markdown("### Save Your Creation")
    col1, col2 = st.columns(2)
    
    with col1:
        # Convert PIL Image to bytes for download
        img_byte_arr = io.BytesIO()
        st.session_state.final_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name="emotional_symphony.png",
            mime="image/png"
        )
    
    with col2:
        # Export story data as JSON
        storyboard_json = json.dumps(st.session_state.story_entries, indent=2)
        st.download_button(
            label="Download Storyboard (JSON)",
            data=storyboard_json,
            file_name="emotional_symphony_storyboard.json",
            mime="application/json"
        )
    
    # Restart button
    if st.button("Create a New Emotional Symphony"):
        st.session_state.story_entries = []
        st.session_state.emotions_detected = []
        st.session_state.current_stage = "setup"
        st.session_state.animation_generated = False
        st.session_state.final_video = None
        st.rerun()
