import streamlit as st
import streamlit_antd_components as sac
from streamlit_lottie import st_lottie
import requests


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def send_data_to_api(text, file):
    # Placeholder for API call
    st.success("Your lesson request has been submitted successfully! 🎉")


def main():
    st.set_page_config(
        page_title="VocalVista - AI Singing Lessons", layout="wide")
    local_css("style.css")

    # Sidebar for navigation
    with st.sidebar:
        st.image("logo.png", width=200)
        selected = sac.menu([
            sac.MenuItem('Home', icon='house'),
            sac.MenuItem('Request Lesson', icon='music-note'),
            sac.MenuItem('About', icon='info-circle')
        ], format_func='title', open_all=True, gap='10px')

    # Main content area
    if selected == 'Home':
        st.title("Welcome to VocalVista 🎤")
        st.subheader("Your AI-Powered Singing Coach")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <p style="font-size: 1.2em; line-height: 1.5;">
            Embark on a personalized journey to vocal excellence with VocalVista. 
            Our cutting-edge AI technology tailors each lesson to your unique voice and goals.
            </p>
            """, unsafe_allow_html=True)
            st.button("Start Your Vocal Journey", type="primary")
        with col2:
            lottie_singing = load_lottieurl(
                "https://assets5.lottiefiles.com/packages/lf20_rjn0esjh.json")
            st_lottie(lottie_singing, height=200)

        st.markdown("<hr style='border:1px solid #e0e0e0;'>",
                    unsafe_allow_html=True)

        st.subheader("Why Choose VocalVista?")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Personalized Lessons",
                      value="100%", delta="Tailored for You")
        with col2:
            st.metric(label="Genres Covered", value="50+",
                      delta="Expanding Weekly")
        with col3:
            st.metric(label="User Satisfaction", value="98%",
                      delta="Based on 10,000+ reviews")

    elif selected == 'Request Lesson':
        st.title("Request Your Personalized Lesson 🎵")

        with st.form("lesson_request_form"):
            st.markdown(
                "<p style='font-size:1.1em;'>Tell us about the lesson you'd like to receive.</p>", unsafe_allow_html=True)
            lesson_type = st.selectbox(
                "What type of lesson are you looking for?",
                ["Vocal Technique", "Genre-Specific",
                    "Song Practice", "Performance Preparation"]
            )

            specific_request = st.text_area(
                "Describe your specific goals or requests",
                placeholder="E.g., 'I want to improve my breath control for long phrases in pop ballads'"
            )

            skill_level = st.slider("Your current skill level", 1, 5, 3)

            uploaded_file = st.file_uploader(
                "Upload a reference audio file (optional)",
                type=["mp3", "wav"],
                help="This helps us understand your current level and style"
            )

            submitted = st.form_submit_button("Request Personalized Lesson")
            if submitted:
                if specific_request:
                    send_data_to_api(specific_request, uploaded_file)
                else:
                    st.warning(
                        "Please provide some details about your lesson request.🤔")

    elif selected == 'About':
        st.title("About VocalVista")
        st.markdown("""
        <p style="font-size: 1.2em; line-height: 1.5;">
        VocalVista is at the forefront of AI-powered music education. Our mission is to make 
        high-quality vocal training accessible to everyone, regardless of location or schedule.
        </p>
        """, unsafe_allow_html=True)

        st.subheader("Our Technology")
        st.markdown("""
        <p style="font-size: 1.2em; line-height: 1.5;">
        We use advanced machine learning algorithms trained on data from world-class vocal coaches. 
        This allows us to provide personalized, adaptive lessons that evolve with your progress.
        </p>
        """, unsafe_allow_html=True)

        st.subheader("Frequently Asked Questions")
        faq = sac.accordion([
            sac.AccordionItem("How does the AI generate lessons?",
                              "Our AI analyzes your voice, goals, and progress to create custom lesson plans and exercises."),
            sac.AccordionItem("Can I use this app on mobile devices?",
                              "Yes! VocalVista is fully responsive and works seamlessly on smartphones and tablets."),
            sac.AccordionItem("How often should I practice?",
                              "We recommend 15-30 minutes daily for optimal progress, but any consistent practice is beneficial.")
        ], gap='5px', format_func='title')


if __name__ == "__main__":
    main()
