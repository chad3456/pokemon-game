import streamlit as st
import pandas as pd
import random

# Load data from CSV
@st.cache_data
def load_pokemon_data():
    df = pd.read_csv("pokemon_data_with_images.csv")
    return df

pokemon_df = load_pokemon_data()

# Clean malformed image URLs
def clean_url(url):
    return url.replace("https:https://", "https://").strip()

# --- Preload 3 default Pokémon ---
DEFAULT_TEAM_NAMES = ["Pikachu", "Bulbasaur", "Charmander"]

if "team" not in st.session_state:
    st.session_state.team = [
        pokemon_df[pokemon_df['name'] == name].iloc[0].to_dict()
        for name in DEFAULT_TEAM_NAMES
    ]
    st.session_state.selected_pokemon = st.session_state.team[0]
    st.session_state.enemy_pokemon = None
    st.session_state.lives = 3
    st.session_state.status = ""
    st.session_state.last_outcome = ""

# Choose fair enemy (same type as selected Pokémon)
def choose_enemy():
    selected_type = st.session_state.selected_pokemon['type']
    enemy_options = pokemon_df[
        (pokemon_df['type'] == selected_type) &
        (~pokemon_df['name'].isin([p['name'] for p in st.session_state.team]))
    ]
    if len(enemy_options) == 0:
        st.session_state.status = "🎉 You’ve collected all Pokémon of this type!"
        st.session_state.enemy_pokemon = None
        return

    enemy = enemy_options.sample(1).iloc[0].to_dict()
    st.session_state.enemy_pokemon = enemy
    st.session_state.status = f"⚔️ {enemy['name']} appears!"
    st.session_state.last_outcome = ""

# Battle logic
def battle():
    player = st.session_state.selected_pokemon
    enemy = st.session_state.enemy_pokemon

    player_power = player['attack'] + random.randint(0, 10)
    enemy_power = enemy['attack'] + random.randint(0, 10)

    if player_power >= enemy_power:
        st.session_state.last_outcome = f"✅ You win! Power: {player_power} vs {enemy_power}"
        st.session_state.team.append(enemy)
        if st.session_state.lives < 3:
            st.session_state.lives += 1
    else:
        st.session_state.lives -= 1
        st.session_state.last_outcome = f"❌ You lose! Power: {player_power} vs {enemy_power}"
        if st.session_state.lives <= 0:
            st.session_state.last_outcome += "\n💀 Game Over!"

    st.session_state.enemy_pokemon = None

# UI Component to show a Pokémon
def display_pokemon(pokemon, title):
    st.markdown(f"### {title}")
    st.image(clean_url(pokemon['image_url']), width=150)
    st.markdown(f"**{pokemon['name']}**")
    st.text(f"Type: {pokemon['type']}")
    st.text(f"HP: {pokemon['hp']} | Attack: {pokemon['attack']}")

# -- Main Layout --
st.title("🔴 Pokémon Match – Type-Based Fair Fights")
st.markdown("Choose your fighter and battle Pokémon of the same type!")

st.markdown(f"### 💚 Lives: {st.session_state.lives}")

# Fighter selector
team_names = [p['name'] for p in st.session_state.team]
selected_name = st.selectbox("🧠 Choose your Pokémon to battle:", team_names)

# Update selected
st.session_state.selected_pokemon = next(p for p in st.session_state.team if p['name'] == selected_name)

# Show chosen
display_pokemon(st.session_state.selected_pokemon, "🧍 Your Pokémon")

st.divider()

# Enemy Pokémon section
if st.session_state.enemy_pokemon:
    display_pokemon(st.session_state.enemy_pokemon, "🤖 Opponent")
    col1, col2 = st.columns(2)
    col1.button("⚔️ Fight", on_click=battle)
    col2.button("⏭️ Skip", on_click=choose_enemy)
else:
    st.button("🔍 Find Opponent", on_click=choose_enemy)

# Result display
if st.session_state.last_outcome:
    st.markdown("---")
    st.info(st.session_state.last_outcome)

if st.session_state.status:
    st.markdown("---")
    st.write(st.session_state.status)

# Show full team
st.markdown("---")
st.markdown("### 📦 Your Team:")
cols = st.columns(min(5, len(st.session_state.team)))
for i, poke in enumerate(st.session_state.team):
    with cols[i % 5]:
        st.image(clean_url(poke['image_url']), width=80)
        st.caption(poke['name'])
