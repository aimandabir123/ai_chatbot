"""
products.py
All product definitions and FAQ knowledge for all 4 Apple products.
"""

# ── Product Registry ──────────────────────────────────────────
PRODUCTS = {
    "vision_pro": {
        "name":     "Apple Vision Pro",
        "emoji":    "🥽",
        "color":    "#2997ff",
        "category": "Spatial Computing",
        "price":    "$3,499",
        "keywords": [
            "vision pro", "visionos", "spatial", "headset", "optic id",
            "eyesight", "light seal", "digital crown", "zeiss", "vision",
        ],
    },
    "iphone_15_pro": {
        "name":     "iPhone 15 Pro",
        "emoji":    "📱",
        "color":    "#30d158",
        "category": "Smartphone",
        "price":    "$999",
        "keywords": [
            "iphone", "ios", "face id", "action button", "dynamic island",
            "titanium", "a17 pro", "iphone 15", "phone",
        ],
    },
    "macbook_pro_m3": {
        "name":     "MacBook Pro M3",
        "emoji":    "💻",
        "color":    "#ff9500",
        "category": "Laptop",
        "price":    "$1,999",
        "keywords": [
            "macbook", "macos", "m3", "laptop", "mac", "trackpad",
            "touch id", "thunderbolt", "macbook pro",
        ],
    },
    "airpods_pro": {
        "name":     "AirPods Pro 2",
        "emoji":    "🎧",
        "color":    "#bf5af2",
        "category": "Audio",
        "price":    "$249",
        "keywords": [
            "airpods", "anc", "noise cancellation", "transparency",
            "h2 chip", "spatial audio", "ear tips", "earbuds", "airpods pro",
        ],
    },
}

# ── FAQ Knowledge Base ────────────────────────────────────────
PRODUCT_FAQ = {

    "vision_pro": [
        {
            "category": "Getting Started",
            "questions": [
                {
                    "q": "How do I set up Apple Vision Pro?",
                    "a": (
                        "1. Charge the external battery pack for 2 hours.\n"
                        "2. Put on the headset and adjust the Light Seal for a snug fit.\n"
                        "3. Press the Digital Crown to power on.\n"
                        "4. Follow eye-tracking calibration — look at each dot precisely.\n"
                        "5. Complete hand-tracking calibration — pinch fingers as instructed.\n"
                        "6. Sign in with your Apple ID.\n"
                        "7. Set up Optic ID (like Face ID but reads your iris).\n"
                        "8. Insert ZEISS prescription lenses if you need vision correction.\n"
                        "9. Complete the visionOS welcome tour.\n"
                        "Total setup time: about 15 minutes."
                    ),
                },
                {
                    "q": "What is Optic ID on Vision Pro?",
                    "a": (
                        "Optic ID is Vision Pro's biometric authentication system. "
                        "It reads the unique pattern of your iris to unlock the device, "
                        "authorise App Store purchases, and authenticate Apple Pay. "
                        "Optic ID data is encrypted and stored only on-device — never sent to Apple. "
                        "Recalibrate at: Settings > Optic ID & Passcode > Add Optic ID Appearance."
                    ),
                },
                {
                    "q": "Is Apple Vision Pro safe for children?",
                    "a": (
                        "Apple Vision Pro is NOT recommended for children under 13. "
                        "Developing eyes may be harmed by extended headset use. "
                        "For adults, Apple recommends taking a 30-minute break every session. "
                        "Never use while driving, cycling, or operating machinery. "
                        "Stop immediately if you feel dizziness, eye strain, or headaches."
                    ),
                },
            ],
        },
        {
            "category": "Display and Optics",
            "questions": [
                {
                    "q": "Why is my Vision Pro display blurry?",
                    "a": (
                        "Fix a blurry display with these steps:\n"
                        "1. Adjust the fit — the Light Seal must sit flush on your face.\n"
                        "2. Rotate the Digital Crown to change eye-relief distance.\n"
                        "3. Recalibrate Optic ID: Settings > Accessibility > Optic ID > Reset.\n"
                        "4. Order ZEISS prescription lenses at apple.com if you need vision correction.\n"
                        "5. Clean lenses gently with the included polishing cloth.\n"
                        "6. Let the headset dry if there is condensation inside."
                    ),
                },
                {
                    "q": "Can I use Vision Pro with prescription glasses?",
                    "a": (
                        "Do NOT insert regular glasses inside Vision Pro — this will scratch the lenses.\n"
                        "The correct solution is ZEISS Optical Inserts, which attach magnetically:\n"
                        "- ZEISS Readers: non-prescription, for reading distance.\n"
                        "- ZEISS Custom Rx: made with your exact prescription.\n"
                        "Order at apple.com — delivery takes 1 to 2 weeks for custom lenses.\n"
                        "Contact lens wearers can use Vision Pro normally without inserts."
                    ),
                },
                {
                    "q": "How do I recalibrate eye tracking on Vision Pro?",
                    "a": (
                        "Method 1: Settings > General > Reset > Reset Eye Calibration.\n"
                        "Method 2: Settings > Accessibility > Optic ID > Add Appearance.\n"
                        "Tips for best results:\n"
                        "- Sit in moderate, consistent lighting.\n"
                        "- Look at the centre of each dot — move only your eyes, not your head.\n"
                        "- Hold each dot until it fills completely before moving on.\n"
                        "- Clean the inside cameras with a microfiber cloth if calibration fails."
                    ),
                },
            ],
        },
        {
            "category": "Battery and Charging",
            "questions": [
                {
                    "q": "How long does Vision Pro battery last?",
                    "a": (
                        "Standard included battery pack: up to 2 hours of general use.\n"
                        "Plugged into a wall outlet via the battery pack: unlimited use time.\n"
                        "Third-party extended battery packs (e.g. Anker): 4 to 6 hours.\n"
                        "Tips to extend battery: lower display brightness, enable Travel Mode, "
                        "close unused background apps."
                    ),
                },
                {
                    "q": "Vision Pro battery not charging — how to fix?",
                    "a": (
                        "1. Use ONLY the included Apple USB-C cable and a 30W+ adapter.\n"
                        "2. Check the USB-C port for debris — clean with a dry toothpick.\n"
                        "3. Try a different wall outlet.\n"
                        "4. Check battery LEDs: 1 amber dot = below 25%, 4 white dots = full.\n"
                        "5. Let the battery completely drain, then charge for 2 hours uninterrupted.\n"
                        "6. If none of these steps work, contact Apple Support — battery replacement "
                        "is covered free within the 1-year warranty."
                    ),
                },
            ],
        },
        {
            "category": "Troubleshooting",
            "questions": [
                {
                    "q": "How do I reset or restart Apple Vision Pro?",
                    "a": (
                        "Soft restart: Hold Digital Crown + Top button for 5 seconds → "
                        "slide to power off → press Digital Crown to restart.\n"
                        "Force restart (if frozen): Hold Digital Crown + Top button for 10 seconds "
                        "until the Apple logo appears.\n"
                        "Factory reset (erases everything): "
                        "Settings > General > Transfer or Reset > Erase All Content and Settings.\n"
                        "Recovery via Mac: Connect USB-C to Mac → open Finder → select Vision Pro → Restore."
                    ),
                },
                {
                    "q": "How do I update visionOS?",
                    "a": (
                        "1. Connect Vision Pro to Wi-Fi and ensure battery is above 50%.\n"
                        "2. Go to Settings > General > Software Update.\n"
                        "3. Tap Download and Install.\n"
                        "4. Keep the headset on or place it on a flat surface during the update.\n"
                        "Updates take 10 to 20 minutes. "
                        "Enable automatic updates at Settings > General > Software Update > Automatic Updates."
                    ),
                },
            ],
        },
    ],

    "iphone_15_pro": [
        {
            "category": "Getting Started",
            "questions": [
                {
                    "q": "How do I set up iPhone 15 Pro?",
                    "a": (
                        "1. Press and hold the side button to power on.\n"
                        "2. Select your language and region.\n"
                        "3. Connect to Wi-Fi.\n"
                        "4. Choose to transfer data from an old iPhone or set up as new.\n"
                        "5. Sign in with your Apple ID.\n"
                        "6. Set up Face ID — follow the on-screen prompts.\n"
                        "7. Set a six-digit passcode.\n"
                        "8. Restore from iCloud backup or set up apps manually.\n"
                        "9. Configure Siri, Screen Time, and Apple Pay."
                    ),
                },
                {
                    "q": "What is the Action Button on iPhone 15 Pro?",
                    "a": (
                        "The Action Button replaces the old mute switch on iPhone 15 Pro. "
                        "It is fully customisable. You can set it to: "
                        "toggle silent mode, launch the camera, turn on flashlight, "
                        "start a voice memo, activate Translate, open Magnifier, "
                        "run a Shortcut, or trigger an Accessibility feature. "
                        "Configure it at: Settings > Action Button."
                    ),
                },
            ],
        },
        {
            "category": "Camera",
            "questions": [
                {
                    "q": "What cameras does iPhone 15 Pro have?",
                    "a": (
                        "iPhone 15 Pro camera system:\n"
                        "- 48MP Main camera (f/1.78, second-gen sensor-shift OIS)\n"
                        "- 12MP Ultra Wide (f/2.2, supports macro photography)\n"
                        "- 12MP 3x Telephoto on Pro, 5x Telephoto on Pro Max\n"
                        "Features: ProRAW, ProRes video, Log video recording, "
                        "Action Mode, Cinematic Mode, Photonic Engine processing. "
                        "Powered by the A17 Pro chip with dedicated hardware ray tracing."
                    ),
                },
                {
                    "q": "How do I shoot ProRes video on iPhone 15 Pro?",
                    "a": (
                        "1. Go to Settings > Camera > Formats and enable ProRes.\n"
                        "2. Open the Camera app and switch to Video mode.\n"
                        "3. Tap the ProRes indicator in the top-right corner to activate it.\n"
                        "4. Press the red record button to start recording.\n"
                        "Important: ProRes files are very large. "
                        "For 4K ProRes, Apple recommends an external USB-C SSD "
                        "connected via a USB 3 cable for storage."
                    ),
                },
            ],
        },
        {
            "category": "Battery and Charging",
            "questions": [
                {
                    "q": "How long does iPhone 15 Pro battery last?",
                    "a": (
                        "iPhone 15 Pro: up to 23 hours of video playback.\n"
                        "iPhone 15 Pro Max: up to 29 hours of video playback.\n"
                        "Charging speeds:\n"
                        "- MagSafe: up to 15W wireless charging.\n"
                        "- Qi: up to 7.5W wireless charging.\n"
                        "- Wired USB-C: up to 20W fast charge (0 to 50% in about 30 minutes)."
                    ),
                },
                {
                    "q": "How do I check iPhone 15 Pro battery health?",
                    "a": (
                        "Go to Settings > Battery > Battery Health and Charging. "
                        "This shows the maximum capacity percentage compared to when new. "
                        "At 80% or below, Apple recommends battery replacement. "
                        "Enable Optimised Battery Charging to slow long-term degradation. "
                        "Avoid leaving the phone at 100% charge overnight regularly."
                    ),
                },
            ],
        },
        {
            "category": "Troubleshooting",
            "questions": [
                {
                    "q": "iPhone 15 Pro overheating — what should I do?",
                    "a": (
                        "iPhone 15 Pro may run warm during initial setup, iCloud restore, "
                        "or intensive gaming. If it feels hot:\n"
                        "1. Remove the case temporarily to improve heat dissipation.\n"
                        "2. Pause resource-heavy tasks like gaming or video editing.\n"
                        "3. Disable 5G temporarily: Settings > Cellular > Voice and Data > LTE.\n"
                        "4. Turn off Background App Refresh: Settings > General > Background App Refresh.\n"
                        "5. Update to the latest iOS — Apple has released patches to improve thermal management."
                    ),
                },
                {
                    "q": "How do I factory reset iPhone 15 Pro?",
                    "a": (
                        "Method 1 (from the phone): "
                        "Settings > General > Transfer or Reset iPhone > Erase All Content and Settings.\n"
                        "Method 2 (Recovery Mode via Mac):\n"
                        "1. Power off the iPhone.\n"
                        "2. Hold the side button and connect USB-C to your Mac simultaneously.\n"
                        "3. Keep holding until you see the recovery mode screen.\n"
                        "4. Open Finder on Mac, select the iPhone, and click Restore."
                    ),
                },
            ],
        },
    ],

    "macbook_pro_m3": [
        {
            "category": "Getting Started",
            "questions": [
                {
                    "q": "How do I set up MacBook Pro M3?",
                    "a": (
                        "1. Open the lid — the MacBook powers on automatically.\n"
                        "2. Select your language and region.\n"
                        "3. Connect to Wi-Fi.\n"
                        "4. Sign in with your Apple ID.\n"
                        "5. Set up Touch ID — press your finger on the top-right corner of the keyboard.\n"
                        "6. Optionally use Migration Assistant to transfer data from an old Mac.\n"
                        "7. Enable FileVault disk encryption when prompted — recommended for security.\n"
                        "8. Complete the macOS setup assistant."
                    ),
                },
                {
                    "q": "What ports does MacBook Pro M3 have?",
                    "a": (
                        "MacBook Pro M3 14-inch ports:\n"
                        "- 3x Thunderbolt 4 (USB-C) — up to 40Gbps each\n"
                        "- 1x HDMI 2.1 — supports 8K/60Hz or 4K/240Hz\n"
                        "- 1x SDXC card slot (UHS-II speed)\n"
                        "- 1x MagSafe 3 charging port\n"
                        "- 1x 3.5mm headphone jack (supports high-impedance headphones)\n"
                        "The 16-inch model adds an additional USB-A port."
                    ),
                },
            ],
        },
        {
            "category": "Performance",
            "questions": [
                {
                    "q": "How fast is the M3 chip in MacBook Pro?",
                    "a": (
                        "Apple M3 chip specifications:\n"
                        "- 8-core CPU (4 performance + 4 efficiency cores)\n"
                        "- 10-core GPU with hardware ray tracing support\n"
                        "- 16GB unified memory standard, up to 24GB\n"
                        "- 100GB/s memory bandwidth\n"
                        "- 8-core Neural Engine capable of 18 TOPS\n"
                        "M3 Pro: 12-core CPU, 18-core GPU, up to 36GB RAM.\n"
                        "M3 Max: 16-core CPU, 40-core GPU, up to 128GB RAM."
                    ),
                },
                {
                    "q": "How long does MacBook Pro M3 battery last?",
                    "a": (
                        "MacBook Pro M3 battery life:\n"
                        "- 14-inch M3: up to 18 hours\n"
                        "- 14-inch M3 Pro or Max: up to 18 hours\n"
                        "- 16-inch M3 Pro: up to 22 hours\n"
                        "- 16-inch M3 Max: up to 22 hours\n"
                        "Charge via MagSafe 3 or any Thunderbolt 4 port with a USB-C PD adapter. "
                        "A 96W or higher adapter is recommended for the 14-inch model. "
                        "Check battery health at: Apple menu > System Settings > Battery > Battery Health."
                    ),
                },
            ],
        },
        {
            "category": "Troubleshooting",
            "questions": [
                {
                    "q": "MacBook Pro M3 running slow — how do I fix it?",
                    "a": (
                        "1. Open Activity Monitor (press Cmd+Space, type Activity Monitor) — "
                        "look for processes using high CPU or memory.\n"
                        "2. Restart the Mac: Apple menu > Restart.\n"
                        "3. Free up storage: Apple menu > System Settings > General > Storage — "
                        "delete large unused files.\n"
                        "4. Reduce visual effects: System Settings > Accessibility > Display > Reduce Motion.\n"
                        "5. Update macOS: System Settings > General > Software Update.\n"
                        "6. Reset NVRAM: power off, then hold Cmd + Option + P + R immediately on startup."
                    ),
                },
                {
                    "q": "MacBook Pro M3 not charging — how do I fix it?",
                    "a": (
                        "1. Use the MagSafe 3 cable or a USB-C PD adapter rated at 96W or higher.\n"
                        "2. Try a different Thunderbolt 4 port on the MacBook.\n"
                        "3. Inspect the cable and port for damage or debris.\n"
                        "4. Plug directly into a wall outlet — avoid extension cords.\n"
                        "5. On M3 Macs, there is no manual SMC reset — simply restart the MacBook.\n"
                        "6. Check the charging indicator light: amber means charging, green means full."
                    ),
                },
                {
                    "q": "How do I take a screenshot on MacBook Pro?",
                    "a": (
                        "Screenshot keyboard shortcuts on Mac:\n"
                        "- Cmd + Shift + 3: capture the entire screen.\n"
                        "- Cmd + Shift + 4: drag to select a custom area.\n"
                        "- Cmd + Shift + 4, then Space: click to capture a specific window.\n"
                        "- Cmd + Shift + 5: open the screenshot toolbar with screen recording options.\n"
                        "Screenshots are saved to the Desktop by default. "
                        "Change the save location in the screenshot toolbar under Options > Save To."
                    ),
                },
            ],
        },
    ],

    "airpods_pro": [
        {
            "category": "Getting Started",
            "questions": [
                {
                    "q": "How do I set up AirPods Pro 2?",
                    "a": (
                        "Pairing with iPhone (easiest method):\n"
                        "1. Open the case near your unlocked iPhone.\n"
                        "2. A setup popup appears — tap Connect.\n"
                        "3. Follow the prompts including the ear tip fit test.\n"
                        "4. AirPods automatically connect to all devices signed into your Apple ID.\n\n"
                        "Pairing with a non-Apple device:\n"
                        "1. Open the case.\n"
                        "2. Press and hold the button on the back of the case until the LED flashes white.\n"
                        "3. Open Bluetooth settings on your device and select AirPods Pro."
                    ),
                },
                {
                    "q": "How do I use the touch controls on AirPods Pro 2?",
                    "a": (
                        "Touch controls on the AirPods Pro 2 stem:\n"
                        "- Press once: play or pause, answer or end a call.\n"
                        "- Press twice: skip to the next track.\n"
                        "- Press three times: go back to the previous track.\n"
                        "- Press and hold: switch between ANC and Transparency mode.\n"
                        "- Swipe up on stem: increase volume.\n"
                        "- Swipe down on stem: decrease volume.\n"
                        "Customise controls at: Settings > Bluetooth > tap the info icon next to AirPods Pro."
                    ),
                },
            ],
        },
        {
            "category": "Audio and Noise Cancellation",
            "questions": [
                {
                    "q": "How does Active Noise Cancellation work on AirPods Pro 2?",
                    "a": (
                        "AirPods Pro 2 ANC uses the H2 chip with two microphones per AirPod. "
                        "The outward-facing microphone detects external noise. "
                        "The inward-facing microphone monitors sound inside the ear canal. "
                        "The H2 chip generates a cancellation audio signal 48,000 times per second. "
                        "ANC is up to 2x more effective than the original AirPods Pro. "
                        "Switch modes by pressing and holding the stem, "
                        "or through Control Centre on iPhone."
                    ),
                },
                {
                    "q": "What is Adaptive Audio on AirPods Pro 2?",
                    "a": (
                        "Adaptive Audio (requires iOS 17 or later) automatically blends "
                        "Active Noise Cancellation and Transparency mode based on your environment. "
                        "Conversation Awareness: automatically lowers your music volume and "
                        "enables Transparency when you start speaking. "
                        "Personalised Volume: adjusts loudness based on your environment and "
                        "listening history over time. "
                        "Enable at: Settings > Bluetooth > tap info icon next to AirPods Pro > Adaptive Audio."
                    ),
                },
            ],
        },
        {
            "category": "Battery",
            "questions": [
                {
                    "q": "How long do AirPods Pro 2 battery last?",
                    "a": (
                        "AirPods Pro 2 battery life:\n"
                        "- AirPods alone with ANC on: up to 6 hours.\n"
                        "- AirPods alone with ANC off: up to 7 hours.\n"
                        "- Total with charging case and ANC on: up to 30 hours.\n"
                        "- Total with charging case and ANC off: up to 36 hours.\n"
                        "Fast charging: 5 minutes in the case gives approximately 1 hour of playback. "
                        "The MagSafe case charges via MagSafe, standard Qi, Apple Watch charger, or USB-C."
                    ),
                },
                {
                    "q": "How do I check AirPods Pro 2 battery level?",
                    "a": (
                        "There are four ways to check battery:\n"
                        "1. Open the case near your iPhone — a popup shows battery for each AirPod and the case.\n"
                        "2. Ask Siri: 'Hey Siri, how is my AirPods battery?'\n"
                        "3. Add the Batteries widget to your iPhone Home Screen.\n"
                        "4. On the charging case itself: press the button on the back — "
                        "the LED shows charge level with colour and flashing pattern."
                    ),
                },
            ],
        },
        {
            "category": "Troubleshooting",
            "questions": [
                {
                    "q": "AirPods Pro 2 not connecting — how do I fix it?",
                    "a": (
                        "1. Put AirPods in the case, close the lid, wait 15 seconds, then reopen.\n"
                        "2. On iPhone: Settings > Bluetooth — find AirPods Pro, tap the info icon, "
                        "tap Forget This Device, then re-pair.\n"
                        "3. Factory reset AirPods: press and hold the case button for 15 seconds "
                        "until the LED flashes amber then white.\n"
                        "4. Update iOS and check for AirPods firmware updates.\n"
                        "5. Move away from Wi-Fi routers — 2.4GHz interference can affect Bluetooth."
                    ),
                },
                {
                    "q": "AirPods Pro 2 sound is muffled or poor quality — how do I fix it?",
                    "a": (
                        "1. Run the ear tip fit test: Settings > Bluetooth > tap info icon > Ear Tip Fit Test.\n"
                        "2. Clean the ear tips — remove them and rinse with water, then dry completely.\n"
                        "3. Clean the AirPod mesh gently with a dry cotton swab.\n"
                        "4. Check EQ settings: Settings > Music > EQ — try setting to Off or Late Night.\n"
                        "5. Toggle ANC or Transparency mode off and back on.\n"
                        "6. Reset AirPods by holding the case button for 15 seconds.\n"
                        "7. If one AirPod is louder: Settings > Accessibility > Audio Visual > adjust balance slider."
                    ),
                },
            ],
        },
    ],
}
