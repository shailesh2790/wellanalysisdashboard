import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def clean_column_values(df):
    # Iterate over each column and replace special characters in values
    for col in df.columns:
        if df[col].dtype == 'object':
            # Assuming we want to replace commas and other special characters with an empty string
            df[col] = df[col].str.replace('[^a-zA-Z0-9\s]', '', regex=True)
    return df

def parse_file(uploaded_file):
    if uploaded_file.name.endswith('.xlsx'):
        # Use pandas to read Excel files
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        # Use pandas to read CSV files, handling commas in values
        df = pd.read_csv(uploaded_file, thousands=',')
    else:
        st.error('Unsupported file type')
        return None

    # Clean the column values
    return clean_column_values(df)

# Rest of your Streamlit code

st.title('Well Analysis')
st.set_option('deprecation.showPyplotGlobalUse', False)
# File uploader
uploaded_file = st.file_uploader('Upload your document', type=['xlsx', 'csv', 'pdf', 'docx'])

if uploaded_file:
    # Assuming a function 'parse_file' that will parse the uploaded file and return a DataFrame
    df = parse_file(uploaded_file)

    if df is not None:
        st.write(df)

        # Allow the user to select multiple variables for analysis
        selected_columns = st.multiselect('Select variables to analyze', df.columns)

        if len(selected_columns) > 1:
            # Pairplot
            if st.checkbox('Show Pairplot'):
                st.write(sns.pairplot(df[selected_columns]))
                st.pyplot()

            # Heatmap
            if st.checkbox('Show Heatmap'):
                corr = df[selected_columns].corr()
                st.write(sns.heatmap(corr, annot=True))
                st.pyplot()

            # Line plot for time series
            if 'time' in df.columns and st.checkbox('Show Time Series Plot'):
                time_series_col = st.selectbox('Select the time variable', df.columns)
                for col in selected_columns:
                    if col != time_series_col:
                        plt.figure(figsize=(10, 5))
                        sns.lineplot(data=df, x=time_series_col, y=col)
                        plt.xticks(rotation=45)
                        st.pyplot()

            # Histograms
            if st.checkbox('Show Histograms'):
                for col in selected_columns:
                    st.write(df[col].plot(kind='hist', title=f'Histogram of {col}'))
                    st.pyplot()

            # Scatter plots with options for hue and size
            if len(selected_columns) >= 3 and st.checkbox('Show Scatter Plot with Hue and Size options'):
                hue_col = st.selectbox('Select the variable for color (hue)', selected_columns, index=0)
                size_col = st.selectbox('Select the variable for size', selected_columns, index=1)
                plt.figure(figsize=(10, 5))
                sns.scatterplot(data=df, x=selected_columns[0], y=selected_columns[1], hue=hue_col, size=size_col)
                st.pyplot()


    # ... the rest of your code for visualization
