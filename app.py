import streamlit as st
import pandas as pd
import random

# -- Load Pokémon data from CSV --
@st.cache_data
def load_pokemon_data():
    df = pd.read_csv("pokemon_data_with_images.csv")
    return df

pokemon_df = load_pokemon_data()

# -- Clean malformed image URLs if needed --
def clean_url(url):
    return url.replace("https:https://", "https://").strip()

# -- Session state defaults --
if "player_pokemon" not in st.session_state:
    st.session_state.player_pokemon = pokemon_df[pokemon_df['name'].str.lower() == "pikachu"].iloc[0].to_dict()
    st.session_state.enemy_pokemon = None
    st.session_state.lives = 3
    st.session_state.status = ""
    st.session_state.last_outcome = ""

# -- Choose a new enemy randomly --
def choose_enemy():
    enemy = pokemon_df.sample(1).iloc[0].to_dict()
    st.session_state.enemy_pokemon = enemy
    st.session_state.status = f"⚔️ {enemy['name']} appears!"
    st.session_state.last_outcome = ""

# -- Battle logic --
def battle():
    player = st.session_state.player_pokemon
    enemy = st.session_state.enemy_pokemon

    player_power = player['attack'] + random.randint(0, 10)
    enemy_power = enemy['attack'] + random.randint(0, 10)

    if player_power >= enemy_power:
        st.session_state.last_outcome = f"✅ You win! Power: {player_power} vs {enemy_power}"
        st.session_state.player_pokemon = enemy
    else:
        st.session_state.lives -= 1
        st.session_state.last_outcome = f"❌ You lose! Power: {player_power} vs {enemy_power}"
        if st.session_state.lives <= 0:
            st.session_state.last_outcome += "\n💀 Game Over!"

    st.session_state.enemy_pokemon = None

# -- Display Pokémon info block --
def display_pokemon(pokemon, title):
    st.markdown(f"### {title}")
    st.image(clean_url(pokemon['image_url']), width=150)
    st.markdown(f"**{pokemon['name']}**")
    st.text(f"Type: {pokemon['type']}")
    st.text(f"HP: {pokemon['hp']} | Attack: {pokemon['attack']}")

# -- Main UI Layout --
st.title("🔴 Pokémon Match – Web Edition")
st.markdown("Defeat wild Pokémon to add them to your team. Lose 3 times and it's game over!")

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
