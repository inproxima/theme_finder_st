import textwrap
import openai
import streamlit as st
import streamlit_ext as ste


def get_summary( prompt, text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.0,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text

def get_ideas(prompt, output):
        # Use OpenAI's GPT-3 model to generate a summary of the text
        themes = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_ideas,
            max_tokens=300,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return themes.choices[0].text
def get_themes(prompt, output):
        # Use OpenAI's GPT-3 model to generate a summary of the text
        themes = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_themes,
            max_tokens=300,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return themes.choices[0].text


#strealit frontend
st.title("AI Theme Finder")
st.markdown("""---""") 
st.subheader("1. Please Enter you OpenAI API key")
url = "https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key"
api = st.text_input("If you don't know your OpenAI API key click [here](%s)." % url, type="password", placeholder="Your API Key")
st.markdown("""---""")
st.subheader("2. Please input the required information:")
themes =st.slider("How many main ideas/themes are you hoping to find?", min_value=3, max_value=10)
docx_file = st.text_area("Paste your input here.👇")

# Check Openai Key
if st.button("Find!"):
    openai.api_key = api
    try:
        # Send a test request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="What is the capital of France?",
            temperature=0.5
    )
        st.markdown("""---""")
        st.success("API key is valid!")
    
    except Exception as e:
        st.error("API key is invalid: {}".format(e))
    
    #AI computation backend
    if docx_file is not None:
        with st.spinner("Rhyme and reason, tech divine, AI theme finder, now be mine!"):
            output = ''
            chunks = textwrap.wrap(docx_file, 6000)
            result = ''
            for chunk in chunks:
                prompt1 = (f"Write a detailed summary of the following TEXT. TEXT:\n{chunk}\n")
                summary_large = get_summary(prompt1, chunk)
                result = result + ' ' + summary_large
            output = output + result
            prompt_ideas = (f"List the {themes} main ideas presented in the DATA, highlighting the central arguments, and supporting evidence. DATA: {output}")
            output_ideas = get_ideas(prompt_ideas, output)
            st.write(output_ideas)
            ste.download_button('Download ideas', output_ideas, "main_ideas.txt")
            st.markdown("""---""")
            prompt_themes = (f"Analyze the DATA identify {themes} recurring themes and patterns that could be used to categorize and describe the DATA. DATA: {output}")
            output_themes = get_themes(prompt_themes, output)
            st.write(output_themes)
            ste.download_button('Download themes', output_themes, "themes.txt")
        

                






