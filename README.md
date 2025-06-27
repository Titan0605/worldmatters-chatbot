# WorldMatters Chatbot

## Overview

This repository contains an informative chatbot specialized in the **WaterFlow** and **CleanLyfe** projects from WorldMatters. The chatbot provides accurate, reliable information about the operation of the app and environmental sustainability, based exclusively on a structured knowledge base.

## Projects Covered

### WaterFlow – Smart Water Valve IoT System

A smart system for homes that enables:

- Remote control of water valves via a mobile app
- Leak detection with flow and humidity sensors
- Alerts for critical temperatures (pipe freezing prevention)
- Cloud event logging for historical monitoring
- Accessible solutions for elderly users

### CleanLyfe – Ecological Footprint Reduction Platform

An interactive web application to help users calculate and reduce their ecological footprint:

- Carbon and water footprint questionnaires
- Eco-missions and rewards (gamification)
- Environmental data dashboards and visualizations
- User progress with levels and KPIs
- Interactive environmental education

## Knowledge Domains

- **Leak Prevention & Home Maintenance:** Leak causes, detection, pipe freezing, winter maintenance, typical water damage costs.
- **Remote Monitoring & Control (WaterFlow):** Mobile apps, smart alerts, accessible interfaces, home automation.
- **Carbon Footprint (CleanLyfe):** Definition, calculation, emission factors, reduction strategies, global impact.
- **Water Footprint & Responsible Consumption (CleanLyfe):** Types of water footprint, direct/indirect use, reduction strategies, meat consumption impact.
- **Gamification for Sustainability (CleanLyfe):** Eco-missions, rewards, habit motivation, playful learning.
- **Environmental Data Visualization:** Dashboard interpretation, common KPIs, benchmarking.
- **Practical Environmental Education:** Sustainability basics, family habits, practical green living tips.
- **Chatbot Operation (Meta-Information):** Search system, limitations, response selection process.

## Chatbot Behavior Rules

### What the Chatbot Does

- Provides accurate information about WaterFlow and CleanLyfe only
- Uses only its structured knowledge base (no generative AI)
- Offers 3–5 response variations for naturalness
- Contextualizes answers by project (WaterFlow or CleanLyfe)
- Suggests related questions to continue the conversation
- Explains technical terms in accessible language
- Recognizes synonyms and linguistic variations

### What the Chatbot Does Not Do

- Generate information not in the knowledge base
- Invent features or functionalities
- Provide information about other projects or systems
- Give specific medical, legal, or financial advice
- Recommend commercial products
- Answer unrelated topics

### Communication Strategies

- Handles ambiguity by clarifying and offering options
- If no answer is found, suggests related topics or asks for clarification
- Accessible but professional language, adapted to user level
- Organized responses with key points and practical examples

### Internal Scoring System

- **High Priority Terms (100 pts):** IoT, sensor, valve, carbon footprint, gamification, WaterFlow, CleanLyfe
- **Action Terms (60 pts):** control, detect, calculate, reduce, monitor, prevent
- **Semantic Expansion (30–50 pts):** valve → tap, faucet; footprint → impact, emissions; app → application, mobile, phone
- **Project Context (+20 pts):** Bonus for correct project identification

## Example Interactions

- **User:** "How do I control my valve from my phone?"  
  **Response:** Explains WaterFlow mobile app, features, and user benefits.

- **User:** "What is a carbon footprint?"  
  **Response:** Clear definition, contributing factors, and how CleanLyfe calculates it.

## Getting Started

### Prerequisites

- Python 3.12+
- Recommended: Virtual environment (see `env/`)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/worldmatters-chatbot.git
   cd worldmatters-chatbot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

```sh
python run.py
```

The chatbot will be available locally. For web or API integration, see the `app/` directory.

## Project Structure

```
app/
  database/         # Data and connection logic
  models/           # Data models
  routes/           # API and processing routes
  services/         # Business logic and scoring
  static/           # CSS/JS assets
  templates/        # HTML templates
  utils/            # Utilities (DB, formatting, logging)
run.py              # Main entry point
requirements.txt    # Python dependencies
```