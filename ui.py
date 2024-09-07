import streamlit as st
import requests

def send_data_to_api(text, file):
    url = "https://api.example.com/endpoint"  # Replace with your API endpoint URL
    
    files = {"file": file}
    data = {"text": text}
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        st.success("Data sent successfully!")
    else:
        st.error("Failed to send data.")

def main():
    st.title("Data Input and Upload")
    
    # Text input
    text_input = st.text_input("What lesson should I sing? 😊")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a file")
    
    if st.button("Send Data"):
        if text_input and uploaded_file:
            send_data_to_api(text_input, uploaded_file)
        else:
            st.warning("Please provide both text input and file.")

if __name__ == "__main__":
    main()
