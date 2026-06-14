# TP : Agent Intelligent - Chef Cuisinier Personnel
**Auteur : HYNDI ELMEHDI**

## 1. Présentation du Projet
Ce projet consiste en la création d'un agent intelligent jouant le rôle d'un chef cuisinier personnel. L'agent utilise un modèle de langage local (LLM) via **Ollama**, intègre un mécanisme de **mémoire** pour les préférences utilisateur, et utilise le **RAG (Retrieval-Augmented Generation)** ainsi que la **recherche web (Tavily)** pour fournir des recettes personnalisées et sécurisées.

## 2. Fonctionnalités de l'Agent
L'agent remplit les objectifs suivants :
- **Prise en compte des ingrédients :** Analyse des ingrédients disponibles dans le réfrigérateur fournis par l'utilisateur.
- **Mémoire Personnalisée :** Mémorisation des préférences culinaires, aversions et allergies (ex: allergie au citron).
- **RAG (Local Recipe Search) :** Recherche dans une base de données locale de recettes (`recipes/`) pour des suggestions "maison".
- **Recherche Web (Tavily) :** Complète ses connaissances avec des recettes ou techniques en temps réel sur internet.
- **Sécurité Alimentaire :** Vérifie systématiquement les allergènes et propose des substituts sûrs (ex: vinaigre au lieu du citron).

## 3. Architecture Technique (Workflow)
Le flux de travail suit les étapes suivantes :
1. **Input :** L'utilisateur saisit ses ingrédients et ses contraintes.
2. **Analyse de l'Agent (Brain) :** Le modèle `llama3.2:3b` (Ollama) traite la demande.
3. **Récupération (RAG/Web) :** 
   - L'agent interroge d'abord les fichiers locaux `.md` dans le dossier `recipes/`.
   - Si aucune recette locale ne convient ou n'est sûre, il utilise l'API **Tavily** pour chercher sur le web.
4. **Filtrage de Mémoire :** L'agent compare les résultats trouvés avec les allergies stockées dans l'historique de la conversation.
5. **Génération de la Réponse :** Le chef propose une recette détaillée avec les instructions de préparation et les mentions de sécurité nécessaires.

## 4. Guide d'Installation
1. **Prérequis :**
   - Python 3.10+
   - Ollama (avec le modèle `llama3.2:3b` installé)
2. **Installation des dépendances :**
   ```bash
   pip install langchain-ollama langchain-community langgraph python-dotenv tavily-python
   ```
3. **Configuration :**
   - Placer vos recettes locales dans le dossier `recipes/`.
   - Configurer votre `TAVILY_API_KEY` dans un fichier `.env`.

## 5. Captures d'Écran (Screenshots)

### 5.1 Test de la Mémoire et des Ingrédients
*(Insérer ici la capture d'écran montrant l'initialisation avec les ingrédients et l'allergie au citron)*

### 5.2 Test du RAG (Recherche Locale)
*(Insérer ici la capture d'écran montrant le Chef trouvant la recette de poulet locale et signalant l'allergène)*

### 5.3 Test de la Recherche Web et Substitution
*(Insérer ici la capture d'écran montrant le Chef proposant une alternative sans ail/citron via le web)*

---
*Projet réalisé dans le cadre du TP : Chef Personnel.*
