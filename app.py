import streamlit as st
import random

# ---- Setup ----
POKEMON_DATA = {
    "Pikachu": {
        "type": "Electric",
        "hp": 35,
        "attack": 55,
        "image": "pikachu.png"
    },
    "Bulbasaur": {
        "type": "Grass/Poison",
        "hp": 45,
        "attack": 49,
        "image": "bulbasaur.png"
    },
    "Charmander": {
        "type": "Fire",
        "hp": 39,
        "attack": 52,
        "image": "charmander.png"
    }
}

if "player_team" not in st.session_state:
    st.session_state.player_team = ["Pikachu"]
    st.session_state.lives = 3
    st.session_state.ai_pokemon = None
    st.session_state.status = ""
    st.session_state.last_outcome = ""

# ---- Functions ----
def choose_new_ai():
    choices = [p for p in POKEMON_DATA if p not in st.session_state.player_team]
    if choices:
        st.session_state.ai_pokemon = random.choice(choices)
        st.session_state.status = f"AI challenges you with {st.session_state.ai_pokemon}!"
        st.session_state.last_outcome = ""
    else:
        st.session_state.ai_pokemon = None
        st.session_state.status = "You've collected all Pokémon!"

def fight():
    player = POKEMON_DATA[st.session_state.player_team[-1]]
    enemy = POKEMON_DATA[st.session_state.ai_pokemon]

    player_power = player['attack'] + random.randint(0, 10)
    enemy_power = enemy['attack'] + random.randint(0, 10)

    if player_power >= enemy_power:
        st.session_state.player_team.append(st.session_state.ai_pokemon)
        st.session_state.last_outcome = f"You won! {st.session_state.ai_pokemon} added to your team!"
    else:
        st.session_state.lives -= 1
        st.session_state.last_outcome = f"You lost the fight. Lives left: {st.session_state.lives}"

    choose_new_ai()

def skip():
    st.session_state.last_outcome = "You skipped the fight."
    choose_new_ai()

# ---- UI ----
st.title("🔴 Pokémon Match – Streamlit Edition")

st.markdown(f"**Lives:** {st.session_state.lives}")
st.markdown(f"**Your Team:** {', '.join(st.session_state.player_team)}")
st.markdown("---")

if st.session_state.ai_pokemon:
    p = POKEMON_DATA[st.session_state.ai_pokemon]
    st.image(p["image"], width=150)
    st.markdown(f"### {st.session_state.ai_pokemon}")
    st.markdown(f"Type: {p['type']}  \nHP: {p['hp']} | Attack: {p['attack']}")
    st.button("⚔️ Fight!", on_click=fight)
    st.button("⏭️ Skip", on_click=skip)
else:
    if st.session_state.lives <= 0:
        st.error("Game Over! You lost all your lives.")
    elif len(st.session_state.player_team) == len(POKEMON_DATA):
        st.success("🎉 Congratulations! You collected all Pokémon!")
    else:
        st.button("Start Battle", on_click=choose_new_ai)

if st.session_state.last_outcome:
    st.markdown("---")
    st.info(st.session_state.last_outcome)

if st.session_state.status:
    st.markdown("---")
    st.write(st.session_state.status)
