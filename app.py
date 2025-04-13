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

# ---- Styled card CSS ----
card_css = """
<style>
.poke-card {
    background: linear-gradient(145deg, #f3f3f3, #ffffff);
    border-radius: 20px;
    padding: 20px;
    width: 100%;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    text-align: center;
}
.poke-card img {
    width: 100px;
    margin-bottom: 10px;
}
.poke-card h3 {
    margin: 0;
    font-size: 22px;
    color: #333;
}
.poke-card .type {
    font-weight: bold;
    color: #666;
    font-size: 16px;
    margin-top: 5px;
}
.poke-card .power {
    font-size: 18px;
    font-weight: bold;
    color: #ff4081;
    margin-top: 10px;
}
</style>
"""
st.markdown(card_css, unsafe_allow_html=True)

def show_card(pokemon, power, title):
    html = f"""
    <div class="poke-card">
        <img src="{clean_url(pokemon['image_url'])}" />
        <h3>{pokemon['name']}</h3>
        <div class="type">Type: {pokemon['type']}</div>
        <div class="power">{title} Power: {power}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

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

# -- Main Layout --
st.title("🔴 Pokémon Match – Type-Based Fair Fights")
st.markdown("Choose your fighter and battle Pokémon of the same type!")

st.markdown(f"### 💚 Lives: {st.session_state.lives}")

# Fighter selector
team_names = [p['name'] for p in st.session_state.team]
selected_name = st.selectbox("🧠 Choose your Pokémon to battle:", team_names)

# Update selected
st.session_state.selected_pokemon = next(p for p in st.session_state.team if p['name'] == selected_name)

# Enemy Pokémon section
if st.session_state.enemy_pokemon:
    col1, col2 = st.columns(2)

    player_power = st.session_state.selected_pokemon['attack'] + random.randint(0, 10)
    enemy_power = st.session_state.enemy_pokemon['attack'] + random.randint(0, 10)

    with col1:
        show_card(st.session_state.selected_pokemon, player_power, "Your")

    with col2:
        show_card(st.session_state.enemy_pokemon, enemy_power, "Enemy")

    col3, col4 = st.columns(2)
    col3.button("⚔️ Fight", on_click=battle)
    col4.button("⏭️ Skip", on_click=choose_enemy)
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
