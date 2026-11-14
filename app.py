
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Mon application",
    page_icon="🚀",
    layout="centered"
)

FICHIER = "utilisateurs.json"
MOT_DE_PASSE_ADMIN = "Admin123"

# Charger les utilisateurs
def charger_utilisateurs():
    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    return []

# Enregistrer les utilisateurs
def sauvegarder_utilisateurs(utilisateurs):
    with open(FICHIER, "w", encoding="utf-8") as fichier:
        json.dump(utilisateurs, fichier, ensure_ascii=False, indent=4)

st.title("🚀 MON APPLICATION")

menu = st.sidebar.selectbox(
    "📌 Navigation",
    ["Accueil", "Administration"]
)

if menu == "Accueil":
    st.header("Bienvenue !")
    st.write("Bienvenue sur ma première application.")

    prenom = st.text_input("Comment tu t'appelles ?")

    if st.button("Valider"):
        if prenom.strip():
            utilisateurs = charger_utilisateurs()

            utilisateurs.append({
                "prenom": prenom.strip(),
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            sauvegarder_utilisateurs(utilisateurs)

            st.success(f"Bienvenue {prenom} !")
        else:
            st.warning("Entre ton prénom.")

elif menu == "Administration":
    st.header("🔐 Espace administrateur")

    mot_de_passe = st.text_input(
        "Mot de passe administrateur",
        type="password"
    )

    if st.button("Se connecter"):
        if mot_de_passe == MOT_DE_PASSE_ADMIN:
            st.session_state.admin_connecte = True
        else:
            st.error("Mot de passe incorrect.")

    if st.session_state.get("admin_connecte", False):
        st.success("Connecté en administrateur !")

        utilisateurs = charger_utilisateurs()

        st.metric("Nombre d'inscriptions", len(utilisateurs))

        st.subheader("👥 Liste des utilisateurs")

        if utilisateurs:
            st.dataframe(utilisateurs, use_container_width=True)
        else:
            st.info("Aucun utilisateur pour le moment.")

        if st.button("Se déconnecter"):
            st.session_state.admin_connecte = False
            st.rerun()
