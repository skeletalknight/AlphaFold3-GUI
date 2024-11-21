# visualization.py

import streamlit as st
from Bio import PDB
import py3Dmol
import io
import json
import numpy as np
import plotly.express as px
import pandas as pd
from loguru import logger

# Configure logger
logger.add("afusion_visualization.log", rotation="1 MB", level="DEBUG")

# ========================================
# Functions that accept file paths
# ========================================

def read_cif_file(file_path):
    parser = PDB.MMCIFParser(QUIET=True)
    with open(file_path, 'r') as file:
        content = file.read()
    file_like = io.StringIO(content)
    structure = parser.get_structure('protein', file_like)
    return structure, content

def extract_pae_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    pae = np.array(data.get("pae", []))
    return pae

def extract_summary_confidences(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# ========================================
# Functions that accept file objects (uploaded files)
# ========================================

def read_cif_file_obj(file_obj):
    parser = PDB.MMCIFParser(QUIET=True)
    content = file_obj.read().decode('utf-8')
    file_like = io.StringIO(content)
    structure = parser.get_structure('protein', file_like)
    return structure, content

def extract_pae_from_json_obj(file_obj):
    data = json.load(file_obj)
    pae = np.array(data.get("pae", []))
    return pae

def extract_summary_confidences_obj(file_obj):
    data = json.load(file_obj)
    return data

# ========================================
# Common functions
# ========================================

def extract_residue_bfactors(structure):
    residue_bfactors = {}
    ligands = []
    for model in structure:
        for chain in model:
            for residue in chain:
                hetfield = residue.get_id()[0]
                resseq = residue.get_id()[1]
                resname = residue.get_resname()
                chain_id = chain.id

                atom_bfactors = []

                for atom in residue:
                    bfactor = atom.get_bfactor()

                    if hetfield.strip() == "":
                        atom_bfactors.append(bfactor)
                    else:
                        # Ligand atoms
                        ligands.append({
                            'chain_id': chain_id,
                            'resseq': resseq,
                            'resname': resname,
                            'atom_name': atom.get_name(),
                            'bfactor': bfactor
                        })

                if hetfield.strip() == "" and atom_bfactors:
                    avg_bfactor = sum(atom_bfactors) / len(atom_bfactors)
                    residue_bfactors[(chain_id, resseq)] = {
                        'avg_bfactor': avg_bfactor,
                        'resname': resname
                    }

    return residue_bfactors, ligands

def get_color_from_bfactor(bfactor):
    # Define color mapping
    color_mapping = [
        {'range': [90, 100], 'color': '#106dff'},   # Very high (pLDDT > 90)
        {'range': [70, 90],  'color': '#10cff1'},   # Confident (90 > pLDDT > 70)
        {'range': [50, 70],  'color': '#f6ed12'},   # Low (70 > pLDDT > 50)
        {'range': [0, 50],   'color': '#ef821e'}    # Very low (pLDDT < 50)
    ]
    for mapping in color_mapping:
        b_min, b_max = mapping['range']
        if b_min <= bfactor < b_max:
            return mapping['color']
    return 'grey'  # Default color

def visualize_structure(residue_bfactors, ligands, cif_content, background_color='#000000'):
    # Create a py3Dmol view
    view = py3Dmol.view(width='100%', height=600)
    view.addModel(cif_content, 'cif')

    # Set default style
    view.setStyle({'model': -1}, {'cartoon': {'color': 'grey'}})

    # Apply coloring based on B-factors
    for (chain_id, resseq), info in residue_bfactors.items():
        avg_bfactor = info['avg_bfactor']
        color = get_color_from_bfactor(avg_bfactor)
        selection = {'chain': chain_id, 'resi': resseq}
        style = {'cartoon': {'color': color}}
        view.addStyle(selection, style)

    # Color ligands
    for ligand in ligands:
        bfactor = ligand['bfactor']
        color = get_color_from_bfactor(bfactor)
        selection = {
            'chain': ligand['chain_id'],
            'resi': ligand['resseq'],
            'atom': ligand['atom_name']
        }
        style = {'stick': {'color': color}}
        view.addStyle(selection, style)

    # Set background color
    view.setBackgroundColor(background_color)

    # Generate HTML content
    view_html = view._make_html()
    return view_html

def display_visualization_header():
    st.write("### Visualization")
    color_mapping_html = """
    <div style='display: flex; flex-wrap: wrap; align-items: center; justify-content: center;'>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #106dff;'></div>
            <span style='margin-left: 5px;'>Very high (pLDDT > 90)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #10cff1;'></div>
            <span style='margin-left: 5px;'>Confident (90 > pLDDT > 70)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #f6ed12;'></div>
            <span style='margin-left: 5px;'>Low (70 > pLDDT > 50)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 5px;'>
            <div style='width: 20px; height: 20px; background-color: #ef821e;'></div>
            <span style='margin-left: 5px;'>Very low (pLDDT < 50)</span>
        </div>
    </div>
    """
    st.markdown(color_mapping_html, unsafe_allow_html=True)

def visualize_pae(pae_matrix):
    st.write("### Predicted Aligned Error (PAE)")
    fig = px.imshow(
        pae_matrix,
        color_continuous_scale='Greens_r',
        labels=dict(
            x="Residue index",
            y="Residue index",
            color="PAE (Å)"
        ),
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=80),
        coloraxis_colorbar=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            title_side='bottom'
        ),
        xaxis=dict(
            tickfont=dict(size=12),
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def display_summary_data(summary_data):
    st.write("### Summary of Confidence Metrics")
    # Convert summary data to DataFrame for better display
    df = pd.DataFrame(list(summary_data.items()), columns=['Metric', 'Value'])

    # Format arrays for better readability
    for index, row in df.iterrows():
        if isinstance(row['Value'], list):
            df.at[index, 'Value'] = json.dumps(row['Value'], indent=2)

    st.table(df)

# ========================================
# Main application
# ========================================

def main():
    # Set page configuration and theme
    st.set_page_config(
        page_title="AFusion Visualization",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS styles
    st.markdown("""
        <style>
        /* Remove padding */
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        /* Header styling */
        .css-10trblm {
            font-size: 2rem;
            color: #2c3e50;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f2f4f5;
        }
        /* Button styling */
        .stButton>button {
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title and subtitle
    st.markdown("<h1 style='text-align: center;'>🔬 AFusion: Visualization</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px;'>Visualize your AlphaFold 3 predictions</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px;'>If this project helps you, please ⭐️ <a href='https://github.com/Hanziwww/AlphaFold3-GUI' target='_blank'>my project</a>!</p>", unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        st.sidebar.markdown("---")
        sections = {
            "Introduction": "introduction",
            "Upload Files": "upload_files",
            "Visualization": "visualization",
            "Summary Metrics": "summary_metrics",
        }
        for section_name, section_id in sections.items():
            st.markdown(f"<a href='#{section_id}' style='text-decoration: none;'>{section_name}</a>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<small>Created by Hanzi 2024.</small>", unsafe_allow_html=True)

    st.markdown('<div id="introduction"></div>', unsafe_allow_html=True)
    st.markdown("### Welcome to AFusion Visualization!")
    st.markdown("Use this app to visualize your AlphaFold 3 prediction results.")

    # File upload section
    st.markdown('<div id="upload_files"></div>', unsafe_allow_html=True)
    st.header("📂 Upload Prediction Files")
    with st.expander("Upload Files", expanded=True):
        model_cif_file = st.file_uploader("Upload model.cif file", type=["cif"])
        confidences_json_file = st.file_uploader("Upload confidences.json file", type=["json"])
        summary_confidences_file = st.file_uploader("Upload summary_confidences.json file", type=["json"])

    if model_cif_file and confidences_json_file and summary_confidences_file:
        try:
            # Read and process files
            structure, cif_content = read_cif_file_obj(model_cif_file)
            residue_bfactors, ligands = extract_residue_bfactors(structure)
            pae_matrix = extract_pae_from_json_obj(confidences_json_file)
            summary_data = extract_summary_confidences_obj(summary_confidences_file)
            logger.info("Successfully loaded and processed uploaded files.")

            # Display visualization results
            st.markdown('<div id="visualization"></div>', unsafe_allow_html=True)
            st.header("🌟 Visualizations")
            display_visualization_header()

            # Create two columns, ratio 3:2
            col1, col2 = st.columns([3, 2])

            with col1:
                st.write("### 3D Model Visualization")
                if residue_bfactors or ligands:
                    view_html = visualize_structure(residue_bfactors, ligands, cif_content, background_color='#000000')
                    st.components.v1.html(view_html, height=600, scrolling=False)
                else:
                    st.error("Failed to extract atom data.")
                    logger.error("Failed to extract atom data.")

            with col2:
                # Visualize PAE matrix
                visualize_pae(pae_matrix)

            # Display summary data
            st.markdown('<div id="summary_metrics"></div>', unsafe_allow_html=True)
            display_summary_data(summary_data)

        except Exception as e:
            st.error(f"An error occurred while processing the files: {e}")
            logger.error(f"Error processing files: {e}")
    else:
        st.info("Please upload all required files to proceed.")

    st.markdown("---")
    # Provide log file download option
    st.markdown("### Download Log File 📥")
    with open('afusion_visualization.log', 'r') as log_file:
        log_content = log_file.read()
    st.download_button(
        label="Download Log File",
        data=log_content,
        file_name='afusion_visualization.log',
        mime='text/plain'
    )

    # Display log content
    with st.expander("Show Log Content 📄", expanded=False):
        st.text_area("Log Content", value=log_content, height=200)

    st.markdown("---")
    # Add footer
    st.markdown("<p style='text-align: center; font-size: 12px; color: #95a5a6;'>© 2024 Hanzi. All rights reserved.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
