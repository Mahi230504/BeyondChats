# Reddit User Persona Generator

This application generates a user persona based on a given Reddit profile URL. It scrapes user data, uses the Gemini API to create a detailed persona, and visualizes comment topic distribution.

## Setup and Installation

Follow these steps to set up and run the application:

1.  **Clone the git repository and Navigate to the `redditmatcher` directory:**

    ```bash
    git clone https://github.com/Mahi230504/BeyondChats.git
    cd redditmatcher
    ```

2.  **Create a Python Virtual Environment (recommended):**

    ```bash
    python3 -m venv my_env
    ```

3.  **Activate the Virtual Environment:**

    *   **On macOS/Linux:**

        ```bash
        source my_env/bin/activate
        ```

    *   **On Windows:**

        ```bash
        .\my_env\Scripts\activate
        ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables:**

    Create a `.env` file in the `redditmatcher` directory with the following content:

    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    PEOPLE_API_KEY="YOUR_PEOPLE_DATA_LABS_API_KEY"
    REDDIT_CLIENT_ID="YOUR_REDDIT_CLIENT_ID"
    REDDIT_CLIENT_SECRET="YOUR_REDDIT_CLIENT_SECRET"
    REDDIT_USER_AGENT="YOUR_REDDIT_USER_AGENT" # e.g., "PersonaGenerator/1.0 (by YourRedditUsername)"
    ```

    *   Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.
    *   Replace `YOUR_PEOPLE_DATA_LABS_API_KEY` with your actual People Data Labs API key (optional, but recommended for richer personas).
    *   Replace `YOUR_REDDIT_CLIENT_ID`, `YOUR_REDDIT_CLIENT_SECRET`, and `YOUR_REDDIT_USER_AGENT` with your Reddit API credentials. You can obtain these by creating an app on Reddit's developer portal.

6.  **Run the Streamlit Application:**

    ```bash
    streamlit run app.py
    ```

    This will open the application in your web browser.

## Usage

1.  Enter a Reddit profile URL in the provided input field.
2.  Click the "Generate Persona" button.
3.  The application will display the generated user persona, including personality traits, motivations, and comment topic distribution.
4.  A `.txt` file containing the complete persona will be saved in the `redditmatcher` directory with the name `[username]_persona.txt`.

## Project Structure

```
redditmatcher/
├── .env
├── .gitignore
├── app.py
├── persona_prompt.txt
├── requirements.txt
├── api/
│   ├── people_api.py
│   └── reddit_api.py
└── core/
    ├── persona_generator.py
    ├── reddit_scraper.py
    └── topic_modeling.py
```
