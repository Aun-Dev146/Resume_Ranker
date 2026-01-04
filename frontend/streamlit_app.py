# frontend/streamlit_app.py
import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Resume Ranker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📄 Resume Ranker")
st.markdown("AI-powered resume ranking system using semantic similarity matching")

# Initialize session state
if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "uploaded_resumes" not in st.session_state:
    st.session_state.uploaded_resumes = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API connection status
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ Cannot reach API")
    
    st.divider()
    
    # Clear data button
    if st.button("🗑️ Clear All Data", key="clear_data"):
        st.session_state.job_id = None
        st.session_state.uploaded_resumes = []
        st.success("Data cleared!")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload", "🎯 Rank", "📊 Results"])

# TAB 1: Upload
with tab1:
    st.header("Upload Documents")
    
    col1, col2 = st.columns(2)
    
    # Resume Upload
    with col1:
        st.subheader("📝 Resumes")
        st.write("Upload one or more resume files (PDF or DOCX)")
        
        resume_files = st.file_uploader(
            "Choose resume files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="resume_uploader"
        )
        
        if resume_files:
            resume_progress = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(resume_files):
                status_text.text(f"Processing: {file.name}")
                
                try:
                    # Get candidate name
                    candidate_name = st.text_input(
                        f"Candidate name for {file.name}",
                        value=file.name.split('.')[0],
                        key=f"candidate_{file.name}"
                    )
                    
                    # Upload file
                    files = {"file": file}
                    params = {"candidate_name": candidate_name}
                    
                    response = requests.post(
                        f"{API_BASE_URL}/upload-resume",
                        files=files,
                        params=params
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.uploaded_resumes.append(data)
                        st.success(f"✅ {file.name} uploaded!")
                    else:
                        st.error(f"❌ Failed to upload {file.name}")
                
                except Exception as e:
                    st.error(f"Error uploading {file.name}: {str(e)}")
                
                resume_progress.progress((idx + 1) / len(resume_files))
            
            status_text.empty()
            resume_progress.empty()
    
    # Job Description Upload
    with col2:
        st.subheader("💼 Job Description")
        st.write("Upload a job description (as text or file)")
        
        job_input_method = st.radio(
            "Choose input method",
            ["Text Input", "File Upload"],
            key="job_input_method"
        )
        
        if job_input_method == "Text Input":
            job_title = st.text_input("Job Title", placeholder="e.g., Senior Python Developer")
            company = st.text_input("Company Name (optional)", placeholder="e.g., Tech Corp")
            job_content = st.text_area(
                "Job Description",
                height=200,
                placeholder="Paste job description here..."
            )
            
            if st.button("📤 Upload Job Description", key="upload_job_text"):
                if job_title and job_content:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/upload-job-description",
                            params={
                                "job_title": job_title,
                                "company": company,
                                "content": job_content
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.job_id = data["id"]
                            st.success(f"✅ Job description uploaded!")
                            st.info(f"Job ID: {data['id']}")
                        else:
                            st.error(f"Failed: {response.json()}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill in Job Title and Description")
        
        else:  # File Upload
            job_title = st.text_input("Job Title", placeholder="e.g., Senior Python Developer")
            company = st.text_input("Company Name (optional)", placeholder="e.g., Tech Corp")
            job_file = st.file_uploader(
                "Choose a job description file",
                type=["pdf", "docx"],
                key="job_file_uploader"
            )
            
            if job_file and st.button("📤 Upload Job File", key="upload_job_file"):
                if job_title:
                    try:
                        files = {"file": job_file}
                        params = {
                            "job_title": job_title,
                            "company": company
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/upload-job-description",
                            files=files,
                            params=params
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.job_id = data["id"]
                            st.success(f"✅ Job file uploaded!")
                            st.info(f"Job ID: {data['id']}")
                        else:
                            st.error(f"Failed: {response.json()}")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please enter Job Title")

# TAB 2: Rank
with tab2:
    st.header("🎯 Rank Resumes")
    
    if st.session_state.job_id:
        st.info(f"Job ID: {st.session_state.job_id}")
        
        if len(st.session_state.uploaded_resumes) > 0:
            st.write(f"**Resumes to rank:** {len(st.session_state.uploaded_resumes)}")
            
            if st.button("🚀 Start Ranking", key="start_ranking"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/rank-resumes",
                        params={"job_id": st.session_state.job_id}
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        st.session_state.ranking_results = results
                        st.success("✅ Ranking completed!")
                        
                        # Display results summary
                        st.divider()
                        st.subheader("📊 Results Summary")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Job Title", results["job_title"])
                        with col2:
                            st.metric("Total Resumes", results["total_resumes"])
                        with col3:
                            if results["rankings"]:
                                top_score = results["rankings"][0]["similarity_score"]
                                st.metric("Top Score", f"{top_score:.4f}")
                        
                        st.divider()
                        
                        # Display rankings table
                        rankings_data = []
                        for ranking in results["rankings"]:
                            rankings_data.append({
                                "Rank": ranking.get("rank", "N/A"),
                                "Candidate": ranking["candidate_name"],
                                "Score": f"{ranking['similarity_score']:.4f}",
                                "File": ranking["filename"]
                            })
                        
                        df = pd.DataFrame(rankings_data)
                        st.dataframe(df, use_container_width=True)
                        
                        # Export option
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "📥 Download Results (CSV)",
                            csv,
                            "ranking_results.csv",
                            "text/csv"
                        )
                    else:
                        st.error(f"Ranking failed: {response.json()}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ No resumes uploaded yet. Please upload resumes first.")
    else:
        st.warning("⚠️ No job description uploaded yet. Please upload a job description first.")

# TAB 3: Results
with tab3:
    st.header("📊 View Results")
    
    if st.session_state.job_id:
        try:
            response = requests.get(
                f"{API_BASE_URL}/results",
                params={"job_id": st.session_state.job_id}
            )
            
            if response.status_code == 200:
                results = response.json()
                
                st.subheader(f"Job: {results['job_title']}")
                st.write(f"Total Results: {results['total_results']}")
                
                if results["rankings"]:
                    # Create visualization
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("Score Distribution")
                        scores = [r["similarity_score"] for r in results["rankings"]]
                        
                        chart_data = pd.DataFrame({
                            "Rank": [r["rank"] for r in results["rankings"]],
                            "Score": scores
                        })
                        
                        st.bar_chart(chart_data.set_index("Rank"))
                    
                    with col2:
                        st.subheader("Statistics")
                        scores = [r["similarity_score"] for r in results["rankings"]]
                        st.metric("Average Score", f"{sum(scores)/len(scores):.4f}")
                        st.metric("Max Score", f"{max(scores):.4f}")
                        st.metric("Min Score", f"{min(scores):.4f}")
                    
                    st.divider()
                    
                    # Detailed table
                    st.subheader("Detailed Rankings")
                    results_data = []
                    for ranking in results["rankings"]:
                        results_data.append({
                            "Rank": ranking["rank"],
                            "Resume ID": ranking["resume_id"],
                            "Score": f"{ranking['similarity_score']:.4f}"
                        })
                    
                    df = pd.DataFrame(results_data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No results yet. Please rank resumes first.")
            else:
                st.warning("No results available for this job.")
        
        except Exception as e:
            st.warning(f"Could not fetch results: {str(e)}")
    else:
        st.info("Upload a job description to view results.")
 
