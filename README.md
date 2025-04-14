# Code-Blue
# SENTINAL 🌊 - Seeing the Unseen

**Team:** Blueberry  
**Tagline:** Protecting Oceans from Afar  

---

## 🌍 Overview

**SENTINAL** is an AI-powered ocean protection system designed to enhance maritime safety and environmental conservation by providing **real-time, AI-verified pollution and ship detection**. It empowers citizens and marine authorities to communicate directly, eliminating bureaucratic delays and enabling swift action on marine issues.

---

## 🔍 Problem Statement

Despite increasing ocean pollution and threats to marine biodiversity, reporting systems are:

- Ineffective and slow
- Riddled with bureaucratic intermediaries
- Lacking prompt verification mechanisms

**SENTINAL** addresses these challenges by combining real-time satellite imaging, AI-based verification, and an interactive web interface.

---

## 💡 Solution

We developed three custom-trained AI models for:

1. **Oil Spill Detection**  
2. **Pollution Detection**  
3. **Ship Detection and Monitoring**

These models analyze images submitted by satellites, officials, and citizens to confirm the presence of pollution or suspicious ship activity.

---

## 🧠 How It Works

### AI Models
- **Oil Spill Detection:** Verifies oil spill images from various sources.
- **Pollution Detection:** Detects and verifies pollution-related entities.
- **Ship Detection:** Tracks ships (using 2022 AIS data for Singapore) and maps them on OpenStreetMap via Google Earth Engine.

### Backend Architecture (FastAPI)
- **"Brain"**: Handles all requests (login, report submission).
- **"Memory"**: Secure database for storing user details and verified reports.
- **"Smart Checkers"**: AI models validating image authenticity.
- **"Messengers"**: Frontend (JavaScript) handling user interactions and API calls.

### Report Flow
1. User submits a report with photo and location.
2. Backend verifies image via AI.
3. If valid, it is stored; else, the user is prompted to re-upload.

---

## 🛠️ Tech Stack

- **AI/ML Models**: Custom-trained models (Tensorflow and YOLO)
- **Backend**: FastAPI (Python)
- **Frontend**: JavaScript (Interactive Web Interface)
- **Mapping**: Google Earth Engine + OpenStreetMap
- **Database**: Secure storage system i.e. MySQL

---

## 🚧 Challenges

- Handling 210M AIS ship records for 2022.
- Difficulty in collecting live satellite data.
- Integration of machine learning models into the web environment.

---

## 🔮 Future Scope

- Live satellite data integration
- Scalable deployment of the website
- New features (e.g., coral reef degradation detection)
- Real-time ship tracking
- Access to current AIS datasets

---

## 🌊 Impact

- Maritime security & surveillance
- Promotes environmental responsibility
- Fosters citizen participation
- Drives tech-forward ecological solutions

---

## 🤝 Contribution

Feel free to fork, explore, or contribute ideas to expand SENTINAL's mission of ocean preservation.

---

## 🐋 Let's Protect Our Oceans Together!

Made with passion by **Team Blueberry** 💙
