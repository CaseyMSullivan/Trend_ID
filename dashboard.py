import os
import streamlit as st
import pandas as pd
from modules.trend_pipeline import run_pipeline
from modules.gcp_loader import list_prefixes, load_documents_from_gcp

# Burt's Bees palette
COLOR_YELLOW = '#F4C32D'
COLOR_RED    = '#C51F25'
COLOR_DARK   = '#4A2C2A'
COLOR_OFFWHITE = '#FFF8E7'
COLOR_GOLD = '#DFAF2B'

st.set_page_config(page_title='Trend Sensing Dashboard', layout='wide')
# Sidebar
st.sidebar.title('Settings')
# OpenAI key
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ''
input_key = st.sidebar.text_input('OpenAI API Key', type='password')
if st.sidebar.button('Save OpenAI Key'):
    st.session_state.openai_key = input_key
if st.session_state.openai_key:
    import openai
    openai.api_key = st.session_state.openai_key
# GCP prefix selection
st.sidebar.subheader('GCP Loader')
BUCKET_NAME = 'trendid_data'
try:
    prefixes = list_prefixes(BUCKET_NAME)
    sel = st.sidebar.selectbox('Select folder (optional)', [''] + prefixes)
    prefix = sel
except Exception as e:
    st.sidebar.write(f'Could not list GCP prefixes: {e}')
    prefix = st.sidebar.text_input('Or enter a folder name (leave empty for root)')
# Load from GCP
if st.sidebar.button('Load from GCP'):
    with st.spinner('Loading docs from GCP ...'):
        docs_gcp = load_documents_from_gcp(BUCKET_NAME, prefix)
        st.session_state['docs_gcp'] = docs_gcp
        st.sidebar.success(f'Loaded {len(docs_gcp)} documents')
# Local docs loader
@st.cache_data
def load_local_docs(path='data/docs'):
    docs = {}
    if os.path.isdir(path):
        for fname in sorted(os.listdir(path)):
            if fname.lower().endswith('.txt'):
                with open(os.path.join(path, fname), 'r') as f:
                    docs[fname] = f.read()
    return docs
local_docs = load_local_docs()
gcp_docs = st.session_state.get('docs_gcp', {})
docs = {**local_docs, **gcp_docs}
# Score
validated = run_pipeline(docs)
# Tabs
tabs = st.tabs(['Quarterly Snapshot', 'Trend Explorer', 'Trend Deep Dive', 'Source Simulation', 'Recommendations'])
# Snapshot
with tabs[0]:
    st.header('Quarterly Snapshot')
    c1, c2, c3 = st.columns(3)
    c1.metric('High Priority', len(validated.get('high', {})))
    c2.metric('Medium Priority', len(validated.get('medium', {})))
    c3.metric('Low Priority', len(validated.get('low', {})))
    st.markdown('---')
    st.subheader('High Priority')
    if validated.get('high'):
        for term in validated['high']:
            stats = validated['high'][term]['stats']
            reason = validated['high'][term]['reason']
            with st.expander(f'{term} (freq: {stats[0]}, breadth: {stats[1]}, momentum: {stats[2]})'):
                st.write('Reason:', reason)
                occ = []
                for fname, text in docs.items():
                    if term in text.lower():
                        occ.append(f'* {fname}')
                if occ:
                    st.write('Found in docs:')
                    for o in occ:
                        st.write(o)
                else:
                    st.write('No occurrences found in docs.')
    else:
        st.write('No high priority trends detected.')
    st.subheader('Medium Priority')
    if validated.get('medium'):
        for term in validated['medium']:
            stats = validated['medium'][term]['stats']
            reason = validated['medium'][term]['reason']
            with st.expander(f'{term} (freq: {stats[0]}, breadth: {stats[1]}, momentum: {stats[2]})'):
                st.write('Reason:', reason)
    else:
        st.write('No medium priority trends detected.')
    st.subheader('Low Priority')
    if validated.get('low'):
        for term in validated['low']:
            stats = validated['low'][term]['stats']
            reason = validated['low'][term]['reason']
            with st.expander(f'{term} (freq: {stats[0]}, breadth: {stats[1]}, momentum: {stats[2]})'):
                st.write('Reason:', reason)
    else:
        st.write('No low priority trends detected.')
    st.subheader('Fads')
    if validated.get('fads'):
        st.write(', '.join(validated['fads']))
    else:
        st.write('No fads detected.')
# Explorer
with tabs[1]:
    st.header('Trend Explorer')
    rows = []
    for cat in ['high','medium','low']:
        for term, info in validated.get(cat, {}).items():
            freq, breadth, momentum = info['stats']
            rows.append({'Term': term, 'Category': cat.title(), 'Frequency': freq, 'Breadth': breadth, 'Momentum': momentum, 'Reason': info['reason']})
    if rows:
        df = pd.DataFrame(rows)
        search = st.text_input('Search terms, ingredients, claims...')
        if search:
            df = df[df['Term'].str.contains(search, case=False) | df['Category'].str.contains(search, case=False) | df['Reason'].str.contains(search, case=False)]
        st.dataframe(df, use_container_width=True)
    else:
        st.write('No trends to explore.')
# Deep Dive
with tabs[2]:
    st.header('Trend Deep Dive')
    all_terms = list(validated.get('high', {}).keys()) + list(validated.get('medium', {}).keys()) + list(validated.get('low', {}).keys())
    term = st.selectbox('Select a trend', options=all_terms if all_terms else [''])
    if term:
        info = None
        for cat in ['high','medium','low']:
            if term in validated.get(cat, {}):
                info = validated[cat][term]
                break
        if info:
            st.subheader(f'{term}')
            st.write('Frequency:', info['stats'][0])
            st.write('Breadth:', info['stats'][1])
            st.write('Momentum:', info['stats'][2])
            st.write('Reason:', info['reason'])
            occ = []
            for fname, text in docs.items():
                if term in text.lower():
                    occ.append(f'* {fname}')
            if occ:
                st.write('Docs containing this term:')
                for x in occ:
                    st.write(x)
            else:
                st.write('No docs mention this term.')
        else:
            st.write('Term info unavailable.')
# Source Simulation
with tabs[3]:
    st.header('Source Simulation')
    st.write('This section is a placeholder. Connect data sources like Spate, Motivebase, etc., and implement their loading and visualization here.')
# Recommendations
with tabs[4]:
    st.header('Recommendations')
    st.write('This section is a placeholder. Implement recommendation logic, e.g. using OpenAI to generate innovation suggestions based on identified trends.')