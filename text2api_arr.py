<<<<<<< HEAD
import streamlit as st
import pandas as pd

credentials = {
    "admin": {"username": "admin", "password": "admin"},
}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Initialize the first page

st.markdown(
    """
    <style>
    .stApp {
        background-color: #002147; /* Change this to the desired color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def login_page():
    # st.set_page_config(page_title="Image Positioning Example")
    # st.markdown(
    # f"""
    # <style>
    # .custom-image {{
    #     position: absolute;
    #     top: 300;  /* Adjust the top position */
    #     left: 300; /* Adjust the left position */
    #     width: 300; /* Set the desired width */
    #     height: auto; /* Keep aspect ratio */
    # }}
    # </style>
    # """,
    # unsafe_allow_html=True
    # )
    # image_path=r"C:\Users\ArribalajiM\TheMathCompany Private Limited\AbbVie - 29. GenAIsys Testing\04. Product\Question Generation & Extrapolation\Codes\AbbVieLogo_white.png"
    # Add the image with a custom class
    # st.markdown(f'<img class="custom-image" src="{image_path}">', unsafe_allow_html=True)
    # st.markdown(f'<img class="custom-image" src="data:image/png;base64,{st.image(image_path, use_column_width=False).to_bytes().decode()}">', unsafe_allow_html=True)
    # Create a container for the login form
    with st.container():
        # Display the bot name and description
        st.markdown("<h1 style='text-align: center; font-family: Roboto, sans-serif;'>Abbvie Testing Product</h1>",
                    unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic; font-family: Roboto, sans-serif;'>Testing Companion</p>",
                    unsafe_allow_html=True)

        # Input field for username
        username_or_email = st.text_input("Username", placeholder="Enter your username")

        # Password input
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        # Container for links
        link_container = st.container()
        with link_container:
            # Forgot Credentials link (open in new page)
            if st.button("Forgot Credentials?"):
                st.session_state.page = "forgot"

            # About Us button
            if st.button("About Us", key="about_us_btn"):
                st.session_state.page = "about_us"

        login_button = st.button("Login")

    if login_button:
        if username_or_email in credentials:
            user_data = credentials[username_or_email]
            if user_data["password"] == password:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = user_data["username"]  # Set the username in session state
                st.session_state.page = 'upload'  # Navigate to upload page
            else:
                st.error("Invalid password.")
        else:
            st.error("Invalid username/email.")

def doc_upload():


    st.image(r"C:\Users\SreevidyaRaman\TheMathCompany Private Limited\AbbVie - 29. GenAIsys Testing\04. Product\Question Generation & Extrapolation\Codes\AbbVieLogo_white.png", use_column_width=True)
    st.markdown(
        """
        <h1 style='text-align: center;'>Testing Product</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <h2 style='text-align: left;'>Question and Answer Generation</h2>
        """,
        unsafe_allow_html=True)
    st.write("")

    st.header("Please Upload the Excel or CSV file")

    # File uploader for the first file
    uploaded_file_1 = st.file_uploader("Upload the Sample question file", type=['csv', 'xlsx'])

    # File uploader for the second file
    uploaded_file_2 = st.file_uploader("Upload the minimum required parameter file", type=['csv', 'xlsx'])

    # Function to read the uploaded file
    def read_file(file):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)

    # Display contents of the first file if uploaded
    if uploaded_file_1 is not None:
        st.write("First File Content:")
        df1 = read_file(uploaded_file_1)
        st.dataframe(df1)

    # Display contents of the second file if uploaded
    if uploaded_file_2 is not None:
        st.write("Second File Content:")
        df2 = read_file(uploaded_file_2)
        st.dataframe(df2)
    
    if st.button("Submit"):
        st.session_state.page = 'submitted'  # Navigate to the submitted page

def parameter_input():
    # st.set_page_config(page_title="Table Input Example")

    # Define the number of rows for the table
    num_rows = st.number_input("Number of rows:", min_value=1, max_value=20, value=5)
    columns = ['User Story', 'Priority', 'Number of Valid question','Number of Invalid question','Number of Typo error question']

    # Display a table-like layout for user input
    st.write("### Enter Data in the Table Below:")

    # Create a dictionary to hold the input data
    data = {col: [] for col in columns}

    # Create table headers
    header_cols = st.columns(len(columns))
    for col, header in zip(header_cols, columns):
        col.write(f"**{header}**")

    # Iterate over the number of rows
    for i in range(num_rows):
        row = st.columns(len(columns))
        
        # Collect input for each cell in the table-like format
        user_story = row[0].text_input(f"User Story {i+1}", key=f"user_story_{i}")
        priority = row[1].text_input("Priority", key=f"priority_{i}")
        
        # email = row[2].text_input(f"Email {i+1}", key=f"email_{i}")
        no_valid_que=row[2].number_input("# Valid question", min_value=0, max_value=120, key=f"no_of_valid_question{i}")
        no_invalid_que=row[3].number_input("# Invalid question", min_value=0, max_value=120, key=f"no_of_invalid_question{i}")
        no_typo_que=row[4].number_input("# Typo error question", min_value=0, max_value=120, key=f"no_of_typo_question{i}")
        
        # Append the data to the dictionary
        data['User Story'].append(user_story)
        data['Priority'].append(priority)
        data['Number of Valid question'].append(no_valid_que)
        data['Number of Invalid question'].append(no_invalid_que)
        data['Number of Typo error question'].append(no_typo_que)


    # When the user clicks "Submit", display the collected data as a DataFrame
    if st.button('Submit'):
        df = pd.DataFrame(data)
        st.write("### Collected Data:")
        df['Total_question']=df['Number of Valid question']+df['Number of Invalid question']+df['Number of Typo error question']
        st.dataframe(df)
    if st.button("Logout"):
        st.session_state.logged_in = False  # Update the logged_in state
        st.session_state.page = 'login'
        

# Main app logic
if st.session_state.logged_in:
    if st.session_state.page == 'upload':
        doc_upload()
    elif st.session_state.page == 'submitted':
        parameter_input()
elif st.session_state.page=='login':
    login_page()
=======
import streamlit as st
import pandas as pd

credentials = {
    "admin": {"username": "admin", "password": "admin"},
}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Initialize the first page

st.markdown(
    """
    <style>
    .stApp {
        background-color: #002147; /* Change this to the desired color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def login_page():
    # st.set_page_config(page_title="Image Positioning Example")
    # st.markdown(
    # f"""
    # <style>
    # .custom-image {{
    #     position: absolute;
    #     top: 300;  /* Adjust the top position */
    #     left: 300; /* Adjust the left position */
    #     width: 300; /* Set the desired width */
    #     height: auto; /* Keep aspect ratio */
    # }}
    # </style>
    # """,
    # unsafe_allow_html=True
    # )
    # image_path=r"C:\Users\ArribalajiM\TheMathCompany Private Limited\AbbVie - 29. GenAIsys Testing\04. Product\Question Generation & Extrapolation\Codes\AbbVieLogo_white.png"
    # Add the image with a custom class
    # st.markdown(f'<img class="custom-image" src="{image_path}">', unsafe_allow_html=True)
    # st.markdown(f'<img class="custom-image" src="data:image/png;base64,{st.image(image_path, use_column_width=False).to_bytes().decode()}">', unsafe_allow_html=True)
    # Create a container for the login form
    with st.container():
        # Display the bot name and description
        st.markdown("<h1 style='text-align: center; font-family: Roboto, sans-serif;'>Abbvie Testing Product</h1>",
                    unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic; font-family: Roboto, sans-serif;'>Testing Companion</p>",
                    unsafe_allow_html=True)

        # Input field for username
        username_or_email = st.text_input("Username", placeholder="Enter your username")

        # Password input
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        # Container for links
        link_container = st.container()
        with link_container:
            # Forgot Credentials link (open in new page)
            if st.button("Forgot Credentials?"):
                st.session_state.page = "forgot"

            # About Us button
            if st.button("About Us", key="about_us_btn"):
                st.session_state.page = "about_us"

        login_button = st.button("Login")

    if login_button:
        if username_or_email in credentials:
            user_data = credentials[username_or_email]
            if user_data["password"] == password:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = user_data["username"]  # Set the username in session state
                st.session_state.page = 'upload'  # Navigate to upload page
            else:
                st.error("Invalid password.")
        else:
            st.error("Invalid username/email.")

def doc_upload():


    st.image(r"C:\Users\ArribalajiM\TheMathCompany Private Limited\AbbVie - 29. GenAIsys Testing\04. Product\Question Generation & Extrapolation\Codes\AbbVieLogo_white.png", use_column_width=True)
    st.markdown(
        """
        <h1 style='text-align: center;'>Testing Product</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <h2 style='text-align: left;'>Question and Answer Generation</h2>
        """,
        unsafe_allow_html=True)
    st.write("")

    st.header("Please Upload the Excel or CSV file")

    # File uploader for the first file
    uploaded_file_1 = st.file_uploader("Upload the Sample question file", type=['csv', 'xlsx'])

    # File uploader for the second file
    uploaded_file_2 = st.file_uploader("Upload the minimum required parameter file", type=['csv', 'xlsx'])

    # Function to read the uploaded file
    def read_file(file):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)

    # Display contents of the first file if uploaded
    if uploaded_file_1 is not None:
        st.write("First File Content:")
        df1 = read_file(uploaded_file_1)
        st.dataframe(df1)

    # Display contents of the second file if uploaded
    if uploaded_file_2 is not None:
        st.write("Second File Content:")
        df2 = read_file(uploaded_file_2)
        st.dataframe(df2)
    
    if st.button("Submit"):
        st.session_state.page = 'submitted'  # Navigate to the submitted page

def parameter_input():
    # st.set_page_config(page_title="Table Input Example")

    # Define the number of rows for the table
    num_rows = st.number_input("Number of rows:", min_value=1, max_value=20, value=5)
    columns = ['User Story', 'Priority', 'Number of Valid question','Number of Invalid question','Number of Typo error question']

    # Display a table-like layout for user input
    st.write("### Enter Data in the Table Below:")

    # Create a dictionary to hold the input data
    data = {col: [] for col in columns}

    # Create table headers
    header_cols = st.columns(len(columns))
    for col, header in zip(header_cols, columns):
        col.write(f"**{header}**")

    # Iterate over the number of rows
    for i in range(num_rows):
        row = st.columns(len(columns))
        
        # Collect input for each cell in the table-like format
        user_story = row[0].text_input(f"User Story {i+1}", key=f"user_story_{i}")
        priority = row[1].text_input("Priority", key=f"priority_{i}")
        
        # email = row[2].text_input(f"Email {i+1}", key=f"email_{i}")
        no_valid_que=row[2].number_input("# Valid question", min_value=0, max_value=120, key=f"no_of_valid_question{i}")
        no_invalid_que=row[3].number_input("# Invalid question", min_value=0, max_value=120, key=f"no_of_invalid_question{i}")
        no_typo_que=row[4].number_input("# Typo error question", min_value=0, max_value=120, key=f"no_of_typo_question{i}")
        
        # Append the data to the dictionary
        data['User Story'].append(user_story)
        data['Priority'].append(priority)
        data['Number of Valid question'].append(no_valid_que)
        data['Number of Invalid question'].append(no_invalid_que)
        data['Number of Typo error question'].append(no_typo_que)


    # When the user clicks "Submit", display the collected data as a DataFrame
    if st.button('Submit'):
        df = pd.DataFrame(data)
        st.write("### Collected Data:")
        df['Total_question']=df['Number of Valid question']+df['Number of Invalid question']+df['Number of Typo error question']
        st.dataframe(df)
    if st.button("Logout"):
        st.session_state.logged_in = False  # Update the logged_in state
        st.session_state.page = 'login'
        

# Main app logic
if st.session_state.logged_in:
    if st.session_state.page == 'upload':
        doc_upload()
    elif st.session_state.page == 'submitted':
        parameter_input()
elif st.session_state.page=='login':
    login_page()
>>>>>>> c6dd4d0b0caf60b834f2380c969180273d08d561
