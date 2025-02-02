import streamlit as st
import random
import pandas as pd
import io

# Set the background image from Google Drive
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://drive.google.com/uc?export=view&id=1thjU2D8z6KLhNqtYeFHrr3WLEE3OeEfx') no-repeat center center fixed;
        background-size: cover;
    }
    .stButton>button {
        background-color: white;
        color: black;
        border-radius: 5px;
        border: 2px solid black;
        padding: 8px 12px;
        font-weight: bold;
        display: block;
        margin: 0 auto;
    }
    .stButton>button:hover {
        background-color: #f0f0f0;
    }
    .stDownloadButton>button {
        background-color: white;
        color: black;
        border-radius: 5px;
        border: 2px solid black;
        padding: 8px 12px;
        font-weight: bold;
        display: block;
        margin: 0 auto;
    }
    .stDownloadButton>button:hover {
        background-color: #f0f0f0;
    }
    h1 {
        text-align: center;
    }
    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Categories and options
categories = {
    "Body": ["Humanoid", "Ghostly", "Jellyfish-like", "Reptilian", "Aquatic", "Insect-like", "Avian", "Feline", "Canine", "Plant-like", "Blob", "Mechanical"],
    "Features": ["Wings", "Horns", "Webbed Hands/Feet", "Tails", "Fins", "Antennae", "Tentacles", "Extra Legs", "Claws", "Scales", "Extra Arms"],
    "Eyes": ["Single Eye", "Multiple Eyes", "Tired Eyes", "Sad Eyes", "Glowing eyes", "Beady Eyes", "Large Cartoon Eyes", "Slitted Eyes", "Compound Eyes", "Hypnotic Eyes", "Star-shaped Pupils", "Floating Eyes"],
    "Personality": ["Shy", "Aggressive", "Curious", "Playful", "Mischievous", "Protective", "Lazy", "Fearful", "Noble", "Hyperactive"],
    "Habitat": ["Forest", "Volcano", "Desert", "Ocean", "Space", "Underground", "Mountains", "Sky", "Swamp", "Arctic", "Urban"],
    "Physical Trait": ["Spiky", "Smooth", "Furry", "Scaly", "Feathery", "Rocky", "Covered in Moss", "Crystalline", "Slimy", "Metallic"],
    "Accessories": ["Crown", "Armor", "Tatoos", "Jewelry", "Gadgets", "Backpack", "Mask", "Cape", "Tools", "Instrument", "Bubbles"],
    "Special Powers": ["Flight", "Super Speed", "Acid Spit", "Telekenesis", "Fire-breathing", "Water manipulation", "Lightning", "Super strength", "Hypnotism", "Healing", "Time control"]
}

# Generate random colors
def generate_colors():
    return ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(5)]

# Initialize session state
if "attributes" not in st.session_state:
    st.session_state.attributes = {cat: random.choice(categories[cat]) for cat in categories}
    st.session_state.counters = {cat: 3 for cat in categories}
    st.session_state.colors = generate_colors()
    st.session_state.color_counters = [3] * 5

# Function to randomize a specific category
def randomize_category(category):
    if st.session_state.counters[category] > 0:
        st.session_state.attributes[category] = random.choice(categories[category])
        st.session_state.counters[category] -= 1
        st.rerun()

# Function to randomize a specific color
def randomize_color(index):
    if st.session_state.color_counters[index] > 0:
        st.session_state.colors[index] = "#%06x" % random.randint(0, 0xFFFFFF)
        st.session_state.color_counters[index] -= 1
        st.rerun()

# Function to randomize all
def randomize_all():
    st.session_state.attributes = {cat: random.choice(categories[cat]) for cat in categories}
    st.session_state.counters = {cat: 3 for cat in categories}
    st.session_state.colors = generate_colors()
    st.session_state.color_counters = [3] * 5
    st.rerun()

# Function to export creature data
def export_creature():
    creature_data = "Fantasy Creature Description:\n\n"
    for category, value in st.session_state.attributes.items():
        creature_data += f"{category}: {value}\n"
    creature_data += "\nColors:\n" + "\n".join(st.session_state.colors)
    return creature_data.encode("utf-8")

# Streamlit UI
st.title("Fantasy Creature Generator")

# Display attributes and randomize buttons
for category in categories.keys():
    col1, col2, col3 = st.columns([2, 3, 1])
    col1.write(f"**{category}:**")
    col2.markdown(f"<p class='center-text'>{st.session_state.attributes[category]}</p>", unsafe_allow_html=True)
    if st.session_state.counters[category] > 0:
        if col3.button(f"Roll ({st.session_state.counters[category]} left)", key=category):
            randomize_category(category)

st.markdown("---")

# Display color choices
st.subheader("Colors")
color_cols = st.columns(5)
for i in range(5):
    with color_cols[i]:
        st.markdown(f'<div style="background-color:{st.session_state.colors[i]}; width:100%; height:50px; border-radius:5px;"></div>', unsafe_allow_html=True)
        st.write(st.session_state.colors[i])
        if st.session_state.color_counters[i] > 0:
            if st.button(f"Roll ({st.session_state.color_counters[i]} left)", key=f"color_{i}"):
                randomize_color(i)

st.markdown("---")

# Centered Randomize all button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Randomize All", key="randomize_all"):
    randomize_all()
st.markdown("</div>", unsafe_allow_html=True)

# Centered Export button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.download_button(label="Export Creature", data=export_creature(), file_name="fantasy_creature.txt", mime="text/plain")
st.markdown("</div>", unsafe_allow_html=True)
