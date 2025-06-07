

# T510 – Emotional Symphony

> A collaborative, emotion‑driven storytelling web app that converts mood‑related text into synchronized music and animation, allowing anyone to create and share a unique **symphony of emotion and imagery**.

---

## 🔗 Live Demo

**Production URL:** [https://510510.streamlit.app/](https://510510.streamlit.app/)

> Open in any modern browser – no local installation required.

---

## 🎯 Project Objective

* Transform free‑form emotional text into real‑time visuals and music.
* Showcase course concepts such as client–server architecture, session‑state management, asynchronous API calls, and AI integration.
* Provide an engaging medium for collaborative storytelling and emotional reflection.

---

## 📋 Prerequisites

| Dependency                   | Minimum Version | Purpose                             |
| ---------------------------- | --------------- | ----------------------------------- |
| **Python**                   | 3.9 or newer    | Core runtime                        |
| Node *(optional)*            | 18+             | Local linting / Storybook (if used) |
| **portaudio** *(Linux only)* | latest          | Enables audio playback              |

```bash
# Recommended: create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📂 Directory Structure

```text
├── app.py               # Streamlit UI entry‑point
├── emotion.py           # detect_emotion(text)
├── music.py             # generate_music(emotion)
├── animation.py         # render_animation(theme, emotion)
├── utils.py             # helpers: JSON export, logging, etc.
├── assets/              # static images / demo GIFs
│   ├── ui_overview.png
│   └── sample_output.gif
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

---

## 🚀 Quick Start

### 1  Run Locally

```bash
git clone https://github.com/<your‑org>/T510_2025.git
cd T510_2025
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### 2  One‑Click Demo

Simply visit [https://510510.streamlit.app/](https://510510.streamlit.app/).

---

## ✨ Core Features

| # | Feature                      | Description                                                                                           |
| - | ---------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1 | **Emotion Detection**        | Uses the Google Gemini API for sentiment analysis with a rule-based fallback for offline reliability. |
| 2 | **Animation Themes**         | Real-time rendering in three distinct visual styles: Forest, Ocean, and Neon.                         |
| 3 | **Turn-Based Collaboration** | Multiple users can contribute text sequentially to co-create an Emotional Symphony together.          |
| 4 | **Export & Share**           | One-click download of the emotion-map JSON and a preview image ready for social sharing.              |
| 5 | **Music Generation Match**   | Maps each detected emotion to a preset MIDI template, mixes tracks via pydub, and exports a WAV file. |

\--- | --- | --- |
\| 1 | **Emotion Detection** | Uses the Google Gemini API for sentiment analysis with a rule‑based fallback to guarantee offline functionality. |
\| 2 | **Animation Themes** | Real‑time rendering in three visual styles: **Forest**, **Ocean**, and **Neon**. |
\| 3 | **Turn‑Based Collaboration** | Multiple users can contribute text sequentially to co‑create an *Emotional Symphony*. |
\| 4 | **Export & Share** | One‑click download of the emotion‑map JSON and a preview image for social sharing. |
\| 5 | **Music Generation Match** | Maps each detected emotion to a preset MIDI template; mixes instruments with **pydub** and outputs a WAV file. |

\------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
\| 1                                                                                          | **Emotion Detection**                                                                      | Uses the Google Gemini API for sentiment analysis with a rule‑based fallback to guarantee offline functionality. |
\| 2                                                                                          | **Music Generation\*\*\*\*Match**                                                              | Maps each detected emotion to a preset MIDI template; mixes instruments with **pydub** and outputs a WAV file.   |
\| 3                                                                                          | **Animation Themes**                                                                       | Real‑time rendering in three visual styles: **Forest**, **Ocean**, and **Neon**.                                 |
\| 4                                                                                          | **Turn‑Based Collaboration**                                                               | Multiple users can contribute text sequentially to co‑create an *Emotional Symphony*.                            |
\| 5                                                                                          | **Export & Share**                                                                         |                                                                                                                  |
\| One‑click download of the emotion‑map JSON and a final image thumbnail for social sharing. |                                                                                            |                                                                                                                  |
\| 4                                                                                          | **Export & Share**                                                                         | One‑click download of the emotion‑map JSON and a final image thumbnail for social sharing.                       |
\|                                                                                            | One‑click download of the emotion‑map JSON and a final image thumbnail for social sharing. |                                                                                                                  |

---

## 🖥️ Usage Walk‑through

1. **Enter text** – for example: `I’m feeling very happy today ☀️`.
2. Choose the **Neon** theme and click **Generate**.
3. The system detects the emotion =`Joy`, plays a matching melody, and displays the neon animation.
4. Click **Download** to save the generated JSON score or the preview image.

*(Insert screenshots in ****************************************`assets/`**************************************** and reference them here once captured.)*

---

## ⚙️ Technical Architecture

```mermaid
graph TD
    A[Streamlit UI] -->|input text| B[detect_emotion]
    B --> C{Emotion label}
    C --> D[generate_music]
    C --> E[render_animation]
    D --> F[Session State]
    E --> F
    F --> G[Download / Share]


* **Emotion Detection**: Calls the Gemini model `models/text-bison‑001`; falls back to keyword matching if the API fails.
* **Music Pipeline**: Maps emotions to preset MIDI files, adjusts tempo & instrumentation with **pydub**, and exports audio as WAV.
* **Animation Engine**: Selects pre‑rendered Lottie JSON based on `(theme, emotion)` and embeds it via `streamlit.components.v1.html`.
* **State Management**: All intermediate data are stored in `st.session_state` for a seamless multi‑step user experience.

---

## 🛠️ Development

### Lint & Format

```bash
pip install flake8 isort
flake8 .
isort .
```

### Unit Tests

```bash
pytest tests/
```

---

## 🔒 Privacy & Compliance

* Fully compliant with **GDPR** and **CCPA** – no personally identifiable information is stored.
* All user input is anonymised and discarded when the session ends.

---

## 🗺️ Roadmap

| Milestone | Scope                                                             | ETA        |
| --------- | ----------------------------------------------------------------- | ---------- |
| Client M1 | Multi‑user emotional narrative flow; three animation themes       | 2025‑05‑02 |
| Client M2 | API‑key management, sensor integration feasibility, feedback loop | 2025‑05‑30 |
| Dev M2    | Joint debugging and feature refinement with the client            | 2025‑06‑04 |

---

## 👥 Contributors

* **Anshul Prakash** 
* **Zeng Zhang**  

