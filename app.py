import streamlit as st
import pandas as pd
import joblib
from database import insert_history, init_db
from sklearn.preprocessing import LabelEncoder

# Initialiser la base de données
init_db()

# Charger le modèle et l'encodeur label
model = joblib.load("models/model.pkl")
label_disease = joblib.load("models/label_encoder.pkl")

# Symptômes possibles (fixes)
symptom_list = [
    'leaf_spot', 'yellow_leaf', 'wilt', 'brown_spot', 
    'dry_leaves', 'stunted_growth', 'leaf_curl'
]

# Encodeur pour symptômes
le_symptom = LabelEncoder()
le_symptom.fit(symptom_list)

# Style général (CSS intégré)
st.markdown("""
    <style>
        .main {
            background: #f5f7fa;
            color: #222222;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .title {
            color: #2c6b45;
            font-weight: 700;
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
        }
        .section-header {
            color: #4a90e2;
            font-weight: 600;
            font-size: 1.6rem;
            margin-top: 2rem;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid #4a90e2;
            padding-bottom: 0.3rem;
        }
        .footer {
            margin-top: 4rem;
            font-size: 0.8rem;
            color: #555555;
            text-align: center;
            opacity: 0.6;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="title">🌿 Détection Intelligente des Maladies des Plantes</h1>', unsafe_allow_html=True)
st.markdown("##### Détectez rapidement la maladie de vos cultures et obtenez un traitement adapté.")

# Disposition en colonnes pour les inputs
col1, col2 = st.columns(2)

with col1:
    plant = st.selectbox("🌱 Plante", ["Tomato", "Corn", "Potato", "Wheat"])
    st.markdown("**Choisissez la plante à diagnostiquer.**")

with col2:
    symptom_1 = st.selectbox("🩺 Symptôme 1", symptom_list)
    symptom_2 = st.selectbox("🩺 Symptôme 2", symptom_list)
    symptom_3 = st.selectbox("🩺 Symptôme 3", symptom_list)
    st.markdown("**Sélectionnez les 3 symptômes observés.**")

st.markdown("---")

# Bouton prédiction centré
predict_btn = st.button("🔍 Prédire la maladie")

if predict_btn:
    # Encoder les symptômes
    X_test = [[symptom_1, symptom_2, symptom_3]]
    df = pd.DataFrame(X_test, columns=["symptom_1", "symptom_2", "symptom_3"])
    df = df.apply(le_symptom.transform)

    # Prédiction
    pred_code = model.predict(df)[0]
    disease = label_disease.inverse_transform([pred_code])[0]

    # Récupérer traitement depuis CSV
    data = pd.read_csv("data/plant_disease.csv")
    treatment = data[data['disease'] == disease]['treatment'].values[0]

    # Affichage soigné des résultats
    st.markdown(f"""
        <div style="background-color:#e6f2ea; padding: 20px; border-radius: 10px; border: 2px solid #2c6b45;">
            <h2 style="color:#2c6b45;">🌱 Maladie détectée :</h2>
            <p style="font-size:1.6rem; font-weight:600; margin:0;">{disease.replace('_', ' ').title()}</p>
            <h3 style="color:#3d9970; margin-top:15px;">💊 Traitement recommandé :</h3>
            <p style="font-size:1.2rem; margin:0;">{treatment}</p>
        </div>
    """, unsafe_allow_html=True)

    # Enregistrer dans la BDD
    insert_history(plant, f"{symptom_1}, {symptom_2}, {symptom_3}", disease, treatment)

    st.success("✅ La prédiction a été enregistrée dans l'historique.")

# Affichage de l'historique des prédictions
st.markdown('<h2 class="section-header">📜 Historique des Prédictions</h2>', unsafe_allow_html=True)

try:
    import sqlite3
    conn = sqlite3.connect("plant_diseases.db")
    df_history = pd.read_sql_query("SELECT id, plant, symptoms, disease, treatment FROM history ORDER BY id DESC LIMIT 10", conn)
    conn.close()

    if not df_history.empty:
        # Mettre un joli style à la table
        styled_df = df_history.style.set_properties(**{
            'background-color': '#f0f9f4',
            'color': '#2c6b45',
            'border-color': '#a2d5ab'
        }).set_table_styles([{
            'selector': 'th',
            'props': [('background-color', '#4a7c59'), ('color', 'white')]
        }])

        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("Aucune prédiction enregistrée pour le moment.")
except Exception as e:
    st.error(f"Erreur lors du chargement de l'historique : {e}")

# Footer discret
st.markdown('<p class="footer">© 2025 Marwa Mnassri — Projet Data Science</p>', unsafe_allow_html=True)
