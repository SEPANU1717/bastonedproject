import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
from streamlit_option_menu import option_menu
from PIL import Image
import base64






def get_img_as_base64(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
        base64_encoded = base64.b64encode(image_data).decode("utf-8")
    return base64_encoded

background_image_path = "image/sm.png"

image_path = "image/logoside.png"
im = Image.open(image_path)

background_image = Image.open(background_image_path)

im = Image.open("image/mm.png")
im2 = Image.open("image/ba.png")

st.markdown("""<style> .css-1544g2n.e1fqkh3o4 {margin-top: -70px;}</style>""", unsafe_allow_html=True)
st.markdown("""<style> .css-uf99v8.egzxvld5 {margin-top: -50px;}</style>""", unsafe_allow_html=True)



with st.sidebar:
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write('')
    with col2:
        st.image(im2, caption='')

# Rest of your code goes here...



# Load the necessary data
book_df = pd.read_csv("final.csv")
similarity = pickle.load(open("similarity.pkl", "rb"))

# Sidebar menu
with st.sidebar:
    st.markdown('<p class="css-1rhbuit-sidebarWrapper">', unsafe_allow_html=True)
    selected = option_menu(
        menu_title="",
        options=["Home", "Recommendation", "Book List", "About Us", "Contact"],
        icons=['house', 'tags','filter', 'people', 'envelope']
    )
    st.markdown('</p>', unsafe_allow_html=True)



if selected == "Home":
    st.header("")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{get_img_as_base64(background_image_path)}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
    
elif selected == "Recommendation":
    st.header("Book Recommendation System for Programmers")

    list_book = np.array(book_df["Title"])
    list_book_placeholder = [''] + list_book.tolist()  # Add an empty string as a placeholder option
    option = st.selectbox("Select Book", list_book_placeholder)

    # Function to get recommended book URLs
    def show_url(book):
        x = []
        index = book_df[book_df['Title'] == book].index
        if len(index) > 0:
            index = index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            for i in distances[1:6]:
                url = book_df.iloc[i[0]]['urls']
                x.append(url)
        return x

    # Function to get recommended book titles and descriptions
    def book_recommend(book):
        distances = similarity[list_book == book][0]
        indices = np.argsort(distances)[::-1][1:6]
        recommended_books = list_book[indices]
        recommended_descriptions = book_df.iloc[indices]['Description']
        return recommended_books, recommended_descriptions

    # Button to get recommendations
    if st.button('Recommend Me'):
        if option == '':
            st.write("No book selected. Please choose a book from the list.")
        else:
            recommended_books, recommended_descriptions = book_recommend(option)
            if len(recommended_books) > 0:
                st.write('Books recommended for "{}" are:'.format(option))
                df = pd.DataFrame({
                    'Book Recommended': recommended_books,
                    'Description': recommended_descriptions,
                    'Book Url': show_url(option)
                })
                # Format URLs as hyperlinks
                df['Book Url'] = df['Book Url'].apply(lambda x: '<a href="{}" target="_blank">Link</a>'.format(x))
                df.index = [''] * len(df.index)
                st.write(df.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.write("No books found for '{}'.".format(option))

elif selected == "Book List":
    st.header("Book List")

    # Define function to load CSV files
    def load_data(folder_path):
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        data_dict = {}
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            data_dict[file[:-4]] = pd.read_csv(file_path)
        return data_dict

    # Load CSV files and create select box
    data_dict = load_data('csvfiles')
    file_name = st.selectbox('Select a Programming language:', list(data_dict.keys()))
    df = data_dict[file_name]

    # Show the selected CSV file
    if st.button('Show Books'):
        df['url'] = df['url'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
        st.write(df.to_html(escape=False), unsafe_allow_html=True)

elif selected == "About Us":
    # Define the tabs
    tab1, tab2, tab3 = st.tabs(["About Us", "Project Description", "Team Members"])
    # Define the contents of each tab
    with tab1:
        st.header("About Us")
        st.write("Introducing our cutting-edge programming book recommendation system! Are you bored of searching through innumerable programming books in search of the best suit for your requirements? There is no need to look any further! Based on your preferences and interests, our recommendation engine use cutting-edge algorithms to select the most relevant and high-quality programming books.")
        st.write("Our technology evaluates your prior book selections, as well as your intended programming languages and areas of specialization, in a matter of seconds to present you with unique recommendations that are tailored directly to you. Whether you're a newbie hoping to learn the fundamentals or an experienced developer looking for advanced information, our system has you covered.")
        st.write("Our extensive dataset of programming books includes volumes from all major publishers as well as unique publications that are difficult to locate elsewhere. You can trust that the books recommended by our system are of the best quality and relevance, guaranteeing that your time is well spent.")
        st.write("So, what are you holding out for? Try out our programming book suggestion system today to boost your coding skills!")
        
    with tab3:
        st.header("Team Members")
        team_members = [
            {"name": "Aboy, Geian", "info": "Software Engineer with expertise in Python and web development."},
            {"name": "Lagan, Jefferson", "info": "Full-stack developer with experience in JavaScript and React."},
            {"name": "Lagazo, Jonah Levi", "info": "Data scientist with skills in machine learning and data analysis."},
            {"name": "Manalo, Mark Christianiel", "info": "Front-end developer specializing in HTML, CSS, and UI design."},
            {"name": "Monroyo, John Andrei", "info": "Backend developer proficient in Java and database management."},
        ]
        
        for member in team_members:
            expander = st.expander(member["name"])
            expander.write(member["info"])

    with tab2:
        st.header("Project Description")
        st.write("The Book Recommendation System for Programmers is a web application designed to help programmers find books that are relevant to their interests. The system uses a content-based filtering algorithm to recommend books based on user interest.")
        st.write("The system is built using the Python programming language and several libraries such as Streamlit, Pandas, NumPy, and Pillow. The data used in the system is stored in a CSV file, and the similarity matrix is computed using a pre-trained model in a pickle file.")
        st.write("The main menu of the system includes four options: Home, Book List, About Us, and Contact. The Home page allows users to select a book from a dropdown list and click on a 'Recommend me' button to get a list of recommended books. The Book List page displays a list of CSV files that can be selected to show their contents. The About Us page provides information about the team members and the project description. Finally, the Contact page allows users to send messages to the team.")
        st.write("The Home page also includes a sidebar menu with icons that represent each option. The Book List page has a button that allows users to show the contents of the selected CSV file. The About Us page uses tabs to display different information such as the team members, project description. The Contact page uses a form that allows users to enter their name, email, and message.")
        st.write("The web application is styled using a CSS file that includes custom styles to improve the user interface. A custom library called streamlit_option_menu is also used to create the dropdown menus in the system.")
        st.write("Overall, the Book Recommendation System for Programmers is a useful tool for programmers who are looking for books that are relevant to their interests. The system is easy to use and provides recommendations based on user preferences.")

elif selected == "Contact":
    st.header("Get in touch with Us")
    st.write("Please use the form below to send us a message:")
    contact_form = """
    <form action="https://formsubmit.co/bastonedproject@gmail.com" 
          method="POST">
         <input type="hidden" name="_captcha" value="false">     
         <input type="text" name="name" placeholder="Your Name" required>
         <input type="email" name="email" placeholder="Your email" required>
         <textarea name="message" placeholder="Your message here"></textarea>
           <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)









#CSS
def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</stle>", unsafe_allow_html=True)

local_css("style/style.css")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 