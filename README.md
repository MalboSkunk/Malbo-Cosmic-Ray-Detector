🌌 Malbo Cosmic Ray Detector (Vailly Station 01)
This project is a DIY cosmic ray detector based on a modified CMOS sensor and a Raspberry Pi. It is designed to capture and log secondary cosmic particles (muons) as part of a citizen science initiative.



🚀 Overview
The system monitors a camera feed in real-time to detect high-energy particle impacts. When a muon strikes the sensor, it creates a cluster of bright pixels which are then analyzed, categorized, and logged.

Location: Vailly-sur-Aisne, France (Station: Malbo_Vailly_Station_01)

Hardware: Raspberry Pi 3A+ with a modified CMOS sensor (Logitech)

Software: Python 3, OpenCV, NumPy



🛠️ Key Features
Real-time Detection: Analyzes frames at high frequency to catch fleeting impacts.

Smart Categorization: Automatically distinguishes between "points" (direct hits) and "traits" (angled tracks) based on pixel count and geometry.

Scientific Logging: Generates a PNG capture and a structured JSON metadata file for every event, following citizen science standards.

Instant Notifications: Integrated Discord Webhook for real-time monitoring of detection events.



📊 Data Structure
Each detection generates:

a PNG image of the impact.

a JSON file containing:

device_id: Station identifier.

timestamp: UTC time of the event.

pixels: Intensity/Size of the impact.

type: Classification of the particle track.



📜 How to use
Clone the repository.

Set up your .env file with your DISCORD_WEBHOOK.

Run python3 Raspberry_Chasseur_de_Muons.py.
