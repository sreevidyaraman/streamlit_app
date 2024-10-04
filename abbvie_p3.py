import streamlit as st
import pandas as pd
import io
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode
# Set the page layout to wide
st.set_page_config(layout="wide")

import pandas as pd
import re
 
from openai import AzureOpenAI

def initialize_llm() :
    gpt_35_config = {
        "api_base":"https://gai-sl-openai.openai.azure.com/",
        "deployment_name": "gai-sl-openai",    
        "openai_api_key": "b62ebb8214074646b3195315b0ae0f25",
        "api_version": "2024-02-15-preview",
        "temperature": 0
    }
    
    opeanai_api_base = gpt_35_config["api_base"]
    api_version =gpt_35_config["api_version"]
    openai_key = gpt_35_config["openai_api_key"]
    azure_deployment=gpt_35_config["deployment_name"]
    
    llm = AzureOpenAI(
        azure_endpoint=opeanai_api_base,
        api_key=openai_key,
        api_version=api_version,
        azure_deployment=azure_deployment
    )
    return llm

def create_json(df):
    json_dynamic = {}

    for _, row in df.iterrows():
        user_story = row['User Story']

        if user_story not in json_dynamic:
            # Create empty lists for all columns except 'User Story'
            json_dynamic[user_story] = {col: [] for col in df.columns if col != 'User Story'}

        # Append non-empty values to the respective lists
        for col in df.columns:
            if col != 'User Story' and not pd.isna(row[col]):            
                json_dynamic[user_story][col].append(row[col])
    return json_dynamic


def generate_questions_hcp_happy(question_generation_context,kpi_metrics,dimensions,llm,num_of_questions=5):
    Question_Generation_Prompt_Template = """
                                        You are an expert question generator. 
                                        Use the given {question_generation_context}. 
                                        Generate a list of questions that can help you analyze these {dimensions} by {kpi_metrics}.
                                        
                                        ###
                                        There are three inputs:

                                        1. Number of questions that needs to be generated.
                                        2. The User story context to generate questions.
                                        3. The Dimensions and KPI Metrics on which questions needs to be generated.

                                        ###
                                        one output:
                                        Generated questions which is list of generated questions.
                                        Strictly follow the below guideline for the generated questions:
                                        * The list of generated question should be strictly enclosed between ``` and ```.
                                        * You need to include all the dimensions along with one key metrics while generating questions.
                                        * The number of questions to be generated should be strictly equal to the provided number of questions.
                                        * The generated question should have different variants of question without changing the context of it.

                                        NUMBER OF QUESTIONS :
                                        {num_of_questions} 
                                        
                                        GENERATED QUESTIONS:
                                        """.format(num_of_questions=num_of_questions,
                                                   question_generation_context=question_generation_context,
                                                   dimensions=dimensions,
                                                   kpi_metrics=kpi_metrics
                                                   )
    qg_message = [{"role":"system","content":Question_Generation_Prompt_Template}]
    message = llm.chat.completions.create(messages = qg_message,temperature=0,model = "5K-gpt-35-turbo")
    generated_questions = message.choices[0].message.content
    pattern = r'\d+\.\s+'
    list_of_generated_questions = re.split(pattern, generated_questions)[1:]
    list_of_generated_questions = list(map(lambda x: x.strip(),list_of_generated_questions))
    return(list_of_generated_questions)

def generate_questions_hcp_multirequest(question_generation_context,kpi_metrics,dimensions,llm,num_of_questions=15):
    Question_Generation_Prompt_Template = """
                                        You are an expert question generator. 
                                        Use the given {question_generation_context}. 
                                        Generate a list of questions that can help you analyze these {dimensions} by {kpi_metrics}.
                                        
                                        ###
                                        There are three inputs:

                                        1. Number of questions that needs to be generated.
                                        2. The User story context to generate questions.
                                        3. The Dimensions and KPI Metrics on which questions needs to be generated.

                                        ###
                                        one output:
                                        Generated questions which is list of generated questions.
                                        Strictly follow the below guideline for the generated questions:
                                        * The list of generated question should be strictly enclosed between ``` and ```.
                                        * You need to include all the dimensions along with key metrics while generating questions.
                                        * You need to use multiple dimension values in the question with multiple key metrics.
                                        * The number of questions to be generated should be strictly equal to the provided number of questions.
                                        * The generated question should have different variants of question without changing the context of it.

                                        NUMBER OF QUESTIONS :
                                        {num_of_questions} 
                                        
                                        GENERATED QUESTIONS:
                                        """.format(num_of_questions=num_of_questions,
                                                   question_generation_context=question_generation_context,
                                                   dimensions=dimensions,
                                                   kpi_metrics=kpi_metrics
                                                   )
    qg_message = [{"role":"system","content":Question_Generation_Prompt_Template}]
    message = llm.chat.completions.create(messages = qg_message,temperature=0,model = "5K-gpt-35-turbo")
    generated_questions = message.choices[0].message.content
    pattern = r'\d+\.\s+'
    list_of_generated_questions = re.split(pattern, generated_questions)[1:]
    list_of_generated_questions = list(map(lambda x: x.strip(),list_of_generated_questions))
    return(list_of_generated_questions)

# Display your styled banners (as in your original code)
st.markdown("""
    <style>
    .blue-banner {
        background-color: #002147;
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }

    .grey-banner {
        background-color: #F5F5F5; /* Light Grey color */
        display: flex; /* Enable flexbox */
        justify-content: left; /* Left align text */
        align-items: center; /* Center align items vertically */
        padding: 0px; /* Padding for spacing */
        width: 100%; /* Full width */
        height: 40px;
        margin-bottom: 5px; /* Remove bottom margin */
    }  

    h1 {
        margin: 0; /* Remove default margin from heading */
        font-size: 18px; /* Reduce font size for less height */
        line-height: 0; /* Set line height to 1 to minimize vertical space */
        color: white; /* White text color */
    }

    .sub-workstream-label {
        font-size: 16px;
        font-weight: normal; /* Remove bold weight */
        margin-bottom: 5px; /* Space below label */
        margin-right: 5px; /* Space between label and icon */
        display: inline-block; /* Allow label and icon to align in the same row */
    }

    .workstream-section {
        margin-bottom: 0; /* Remove bottom margin */
        display: flex; /* Use flexbox for alignment */
        align-items: center; /* Center align items vertically */
    }

    .workstream-input {
        width: 200px; /* Width of the input box */
    }

    .info-icon {
        color: white; /* Color of the text inside the circle */
        font-size: 12px; /* Font size of the info icon */
        background-color: gray; /* Background color of the circle */
        border-radius: 50%; /* Make it circular */
        width: 15px; /* Width of the circle */
        height: 15px; /* Height of the circle */
        display: flex; /* Use flexbox for centering */
        align-items: center; /* Center align text vertically */
        justify-content: center; /* Center align text horizontally */
        cursor: pointer; /* Change cursor to pointer on hover */
        margin-left: 5px; /* Space between label and icon */
        margin-top: -5px; /* Move icon slightly up */
    }

    .info-icon:hover {
        background-color: #555; /* Darker gray on hover */
    }

    </style>

    <div class="blue-banner">
        <h1>BTS Orchestrator | Testing Product</h1>
    </div>
            
    <div class="grey-banner">
        <span style="padding-left: 10px; color: #0089FD; font-weight: bold;">Admin</span> <!-- Added padding before Admin -->
        <span style="color: #FF9300; font-weight: bold; margin-left: 10px; margin-right: 10px;"> > </span> <!-- Orange color for ">" symbol -->
        <span style="color: black; font-weight: bold;">Testing Product</span> <!-- Black color for "Testing Product" -->
    </div>


""", unsafe_allow_html=True)

# Add space between "Title", "Sub Workstream", and "Specify the Number of User Stories"
st.markdown("<br><br>", unsafe_allow_html=True)  # Two lines space

# Page navigation logic
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'User_Stories'

def user_story():
    # Input field for the user to specify the number of rows
    sub_workstream = st.text_input("Enter Sub Workstream", value="", key="sub_workstream_input")
    num_rows = st.number_input("Specify the Number of User Stories:", min_value=0, value=0)

    if num_rows > 0:
        st.session_state.df = create_dataframe_with_serial_numbers(num_rows)

    # Configure the editable grid options
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    gb.configure_default_column(editable=True)

    # Adjust column widths and alignments
    gb.configure_column("Serial Number", width=70, headerStyle={"fontWeight": "bold", "textAlign": "center"},
                        cellStyle={"textAlign": "center"})
    gb.configure_column("User Story", width=400, headerStyle={"fontWeight": "bold", "textAlign": "center"},
                        cellStyle={"textAlign": "left"})
    gb.configure_column("Priority", width=100, headerStyle={"fontWeight": "bold", "textAlign": "center"},
                        cellStyle={"textAlign": "center"})

    grid_options = gb.build()

    if not st.session_state.df.empty:
        st.write("### User Persona and Priority Overview")
        response = AgGrid(
            st.session_state.df,
            gridOptions=grid_options,
            editable=True,
            fit_columns_on_grid_load=True,
            theme="streamlit",
            key='data_grid'
        )

        if response['data'] is not None:
            st.session_state.df = pd.DataFrame(response['data'])

    # Button to navigate to the next page
    if st.button("Submit"):
        st.session_state.df = st.session_state.df
        st.session_state.current_page = 'doc_upload'
        st.experimental_rerun()

def doc_upload():
    container=st.container()
    with container:
        col=st.columns(2)
        with col[0]:
            # File uploader for the first file
            uploaded_file_1 = st.file_uploader("Upload the Sample question file", type=['csv', 'xlsx'])

            uploaded_file_2 = st.file_uploader(f"Upload the minimum required parameter file for generating question", type=['csv', 'xlsx'])
            # Dropdown for selecting the second upload option
            option = st.selectbox(
                "Choose a Agent for question generation",
                ["Select an option", "Text2API", "Text2SQL", "Text2Doc"]
            )


            # Function to read the uploaded file
            def read_file(file):
                if file.name.endswith('.csv'):
                    return pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    return pd.read_excel(file)

            # Display contents of the first file if uploaded
            if uploaded_file_1 is not None:
                st.write("File Content:")
                df1 = read_file(uploaded_file_1)
                st.session_state.sample_qn=df1
                # st.dataframe(df1)
            if uploaded_file_2 is not None:
                st.write("File Content:")
                df2 = read_file(uploaded_file_2)
                st.session_state.minimum_param=df2

            # Based on the dropdown option, show the second file uploader
            if option == "Text2API":
                api_container=st.container()
                with api_container:
                    api_col=st.columns(2)
                    with api_col[0]:
                        st.text_input("Please provide Module Id")
                        st.text_input("Please provide sample column values")
                    with api_col[1]:
                        st.text_input("Please provide schema information")
                        st.text_input("Please provide column description")

            elif option == "Text2Doc":
                uploaded_file_3 = st.file_uploader(f"Upload the document for {option} to generate the questions", type=['pdf'])
                if uploaded_file_3 is not None:
                    st.write(f"upload successful for {option}")
            elif option == "Text2SQL":
                st.text_input("Please provide schema information")

            # Submit button to move to the next page
            if st.button("Proceed"):
                st.session_state.current_page = 'Testcase_design'  # Navigate to the submitted page
                st.experimental_rerun()
        with col[1]:
            st.write("Sample format to upload")
            df_question_sample=pd.read_excel(r"C:\Users\SaranKirthicS\OneDrive - TheMathCompany Private Limited\Desktop\pdf_capstone\pdf_bot\abbvie_files\sample question to upload.xlsx")
            df_min_required_metric=pd.read_excel(r"C:\Users\SaranKirthicS\OneDrive - TheMathCompany Private Limited\Desktop\pdf_capstone\pdf_bot\abbvie_files\minimum required parameter.xlsx")
            @st.cache_data
            def convert_df_to_excel(df):
                output = io.BytesIO()
                # Use ExcelWriter to write the DataFrame to a BytesIO object
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                processed_data = output.getvalue()
                return processed_data

            que_excel_data = convert_df_to_excel(df_question_sample)
            req_excel_data= convert_df_to_excel(df_min_required_metric)
            
            download_bt_container=st.container()
            with download_bt_container:
                download_bt_col=st.columns(2)
                with download_bt_col[0]:
                    st.download_button(label="sample question template",
                                        data=que_excel_data,
                                        file_name='sample_question_template.xlsx',
                                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                with download_bt_col[1]:
                    st.download_button(label="Minimum required parameter file template",
                                        data=req_excel_data,
                                        file_name='Minimum required parameter template.xlsx',
                                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# User Stories Page
if st.session_state.current_page == 'User_Stories':
    # Function to create an empty DataFrame with a specified number of rows
    def create_dataframe_with_serial_numbers(num_rows):
        serial_numbers = [i + 1 for i in range(num_rows)]
        return pd.DataFrame({'Serial Number': serial_numbers, 'User Story': [''] * num_rows, 'Priority': [''] * num_rows})

    # Initialize the session state for the DataFrame if it doesn't exist
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=['Serial Number', 'User Story'])
    
    user_story()
    
if st.session_state.current_page == 'doc_upload':
    doc_upload()

def test_case():
    st.write("HCP1")  # Update with actual value as needed

    # Initialize the new DataFrame with additional columns
    df_testcase = st.session_state.df.copy()
    # df_testcase=st.session_state.minimum_param
    happiness_columns = ['Happy', 'Happy-Multirequest', 'Happy-Nudging', 'Unhappy', 'Unhappy-Multirequest', 'Unhappy-Not Authorized', 'Unhappy-Out of Scope']
    
    # Create additional columns initialized to 0
    for col in happiness_columns:
        df_testcase[col] = 0
    
    # Define a function to calculate totals
    def calculate_total(row):
        return sum(row[happiness_columns])

    # Calculate initial totals for the new DataFrame
    df_testcase['Total'] = df_testcase.apply(calculate_total, axis=1)

    # Configure the grid for Testcase Design
    gb_testcase = GridOptionsBuilder.from_dataframe(df_testcase)
    gb_testcase.configure_column("Serial Number", width=70, headerStyle={"fontWeight": "bold", "textAlign": "center"}, cellStyle={"textAlign": "center"})
    gb_testcase.configure_column("User Story", width=400, headerStyle={"fontWeight": "bold", "textAlign": "center"}, cellStyle={"textAlign": "left"})
    gb_testcase.configure_column("Priority", width=100, headerStyle={"fontWeight": "bold", "textAlign": "center"}, cellStyle={"textAlign": "center"})

    # Additional happiness columns
    for col in happiness_columns:
        gb_testcase.configure_column(col, width=100, headerStyle={"fontWeight": "bold", "textAlign": "center"}, cellStyle={"textAlign": "center", "minWidth": 60}, editable=True)

    # Final Total Column
    gb_testcase.configure_column("Total", width=100, headerStyle={"fontWeight": "bold", "textAlign": "center"}, cellStyle={"textAlign": "center", "minWidth": 60})

    grid_options_testcase = gb_testcase.build()

    # Display the Testcase Design table
    st.write("### Test Case Design Table")
    response_testcase = AgGrid(
        df_testcase,
        gridOptions=grid_options_testcase,
        editable=True,
        fit_columns_on_grid_load=True,
        theme="streamlit",
        key='data_grid_testcase'
    )

    # Update DataFrame with the new data and recalculate totals
    if response_testcase['data'] is not None:
        
        df_testcase_updated = pd.DataFrame(response_testcase['data'])
        # Recalculate totals after editing
        df_testcase_updated['Total'] = df_testcase_updated.apply(calculate_total, axis=1)
        st.session_state.df_testcase = df_testcase_updated

    if st.button("Generate Questions"):
        st.session_state.current_page = 'Generated_Qns'  # Navigate to the submitted page
        st.experimental_rerun()
   
def generate_qns():
    df=st.session_state.minimum_param
    results=[]
    json_dynamic=create_json(df)
    for user_story, data in json_dynamic.items():
        kpi_metrics=[]
        dimensions={}
        question_generation_context=user_story
        for i,j in data.items():
            if i =='KPI':
                kpi_metrics=j
            else:
                dimensions[i]=j
        num_ques_df=st.session_state.df_testcase 
        llm=initialize_llm()

        happy=int(num_ques_df[num_ques_df['User Story']==user_story]['Happy'].iloc[0])
        happy_df=pd.DataFrame()
        if happy:
            
            y=generate_questions_hcp_happy(question_generation_context,kpi_metrics,dimensions,llm,happy)
            for q in y:
                results.append([user_story,'Happy',q])
            # happy_df=pd.DataFrame(results,columns=['User story','question type','questions'])

        happy_multi=int(num_ques_df[num_ques_df['User Story']==user_story]['Happy-Multirequest'].iloc[0])
        happy_multi_df=pd.DataFrame()
        if happy_multi:
           
            y=generate_questions_hcp_multirequest(question_generation_context,kpi_metrics,dimensions,llm,happy_multi)
            for q in y:
                results.append([user_story,'Happy-Multirequest',q])
        
            
                
    results_df=pd.DataFrame(results,columns=['User story','question type','questions'])
    results_df.drop_duplicates(inplace=True)
    st.write(results_df)
    


# Testcase Design Page
if st.session_state.current_page == 'Testcase_design':
    test_case()


if st.session_state.current_page == 'Generated_Qns':
    generate_qns()

