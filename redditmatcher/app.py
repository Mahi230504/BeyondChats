import streamlit as st
import re
from core.reddit_scraper import get_user_data
from core.persona_generator import generate_persona

# --- Custom CSS for Enhanced Section Division and Visuals ---
st.markdown("""
    <style>
    .persona-header {
        background: linear-gradient(90deg, #f8b500 0%, #fceabb 100%);
        border-radius: 14px 14px 0 0;
        padding: 28px 24px 14px 24px;
        margin-bottom: 0;
        color: #2d2d2d;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-bottom: 4px solid #f8b500;
    }
    .section-divider {
        height: 10px;
        background: linear-gradient(90deg, #f8b500 0%, #fceabb 100%);
        border: none;
        margin: 0 0 24px 0;
        border-radius: 0 0 14px 14px;
    }
    .section-block {
        background: #fffdfa;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 22px 24px 14px 24px;
        margin-bottom: 22px;
        border: 1.5px solid #f8b50033;
    }
    .section-title {
        font-weight: 700;
        font-size: 1.12rem;
        margin-top: 0;
        margin-bottom: 10px;
        color: #f8b500;
        letter-spacing: 0.5px;
    }
    .trait-badge {
        display: inline-block;
        background: #fceabb;
        color: #b47a00;
        border-radius: 8px;
        padding: 3px 10px;
        margin: 2px 4px 2px 0;
        font-size: 0.92rem;
        font-weight: 600;
    }
    .motivation-badge {
        display: inline-block;
        background: #e6f4ea;
        color: #007f5f;
        border-radius: 8px;
        padding: 3px 10px;
        margin: 2px 4px 2px 0;
        font-size: 0.92rem;
        font-weight: 600;
    }
    .degree-display-group {
        display: flex;
        align-items: center;
        margin-bottom: 5px; /* Small margin between each trait/motivation line */
    }
    .degree-label-side {
        font-size: 0.75rem;
        color: #555;
        margin: 0 4px; /* Adjust margin to place labels just outside the scale */
    }
    .degree-scale-container {
        display: inline-block;
        width: 100px; /* Increased width */
        height: 12px; /* Slightly increased height for better visibility */
        background-color: #e0e0e0;
        border-radius: 6px;
        overflow: hidden;
        vertical-align: middle;
        position: relative;
    }
    .degree-scale-fill {
        height: 100%;
        background-color: #4CAF50; /* Green color for the fill */
        border-radius: 6px;
        position: absolute;
        left: 0;
        top: 0;
    }
    .subreddit-pill {
        display: inline-block;
        background: #e6f4ea;
        color: #007f5f;
        border-radius: 8px;
        padding: 3px 10px;
        margin: 2px 4px 2px 0;
        font-size: 0.92rem;
        font-weight: 600;
    }
    .sentiment-pill {
        display: inline-block;
        background: #e0f7fa; /* A light blue/cyan for sentiments */
        color: #006064; /* Darker blue/cyan */
        border-radius: 8px;
        padding: 3px 10px;
        margin: 2px 4px 2px 0;
        font-size: 0.92rem;
        font-weight: 600;
    }
    .info-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 10px;
    }
    .info-table td {
        padding: 4px 8px;
        font-size: 1.02rem;
        border-bottom: 1px solid #f8b50022;
    }
    .info-table tr:last-child td {
        border-bottom: none;
    }
    .persona-quote {
        font-style: italic;
        color: #ff6600;
        font-size: 1.15rem;
        margin: 22px 0 12px 0;
        padding-left: 18px;
        border-left: 4px solid #ff6600;
    }
    .three-col-flex {
        display: flex;
        gap: 24px;
        margin-top: 0;
        margin-bottom: 0;
    }
    .three-col-block {
        flex: 1;
        background: #fffdfa;
        border-radius: 12px;
        padding: 18px 18px 10px 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        border: 1.2px solid #f8b50022;
        margin-bottom: 0;
    }
    ul {
        margin-bottom: 0.1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Reddit User Persona Generator", layout="wide")
st.title("Reddit User Persona Generator")

url = st.text_input("Enter a Reddit profile URL:")

def get_username_from_url(url):
    match = re.search(r"(?:reddit.com/u/|reddit.com/user/)([^/]+)", url)
    if match:
        return match.group(1)
    return None

if st.button("Generate Persona"):
    if url:
        username = get_username_from_url(url)
        if username:
            with st.spinner(f"Scraping data for u/{username}..."):
                user_data = get_user_data(username)
            

            if user_data:
                st.success(f"Successfully scraped data for u/{username}.")
                with st.spinner("Generating persona..."):
                    persona = generate_persona(user_data)

                if persona and "error" in persona:
                    st.error(f"Error generating persona: {persona['error']}")
                elif persona:
                    # --- Persona Header Card ---
                    st.markdown(f"""
                        <div class="persona-header">
                            <div style="display:flex; align-items:flex-start; gap: 40px;">
                                <div style="flex:1;">
                                    <h2 style="margin-bottom:0;">{persona.get('name', username)}</h2>
                                    <table class="info-table">
                                        <tr><td><strong>Age</strong></td><td>{persona.get('age', 'N/A')}</td></tr>
                                        <tr><td><strong>Occupation</strong></td><td>{persona.get('occupation', 'N/A')}</td></tr>
                                        <tr><td><strong>Status</strong></td><td>{persona.get('status', 'N/A')}</td></tr>
                                        <tr><td><strong>Location</strong></td><td>{persona.get('location', 'N/A')}</td></tr>
                                        <tr><td><strong>Comment Karma</strong></td><td>{persona.get('comment_karma', 'N/A')}</td></tr>
                                        <tr><td><strong>Link Karma</strong></td><td>{persona.get('link_karma', 'N/A')}</td></tr>
                                    </table>
                                </div>
                                <div style="flex-shrink: 0;">
                                    {f'<img src="{persona.get('profile_picture', user_data.get('profile_img', ''))}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; border: 3px solid #f8b500;" />' if persona.get('profile_picture') or user_data.get('profile_img') else ''}
                                </div>
                            </div>
                            {f'<div class="persona-quote">"{persona["summary_quote"]}"</div>' if persona.get('summary_quote') else ''}
                            <div style="display:flex; justify-content:space-around; margin-top: 30px;">
                                <div style="flex:1; padding-right: 10px;">
                                    <div class="section-title" style="color: black;">Motivations</div>
                                    <div style="text-align:left; padding-left:10px;">
                                    {''.join([
                                            f'<div class="degree-display-group">' +
                                            f'<span class="motivation-badge">{item.get("motivation", "")}</span>' +
                                            f'<span class="degree-label-side">1</span>' +
                                            f'<div class="degree-scale-container"><div class="degree-scale-fill" style="width: {item.get("degree", 0) * 10}%;"></div></div>' +
                                            f'<span class="degree-label-side">10</span>' +
                                            f'</div>' +
                                            (''.join([f'<div style="font-size:0.85rem; color:#666; margin-left:10px; font-style:italic;">"{citation}"</div>' for citation in item.get('citations', [])]) if item.get('citations') else '')
                                            for item in persona.get("motivations", [])
                                        ])}
                                    </div>
                                </div>
                                <div style="flex:1; padding-left: 10px;">
                                    <div class="section-title" style="color: black;">Personality Traits</div>
                                    <div style="text-align:left; padding-left:10px;">
                                    {''.join([
                                            f'<div class="degree-display-group">' +
                                            f'<span class="trait-badge">{item.get("trait", "")}</span>' +
                                            f'<span class="degree-label-side">1</span>' +
                                            f'<div class="degree-scale-container"><div class="degree-scale-fill" style="width: {item.get("degree", 0) * 10}%;"></div></div>' +
                                            f'<span class="degree-label-side">10</span>' +
                                            f'</div>' +
                                            (''.join([f'<div style="font-size:0.85rem; color:#666; margin-left:10px; font-style:italic;">"{citation}"</div>' for citation in item.get('citations', [])]) if item.get('citations') else '')
                                            for item in persona.get("personality_traits", [])
                                        ])}
                                    </div>
                                </div>
                            </div>
                            <div style="display:flex; justify-content:space-around; margin-top: 30px;">
                                <div style="flex:1; padding-right: 10px;">
                                    <div class="section-title" style="color: black;">Active Subreddits</div>
                                    {''.join([f'<span class="subreddit-pill">r/{sr}</span>' for sr in persona.get("subreddits_active", [])])}
                                </div>
                                <div style="flex:1; padding-left: 10px;">
                                    <div class="section-title" style="color: black;">Sentiment & Tone</div>
                                    <span class="sentiment-pill">{persona.get("sentiment_tone", "N/A")}</span>
                                </div>
                            </div>
                        </div>
                        <hr class="section-divider">
                    """, unsafe_allow_html=True)

                    # --- Summary Quote ---
                    if persona.get('summary_quote'):
                        st.markdown(f'<div class="persona-quote">"{persona["summary_quote"]}"</div>', unsafe_allow_html=True)

                    # --- Section Blocks with Clear Divisions ---
                    st.markdown('<div class="section-block">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Behaviour & Habits</div>', unsafe_allow_html=True)
                    st.markdown("<ul>" + "".join([
                        f"<li>{item.get('habit', '')}" +
                        ("".join([f'<div style="font-size:0.85rem; color:#666; margin-left:10px; font-style:italic;">"{citation}"</div>' for citation in item.get('citations', [])]) if item.get('citations') else '') +
                        "</li>" for item in persona.get("behaviour_habits", [])
                    ]) + "</ul>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-block">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Frustrations</div>', unsafe_allow_html=True)
                    st.markdown("<ul>" + "".join([
                        f"<li>{item.get('frustration', '')}" +
                        ("".join([f'<div style="font-size:0.85rem; color:#666; margin-left:10px; font-style:italic;">"{citation}"</div>' for citation in item.get('citations', [])]) if item.get('citations') else '') +
                        "</li>" for item in persona.get("frustrations", [])
                    ]) + "</ul>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-block">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Goals & Needs</div>', unsafe_allow_html=True)
                    st.markdown("<ul>" + "".join([
                        f"<li>{item.get('goal_need', '')}" +
                        ("".join([f'<div style="font-size:0.85rem; color:#666; margin-left:10px; font-style:italic;">"{citation}"</div>' for citation in item.get('citations', [])]) if item.get('citations') else '') +
                        "</li>" for item in persona.get("goals_needs", [])
                    ]) + "</ul>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("---")
                    
                    # Prepare persona for download
                    persona_text_content = f"""
User Persona for {persona.get('name', username)}

--- Basic Information ---
Age: {persona.get('age', 'N/A')}
Occupation: {persona.get('occupation', 'N/A')}
Status: {persona.get('status', 'N/A')}
Location: {persona.get('location', 'N/A')}
Comment Karma: {persona.get('comment_karma', 'N/A')}
Link Karma: {persona.get('link_karma', 'N/A')}

--- Personality Traits ---
{chr(10).join([f'- {item.get('trait', '')}' + (chr(10) + chr(10).join([f'  > "{citation}"' for citation in item.get('citations', [])]) if item.get('citations') else '') for item in persona.get('personality_traits', [])])}

--- Motivations ---
{chr(10).join([f'- {item.get('motivation', '')}' + (chr(10) + chr(10).join([f'  > "{citation}"' for citation in item.get('citations', [])]) if item.get('citations') else '') for item in persona.get('motivations', [])])}

--- Active Subreddits ---
{', '.join([f'r/{sr}' for sr in persona.get('subreddits_active', [])])}

--- Sentiment & Tone ---
{persona.get('sentiment_tone', 'N/A')}

--- Summary Quote ---
"{persona.get('summary_quote', '')}"

--- Behaviour & Habits ---
{chr(10).join([f'- {item.get('habit', '')}' + (chr(10) + chr(10).join([f'  > "{citation}"' for citation in item.get('citations', [])]) if item.get('citations') else '') for item in persona.get('behaviour_habits', [])])}

--- Frustrations ---
{chr(10).join([f'- {item.get('frustration', '')}' + (chr(10) + chr(10).join([f'  > "{citation}"' for citation in item.get('citations', [])]) if item.get('citations') else '') for item in persona.get('frustrations', [])])}

--- Goals & Needs ---
{chr(10).join([f'- {item.get('goal_need', '')}' + (chr(10) + chr(10).join([f'  > "{citation}"' for citation in item.get('citations', [])]) if item.get('citations') else '') for item in persona.get('goals_needs', [])])}
"""
                    st.download_button(
                        label="Download Persona as Text",
                        data=persona_text_content,
                        file_name=f"{username}_persona.txt",
                        mime="text/plain"
                    )

                    with st.expander("View Raw Data"):
                        st.json(user_data)
            else:
                st.warning("Could not retrieve data for this user.")
        else:
            st.warning("Please enter a valid Reddit profile URL.")
    else:
        st.warning("Please enter a Reddit profile URL.")
