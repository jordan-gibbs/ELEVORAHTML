import streamlit as st
from bs4 import BeautifulSoup
import io

def modify_htm(content):
    # Parse the HTM with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Remove the top navigation links (Job Dashboard, Resources, Account)
    for link in soup.find_all('a', href=True):
        if 'jobpositions' in link['href'] or 'candidates' in link['href'] or 'resources' in link['href'] or 'account' in \
                link['href']:
            link.decompose()

    # Remove the 'Back to Results Table' button
    back_button = soup.find(lambda tag: tag.name == "button" and "Back to Results Table" in tag.text)
    if back_button:
        back_button.decompose()

    # Remove the error flash message
    error_message = soup.find('div', id='disconnected')
    if error_message:
        error_message.decompose()

    # Remove Grammarly integration
    grammarly = soup.find('grammarly-desktop-integration')
    if grammarly:
        grammarly.decompose()

    for script in soup.find_all('script', {'defer': '', 'phx-track-static': '', 'type': 'text/javascript'}, src=True):
        if script['src'].startswith('./Elevora_files/app-') and script['src'].endswith('.js.download'):
            script.decompose()
            break

    # Save the modified HTM to a new file
    with open('Elevora_results.htm', 'w', encoding='utf-8') as file:
        file.write(str(soup.prettify()))

    return soup.prettify()

def save_htm(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Streamlit UI
def get_htm_download_link(modified_htm, filename):
    # Generate a link to download the modified HTM file
    buffer = io.BytesIO()
    buffer.write(modified_htm.encode())
    buffer.seek(0)
    return st.download_button(label="Download Modified File", data=buffer, file_name=filename, mime="text/html")

# Streamlit UI
st.set_page_config(page_title='HTM File Modifier', page_icon=':moon:', initial_sidebar_state='auto')

# File uploader
uploaded_file = st.file_uploader("Choose the HTML File", type="htm")

# Text input for output file name
name = st.text_input("Enter User's Name")

if uploaded_file is not None and name:
    # Read and modify the HTM content
    content = uploaded_file.getvalue().decode("utf-8")
    modified_content = modify_htm(content)

    # Generate download button
    output_filename = f"{name}-interview-results.htm"
    get_htm_download_link(modified_content, output_filename)
else:
    st.warning("Please upload an HTM file and enter a name.")
