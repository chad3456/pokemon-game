import streamlit as st
import pandas as pd
import random

# -- Load Pokémon data --
@st.cache_data
def load_pokemon_data():
    df = pd.read_csv("pokemon_data_with_images.csv")
    return df

pokemon_df = load_pokemon_data()

# -- Utility --
def clean_url(url):
    return url.replace("https:https://", "https://").strip()

# -- Initialize session state --
if "team" not in st.session_state:
    st.session_state.team = [
        pokemon_df[pokemon_df['name'].str.lower() == "pikachu"].iloc[0].to_dict()
    ]
    st.session_state.selected_pokemon = st.session_state.team[0]
    st.session_state.enemy_pokemon = None
    st.session_state.lives = 3
    st.session_state.status = ""
    st.session_state.last_outcome = ""

# -- Choose new enemy --
def choose_enemy():
    while True:
        enemy = pokemon_df.sample(1).iloc[0].to_dict()
        if enemy['name'] not in [p['name'] for p in st.session_state.team]:
            break
    st.session_state.enemy_pokemon = enemy
    st.session_state.status = f"⚔️ {enemy['name']} appears!"
    st.session_state.last_outcome = ""

# -- Battle Logic --
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

# -- Display Pokémon Card --
def display_pokemon(pokemon, title):
    st.markdown(f"### {title}")
    st.image(clean_url(pokemon['image_url']), width=150)
    st.markdown(f"**{pokemon['name']}**")
    st.text(f"Type: {pokemon['type']}")
    st.text(f"HP: {pokemon['hp']} | Attack: {pokemon['attack']}")

# -- Main UI --
st.title("🔴 Pokémon Match – Choose & Fight")
st.markdown("Win battles to collect Pokémon. Choose your fighter from your team!")

st.markdown(f"### 💚 Lives: {st.session_state.lives}")

# -- Select Pokémon from team --
team_names = [p['name'] for p in st.session_state.team]
selected_name = st.selectbox("🧠 Choose your Pokémon to battle:", team_names)

# Update selected Pokémon
st.session_state.selected_pokemon = next(p for p in st.session_state.team if p['name'] == selected_name)

# Show selected Pokémon
display_pokemon(st.session_state.selected_pokemon, "🧍 Your Chosen Pokémon")

st.divider()

# Show enemy
if st.session_state.enemy_pokemon:
    display_pokemon(st.session_state.enemy_pokemon, "🤖 Opponent")
    col1, col2 = st.columns(2)
    col1.button("⚔️ Fight", on_click=battle)
    col2.button("⏭️ Skip", on_click=choose_enemy)
else:
    st.button("🔍 Find Opponent", on_click=choose_enemy)

# Show outcome
if st.session_state.last_outcome:
    st.markdown("---")
    st.info(st.session_state.last_outcome)

# Show current team at the bottom
st.markdown("---")
st.markdown("### 📦 Your Team:")
cols = st.columns(min(5, len(st.session_state.team)))
for i, poke in enumerate(st.session_state.team):
    with cols[i % 5]:
        st.image(clean_url(poke['image_url']), width=80)
        st.caption(poke['name'])
