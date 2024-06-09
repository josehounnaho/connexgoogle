import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Chemin vers le fichier de configuration Firebase Admin SDK (à télécharger depuis la Console Firebase)
cred = credentials.Certificate('localisatio-40250-firebase-adminsdk-az73x-9014a55c9c.json')

# Vérifiez si Firebase a déjà été initialisé avant d'appeler initialize_app()
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Fonction pour inscrire un utilisateur avec Firebase Auth
def register_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        st.success(f"Inscription réussie pour l'utilisateur : {user.uid}")
    except Exception as e:
        st.error(f"Erreur lors de l'inscription : {e}")

# Fonction pour connecter un utilisateur avec Firebase Auth
def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.success(f"Connexion réussie pour l'utilisateur : {user.uid}")
    except Exception as e:
        st.error(f"Erreur lors de la connexion : {e}")

# Interface utilisateur avec Streamlit
def main():
    st.title('Gestion Utilisateurs avec Firebase')

    # Déclaration de l'état de la session
    session_state = st.session_state.setdefault(
        'page', 'login'  # Par défaut, commence par la page de connexion
    )

    # Navigation entre les pages
    if session_state == 'login':
        login_page()
    elif session_state == 'register':
        register_page()

def login_page():
    st.header('Connexion')
    email_login = st.text_input('Email')
    password_login = st.text_input('Mot de passe', type='password')

    if st.button('Se connecter'):
        login_user(email_login, password_login)

    st.markdown('### Pas encore inscrit ?')
    if st.button('S\'inscrire'):
        st.session_state['page'] = 'register'

def register_page():
    st.header('Inscription')
    email_reg = st.text_input('Email')
    password_reg = st.text_input('Mot de passe', type='password')
    confirm_password = st.text_input('Confirmez le mot de passe', type='password')

    if st.button('S\'inscrire'):
        if password_reg == confirm_password:
            register_user(email_reg, password_reg)
            st.session_state['page'] = 'login'  # Après inscription, revenir à la page de connexion
        else:
            st.error('Les mots de passe ne correspondent pas.')

    st.markdown('### Déjà inscrit ?')
    if st.button('Se connecter'):
        st.session_state['page'] = 'login'

if __name__ == '__main__':
    main()
