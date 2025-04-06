import streamlit as st
import pandas as pd
import random

# Load Pokémon data
@st.cache_data
def load_pokemon_data():
    df = pd.read_csv("pokemon_data_with_images.csv")
    return df

pokemon_df = load_pokemon_data()

# --- Session State ---
if "player_pokemon" not in st.session_state:
    st.session_state.player_pokemon = pokemon_df[pokemon_df['name'] == "Pikachu"].iloc[0].to_dict()
    st.session_state.enemy_pokemon = None
    st.session_state.lives = 3
    st.session_state.status = ""
    st.session_state.last_outcome = ""

# --- Functions ---
def choose_enemy():
    enemy = pokemon_df.sample(1).iloc[0].to_dict()
    st.session_state.enemy_pokemon = enemy
    st.session_state.status = f"⚔️ {enemy['name']} appears!"
    st.session_state.last_outcome = ""

def battle():
    player = st.session_state.player_pokemon
    enemy = st.session_state.enemy_pokemon

    player_power = player['attack'] + random.randint(0, 10)
    enemy_power = enemy['attack'] + random.randint(0, 10)

    if player_power >= enemy_power:
        st.session_state.last_outcome = f"✅ You won! Power: {player_power} vs {enemy_power}"
        st.session_state.player_pokemon = enemy  # Player adopts enemy
    else:
        st.session_state.lives -= 1
        st.session_state.last_outcome = f"❌ You lost! Power: {player_power} vs {enemy_power}"
        if st.session_state.lives <= 0:
            st.session_state.last_outcome += "\n💀 Game Over!"

    st.session_state.enemy_pokemon = None

# --- UI Helpers ---
def display_pokemon(pokemon, title):
    st.markdown(f"### {title}")
    st.image(pokemon['image_url'], width=150)
    st.markdown(f"**{pokemon['name']}**")
    st.text(f"Type: {pokemon['type']}")
    st.text(f"HP: {pokemon['hp']} | Attack: {pokemon['attack']}")

# --- Layout ---
st.title("🔴 Pokémon Match – Web Version")
st.markdown("Win battles to use new Pokémon. Lose 3 times and it's game over.")

st.markdown(f"### 💚 Lives: {st.session_state.lives}")
display_pokemon(st.session_state.player_pokemon, "🧍 Your Pokémon")

st.divider()

if st.session_state.enemy_pokemon:
    display_pokemon(st.session_state.enemy_pokemon, "🤖 Opponent")
    col1, col2 = st.columns(2)
    col1.button("⚔️ Fight", on_click=battle)
    col2.button("⏭️ Skip", on_click=choose_enemy)
else:
    st.button("🔍 Find Opponent", on_click=choose_enemy)

if st.session_state.last_outcome:
    st.markdown("---")
    st.info(st.session_state.last_outcome)

if st.session_state.status:
    st.markdown("---")
    st.write(st.session_state.status)
