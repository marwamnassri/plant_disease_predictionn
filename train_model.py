import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
df = pd.read_csv("data/plant_disease.csv")



# Encodage
le_disease = LabelEncoder()
df['disease_code'] = le_disease.fit_transform(df['disease'])

X = df[['symptom_1', 'symptom_2', 'symptom_3']].apply(LabelEncoder().fit_transform)
y = df['disease_code']

# Modèle
model = RandomForestClassifier()
model.fit(X, y)

# Sauvegarde
joblib.dump(model, "models/model.pkl")
joblib.dump(le_disease, "models/label_encoder.pkl")
