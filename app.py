import streamlit as st
import time
import random
import base64
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io
from PIL import Image

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

# Initialize session state variables if they don't exist
if 'story_entries' not in st.session_state:
    st.session_state.story_entries = []
if 'emotions_detected' not in st.session_state:
    st.session_state.emotions_detected = []
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "setup"  # setup, input, generate, share
if 'music_generated' not in st.session_state:
    st.session_state.music_generated = False
if 'animation_generated' not in st.session_state:
    st.session_state.animation_generated = False
if 'final_video' not in st.session_state:
    st.session_state.final_video = None
if 'animation_theme' not in st.session_state:
    st.session_state.animation_theme = "forest"  # default theme
if 'current_entry_number' not in st.session_state:
    st.session_state.current_entry_number = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = "You"

# Mock functions for emotion detection and media generation
def detect_emotion(text):
    """Mock function to detect emotion from text"""
    emotions = ["joy", "sadness", "anger", "fear", "surprise"]
    primary_emotion = random.choice(emotions)
    intensity = random.uniform(0.6, 0.95)
    return {"emotion": primary_emotion, "intensity": intensity}

def generate_music_snippet(emotion, intensity):
    """Mock function to generate music based on emotion"""
    # In a real implementation, this would connect to a music generation API
    return {
        "tempo": 60 + (intensity * 80) if emotion in ["joy", "surprise"] else 100 - (intensity * 40),
        "key": random.choice(["C major", "A minor", "F major", "D minor"]),
        "instruments": ["piano", "strings"] if emotion in ["sadness", "fear"] else ["guitar", "drums", "synth"]
    }

def create_forest_animation(emotions):
    """Generate a forest-themed animation based on emotions"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Background color based on overall emotion
    dominant_emotion = max(set([e["emotion"] for e in emotions]), key=[e["emotion"] for e in emotions].count)
    bg_colors = {
        "joy": "#e6f7ff",  # Light blue sky
        "sadness": "#c6d7eb",  # Gray-blue sky
        "anger": "#ffcccc",  # Red-tinted sky
        "fear": "#e0e0e0",  # Dark gray sky
        "surprise": "#e6ffe6"  # Light green sky
    }
    ax.set_facecolor(bg_colors.get(dominant_emotion, "#f0f0f0"))
    
    # Add trees
    n_trees = 15
    tree_positions = [(random.uniform(0, 10), random.uniform(0, 4)) for _ in range(n_trees)]
    tree_sizes = [random.uniform(1.0, 2.5) for _ in range(n_trees)]
    tree_colors = []
    
    for e in emotions:
        if e["emotion"] == "joy":
            tree_colors.append("#228B22")  # Forest green
        elif e["emotion"] == "sadness":
            tree_colors.append("#556B2F")  # Dark olive green
        elif e["emotion"] == "anger":
            tree_colors.append("#8B4513")  # Saddle brown
        elif e["emotion"] == "fear":
            tree_colors.append("#2F4F4F")  # Dark slate gray
        elif e["emotion"] == "surprise":
            tree_colors.append("#32CD32")  # Lime green
    
    # Ensure we have enough colors
    while len(tree_colors) < n_trees:
        tree_colors.append(random.choice(tree_colors))
    
    # Draw trees
    for i in range(n_trees):
        x, y = tree_positions[i]
        size = tree_sizes[i]
        color = tree_colors[i % len(tree_colors)]
        
        # Tree trunk
        ax.add_patch(plt.Rectangle((x-0.2*size, y), 0.4*size, 1.5*size, color="#8B4513"))
        
        # Tree foliage (triangle)
        ax.add_patch(plt.Polygon([
            (x, y+4*size),
            (x-1.5*size, y+1*size),
            (x+1.5*size, y+1*size)
        ], color=color))
        
        ax.add_patch(plt.Polygon([
            (x, y+5*size),
            (x-1.2*size, y+2.5*size),
            (x+1.2*size, y+2.5*size)
        ], color=color))
    
    # Ground
    ax.add_patch(plt.Rectangle((0, 0), 10, 1, color="#8B4513"))
    ax.add_patch(plt.Rectangle((0, 0), 10, 0.3, color="#A0522D"))
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)

def create_ocean_animation(emotions):
    """Generate an ocean-themed animation based on emotions"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Sky color based on overall emotion
    dominant_emotion = max(set([e["emotion"] for e in emotions]), key=[e["emotion"] for e in emotions].count)
    sky_colors = {
        "joy": "#87CEEB",  # Sky blue
        "sadness": "#4682B4",  # Steel blue
        "anger": "#4A0000",  # Dark red
        "fear": "#191970",  # Midnight blue
        "surprise": "#ADD8E6"  # Light blue
    }
    ax.set_facecolor(sky_colors.get(dominant_emotion, "#87CEEB"))
    
    # Ocean color and waves based on emotions
    avg_intensity = sum([e["intensity"] for e in emotions]) / len(emotions)
    wave_height = 2 + avg_intensity * 3
    
    ocean_colors = {
        "joy": "#1E90FF",  # Bright blue
        "sadness": "#000080",  # Navy blue
        "anger": "#006666",  # Dark teal
        "fear": "#000033",  # Very dark blue
        "surprise": "#00BFFF"  # Deep sky blue
    }
    ocean_color = ocean_colors.get(dominant_emotion, "#1E90FF")
    
    # Draw ocean
    ax.add_patch(plt.Rectangle((0, 0), 10, 6, color=ocean_color))
    
    # Draw waves
    x = np.linspace(0, 10, 1000)
    wave_count = int(3 + avg_intensity * 5)
    
    for i in range(wave_count):
        amplitude = random.uniform(0.2, 0.5) * avg_intensity
        frequency = random.uniform(1, 3)
        phase = random.uniform(0, 2*np.pi)
        y_position = 5.5 - i * 0.5
        
        y = amplitude * np.sin(frequency * x + phase) + y_position
        ax.plot(x, y, color='white', alpha=0.5, linewidth=2)
    
    # Draw sun/moon
    if dominant_emotion in ["joy", "surprise"]:
        # Sun
        circle = plt.Circle((8, 8), 0.8, color='#FFFF00')
    else:
        # Moon
        circle = plt.Circle((8, 8), 0.8, color='#F0F0F0')
    ax.add_patch(circle)
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)

def create_neon_animation(emotions):
    """Generate a neon-themed animation based on emotions"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_facecolor('black')
    ax.axis('off')
    
    # Neon colors based on emotions
    neon_colors = {
        "joy": "#FFFF00",      # Neon yellow
        "sadness": "#00FFFF",  # Neon cyan
        "anger": "#FF0000",    # Neon red
        "fear": "#9932CC",     # Dark orchid
        "surprise": "#00FF00"  # Neon green
    }
    
    # Create abstract neon shapes based on emotions
    for emotion_data in emotions:
        emotion = emotion_data["emotion"]
        intensity = emotion_data["intensity"]
        color = neon_colors.get(emotion, "#FFFFFF")
        
        # Number of shapes based on intensity
        n_shapes = int(3 + intensity * 7)
        
        for _ in range(n_shapes):
            shape_type = random.choice(['circle', 'line', 'rectangle'])
            
            if shape_type == 'circle':
                x, y = random.uniform(1, 9), random.uniform(1, 9)
                size = random.uniform(0.1, 0.8) * intensity
                circle = plt.Circle((x, y), size, color=color, alpha=0.7, fill=False, linewidth=2)
                ax.add_patch(circle)
                
                # Add glow effect
                for i in range(3):
                    glow = plt.Circle((x, y), size + i*0.05, color=color, alpha=0.2-i*0.05, fill=False, linewidth=1)
                    ax.add_patch(glow)
                
            elif shape_type == 'line':
                x1, y1 = random.uniform(0, 10), random.uniform(0, 10)
                angle = random.uniform(0, 2*np.pi)
                length = random.uniform(1, 3) * intensity
                x2 = x1 + length * np.cos(angle)
                y2 = y1 + length * np.sin(angle)
                
                ax.plot([x1, x2], [y1, y2], color=color, alpha=0.8, linewidth=2)
                
                # Add glow effect
                ax.plot([x1, x2], [y1, y2], color=color, alpha=0.3, linewidth=4)
                
            elif shape_type == 'rectangle':
                x, y = random.uniform(1, 8), random.uniform(1, 8)
                width = random.uniform(0.5, 2) * intensity
                height = random.uniform(0.5, 2) * intensity
                rect = plt.Rectangle((x, y), width, height, color=color, alpha=0.7, fill=False, linewidth=2)
                ax.add_patch(rect)
                
                # Add glow effect
                for i in range(3):
                    glow = plt.Rectangle((x-i*0.05, y-i*0.05), width+i*0.1, height+i*0.1, color=color, alpha=0.2-i*0.05, fill=False, linewidth=1)
                    ax.add_patch(glow)
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)

def create_animation(emotions, theme="forest"):
    """Create animation based on selected theme and emotions"""
    if theme == "forest":
        return create_forest_animation(emotions)
    elif theme == "ocean":
        return create_ocean_animation(emotions)
    elif theme == "neon":
        return create_neon_animation(emotions)
    else:
        return create_forest_animation(emotions)  # Default to forest

def generate_composite_image(emotions):
    """Generate a composite image from all emotions in the story"""
    return create_animation(emotions, st.session_state.animation_theme)

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

# Main content
if st.session_state.current_stage == "setup":
    st.subheader("Let's create your Emotional Symphony!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personalize Your Experience")
        username = st.text_input("Your Name (Optional)", value="You")
        st.session_state.user_name = username if username else "You"
        
    with col2:
        st.markdown("### Choose Your Story Elements")
        st.session_state.story_length = st.slider(
            "Story Length (number of emotional entries)",
            min_value=2,
            max_value=10,
            value=4
        )
        
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
    # Show progress
    total_entries = st.session_state.story_length
    current_entries = len(st.session_state.story_entries)
    progress = current_entries / total_entries
    
    st.progress(progress)
    st.markdown(f"### Entry {st.session_state.current_entry_number} of {total_entries}")
    
    # Prompt for emotional input based on entry number
    prompts = [
        "Express your current emotional state. What are you feeling right now?",
        "Describe a memory that brings up strong emotions.",
        "Share an emotional high point or success in your life.",
        "Describe an emotion you find difficult to express.",
        "Share a hope or dream that brings you joy.",
        "What makes you feel peaceful or calm?",
        "Describe something that made you laugh recently.",
        "Share an emotional challenge you're facing.",
        "What sensation or experience fills you with wonder?",
        "If your current mood was a landscape, what would it look like?"
    ]
    
    current_prompt_index = min(st.session_state.current_entry_number - 1, len(prompts) - 1)
    current_prompt = prompts[current_prompt_index]
    
    st.markdown(f"## Your Emotional Expression")
    st.markdown(current_prompt)
    
    user_text = st.text_area("Your response:", height=100)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Submit", key="submit_emotion"):
            if user_text.strip():
                # Detect emotion from text
                emotion_data = detect_emotion(user_text)
                music_data = generate_music_snippet(emotion_data["emotion"], emotion_data["intensity"])
                
                entry = {
                    "user": st.session_state.user_name,
                    "text": user_text,
                    "emotion": emotion_data,
                    "music": music_data,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                
                st.session_state.story_entries.append(entry)
                st.session_state.emotions_detected.append(emotion_data)
                
                # Move to next entry or next stage
                st.session_state.current_entry_number += 1
                
                # Check if story is complete
                if len(st.session_state.story_entries) >= st.session_state.story_length:
                    st.session_state.current_stage = "generate"
                
                st.rerun()
            else:
                st.error("Please enter some text before submitting.")
    
    # Display previous entries
    if st.session_state.story_entries:
        st.markdown("### Your Story So Far")
        for i, entry in enumerate(st.session_state.story_entries, 1):
            emotion = entry["emotion"]["emotion"]
            intensity = entry["emotion"]["intensity"]
            emotion_class = f"emotion-{emotion}"
            
            st.markdown(f"""
            <div class='story-card'>
                <h4>Entry {i} <span style='font-size:0.8rem;color:gray;'>{entry['timestamp']}</span></h4>
                <p>{entry['text']}</p>
                <div>
                    <span class='emotion-pill {emotion_class}'>{emotion.capitalize()} ({int(intensity*100)}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_stage == "generate":
    st.markdown("## Generating Your Emotional Symphony")
    
    # Generate music
    if not st.session_state.music_generated:
        with st.spinner("Composing music based on your emotional journey..."):
            # Mock progress bar for music generation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            st.session_state.music_generated = True
            st.success("Music composition complete!")
    
    # Generate animation
    if st.session_state.music_generated and not st.session_state.animation_generated:
        with st.spinner(f"Creating {st.session_state.animation_theme}-themed animation..."):
            # Mock progress bar for animation generation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Generate the animation
            final_image = generate_composite_image(st.session_state.emotions_detected)
            st.session_state.final_image = final_image
            st.session_state.animation_generated = True
            st.success("Animation creation complete!")
    
    # Show final results and move to share stage
    if st.session_state.music_generated and st.session_state.animation_generated:
        st.markdown("## Your Emotional Symphony is Ready!")
        st.image(st.session_state.final_image, use_column_width=True)
        
        if st.button("Continue to Share Options"):
            st.session_state.current_stage = "share"
            st.rerun()

elif st.session_state.current_stage == "share":
    st.markdown("## Share Your Emotional Symphony")
    
    # Display the final creation
    st.image(st.session_state.final_image, use_column_width=True)
    
    # Mock audio player
    st.markdown("### 🎵 Listen to Your Symphony")
    st.audio("https://upload.wikimedia.org/wikipedia/commons/e/e5/Sine_wave_440.ogg", format="audio/ogg")
    
    # Story text compilation
    st.markdown("### Your Emotional Journey")
    story_text = ""
    for i, entry in enumerate(st.session_state.story_entries, 1):
        story_text += f"**Entry {i}**: {entry['text']}\n\n"
    
    st.markdown(story_text)
    
    # Emotion summary
    emotions_count = {}
    for entry in st.session_state.story_entries:
        emotion = entry["emotion"]["emotion"]
        emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
    
    st.markdown("### Your Emotional Palette")
    
    # Create a simple pie chart of emotions
    if emotions_count:
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = {
            "joy": "#FFEB3B", 
            "sadness": "#90CAF9", 
            "anger": "#EF5350", 
            "fear": "#9C27B0", 
            "surprise": "#66BB6A"
        }
        emotion_colors = [colors.get(emotion, "#CCCCCC") for emotion in emotions_count.keys()]
        ax.pie(emotions_count.values(), labels=[f"{k.capitalize()}" for k in emotions_count.keys()], 
               autopct='%1.1f%%', startangle=90, colors=emotion_colors)
        ax.axis('equal')
        st.pyplot(fig)
    
    # Download options
    st.markdown("### Save Your Creation")
    col1, col2, col3 = st.columns(3)
    
    with col1:
    buf = io.BytesIO()
    st.session_state.final_image.save(buf, format="PNG")
    buf.seek(0)

    st.download_button(
        label="Download Image",
        data=buf,  # Use actual image buffer instead of empty BytesIO()
        file_name="emotional_symphony.png",
        mime="image/png"
    )
    
    with col2:
        st.download_button(
            label="Download Audio",
            data=io.BytesIO(),  # This would be real audio data in production
            file_name="emotional_symphony.mp3",
            mime="audio/mpeg"
        )
    
    with col3:
        st.download_button(
            label="Download Video",
            data=io.BytesIO(),  # This would be real video data in production
            file_name="emotional_symphony.mp4",
            mime="video/mp4"
        )
    
    # Share options (mock)
    st.markdown("### Share on Social Media")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.button("Share to Facebook")
    with col2:
        st.button("Share to Twitter")
    with col3:
        st.button("Share to Instagram")
    with col4:
        st.button("Copy Link")
    
    # Start a new creation
    if st.button("Create a New Emotional Symphony"):
        # Reset all session state variables
        st.session_state.story_entries = []
        st.session_state.emotions_detected = []
        st.session_state.current_stage = "setup"
        st.session_state.music_generated = False
        st.session_state.animation_generated = False
        st.session_state.final_video = None
        st.session_state.current_entry_number = 1
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:gray;font-size:0.8rem;'>Emotional Symphony - A Music Storytelling Platform</div>", unsafe_allow_html=True)