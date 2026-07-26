import streamlit as st
from pathlib import Path
import time

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Codebase Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>

/* ================================
   GLOBAL
================================ */

.main{
    padding-top:1rem;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:95%;
}

body{
    background:#0f172a;
    color:white;
}

h1,h2,h3,h4{
    color:white !important;
    font-weight:700;
}

/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"]{
    width:280px !important;
    background:#111827;
    border-right:1px solid #374151;
}

/* ================================
   CARDS
================================ */

.repo-card{
    background:#1e293b;
    border:1px solid #334155;
    border-radius:14px;
    padding:20px;
    margin-bottom:18px;
    color:white;
}

/* ================================
   METRIC CARDS
================================ */

div[data-testid="stMetric"]{

    background:#1e293b !important;
    border:1px solid #334155 !important;
    border-radius:14px;
    padding:18px;
}

div[data-testid="stMetric"] label{

    color:#cbd5e1 !important;
    font-size:15px !important;
    font-weight:600 !important;
}

div[data-testid="stMetricValue"]{

    color:white !important;
    font-size:34px !important;
    font-weight:700 !important;
}

div[data-testid="stMetricDelta"]{
    color:#22c55e !important;
}

/* ================================
   ALERT BOXES
================================ */

.success-box{
    background:#052e16;
    border-left:5px solid #22c55e;
    color:white;
    padding:14px;
    border-radius:8px;
}

.warning-box{
    background:#451a03;
    border-left:5px solid #f59e0b;
    color:white;
    padding:14px;
    border-radius:8px;
}

.info-box{
    background:#172554;
    border-left:5px solid #3b82f6;
    color:white;
    padding:14px;
    border-radius:8px;
}

/* ================================
   BUTTONS
================================ */

.stButton>button{

    width:100%;
    height:45px;
    border-radius:10px;
    font-weight:600;
    background:#2563eb;
    color:white;
    border:none;
}

.stButton>button:hover{
    background:#1d4ed8;
    color:white;
}

/* ================================
   HORIZONTAL LINE
================================ */

hr{
    margin:20px 0;
    border:1px solid #334155;
}

/* ================================
   HIDE STREAMLIT BRANDING
================================ */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header[data-testid="stHeader"]{
    height: 2.5rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# IMPORT BACKEND MODULES
# ==========================================================

# ---------- GitHub ----------
from github.validator import validate_github_url
from github.clone import clone_repository

# ---------- Scanner ----------
from scanner.file_scanner import scan_repository

# ---------- Reader ----------
from reader.file_reader import read_repository_files

# ---------- AI ----------
from ai.analyzer import RepositoryAnalyzer

# ---------- RAG ----------
from rag.chunker import RepositoryChunker
from rag.embeddings import EmbeddingGenerator
from rag.vector_store import VectorStore
from rag.chat import RepositoryChat

# ---------- Explorer ----------
from explorer.file_tree import get_repository_tree
from explorer.file_explainer import FileExplainer

# ---------- Architecture ----------
from architecture.dependency_graph import DependencyGraph
from architecture.call_graph import CallGraph
from architecture.diagram import ArchitectureDiagram

# ---------- Review ----------
from review.reviewer import RepositoryReviewer

# ---------- Security ----------
from security.scanner import SecurityScanner

# ---------- Refactoring ----------
from refactor.advisor import RefactoringAdvisor

# ---------- Reports ----------
from report.generator import ReportGenerator
from report.pdf_generator import PDFGenerator



# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_STATE = {

    "repository_loaded": False,

    "repo_path": None,

    "repository_data": None,

    "analysis": None,

    "vector_store": None,

    "report": None,

    "messages": [],

    "selected_page": "Dashboard",

    "mcp_agent": None,

}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# HEADER
# ==========================================================

st.title("🏗️ AI Codebase Architect")

st.caption(
    "AI-Powered Repository Analysis • Code Review • RAG Chat • MCP Assistant"
)

st.divider()
# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🏗️ AI Codebase Architect")

    st.caption("Repository Intelligence Platform")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💬 AI Chat",
            "📁 Explorer",
            "🏛️ Architecture",
            "🔍 Review",
            "📄 Reports",
    
        ]
    )

    st.session_state.selected_page = page

    st.divider()

    st.subheader("📂 GitHub Repository")

    github_input = st.text_input(
        "Repository",
        placeholder="owner/repository\nor\nhttps://github.com/owner/repository"
    )

    analyze_btn = st.button(
        "🚀 Analyze Repository",
        use_container_width=True,
        type="primary"
    )

    st.divider()

    if st.session_state.repository_loaded:

        st.success("✅ Repository Loaded")

        st.code(
            str(st.session_state.repo_path),
            language="text"
        )

        st.write("Repository is ready.")

        if st.button(
            "🗑️ Clear Session",
            use_container_width=True
        ):

            for key in DEFAULT_STATE:

                st.session_state[key] = DEFAULT_STATE[key]

            st.rerun()

# ==========================================================
# REPOSITORY LOADING
# ==========================================================

if analyze_btn:

    if github_input.strip() == "":

        st.warning("Please enter a GitHub repository.")

        st.stop()

    github_input = github_input.strip()

    if github_input.startswith("http"):

        github_url = github_input

    else:

        github_url = f"https://github.com/{github_input}"

    progress = st.progress(0)

    status = st.empty()

    # ---------------- Validation ----------------

    status.info("🔍 Validating repository...")

    if not validate_github_url(github_url):

        st.error("❌ Invalid GitHub repository.")

        st.stop()

    progress.progress(15)

    # ---------------- Clone ----------------

    status.info("📥 Cloning repository...")

    repo_path = clone_repository(github_url)

    st.session_state.repo_path = Path(repo_path)

    progress.progress(40)

    # ---------------- Scan ----------------

    status.info("📂 Scanning repository...")

    repository_data = scan_repository(
        st.session_state.repo_path
    )

    st.session_state.repository_data = repository_data

    progress.progress(60)

    # ---------------- AI Analysis ----------------

    status.info("🤖 AI repository analysis...")

    analyzer = RepositoryAnalyzer()

    st.session_state.analysis = analyzer.analyze(
        st.session_state.repo_path
    )

    progress.progress(75)

    # ---------------- Build Knowledge Base ----------------

    status.info("🧠 Building RAG knowledge base...")

    files = read_repository_files(
        st.session_state.repo_path
    )

    chunker = RepositoryChunker()

    chunks = chunker.chunk_repository(files)

    embedding_model = EmbeddingGenerator()

    embeddings = embedding_model.create_embeddings(chunks)

    vector_store = VectorStore()

    vector_store.build_index(
        embeddings,
        chunks
    )

    st.session_state.vector_store = vector_store

    progress.progress(90)


    progress.progress(100)

    status.success("✅ Repository Ready!")

    st.session_state.repository_loaded = True

    time.sleep(1)

    st.rerun()

# ==========================================================
# DASHBOARD HEADER
# ==========================================================

if not st.session_state.repository_loaded:

    st.info("👈 Enter a GitHub repository in the sidebar and click **Analyze Repository** to begin.")

else:

    repo = st.session_state.repository_data

    st.subheader("📊 Repository Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Files", repo["total_files"])

    with c2:
        st.metric("📁 Folders", repo["total_folders"])

    with c3:
        st.metric("💾 Size", f"{repo['total_size']:,} Bytes")

    with c4:
        st.metric("💻 Languages", len(repo["languages"]))

    st.divider()
    # ==========================================================
# DASHBOARD
# ==========================================================

if st.session_state.repository_loaded:

    st.subheader("📊 Repository Dashboard")

    repo = st.session_state.repository_data

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Files",
            repo.get("total_files", 0)
        )

    with col2:
        st.metric(
            "📁 Folders",
            repo.get("total_folders", 0)
        )

    with col3:
        st.metric(
            "💾 Size",
            f"{repo.get('total_size',0):,} Bytes"
        )

    with col4:
        st.metric(
            "💻 Languages",
            len(repo.get("languages", {}))
        )

    st.divider()

    # =====================================================
    # Repository Information
    # =====================================================

    left, right = st.columns([2, 1])

    with left:

        st.markdown("### 📂 Repository Information")

        st.write(f"**Repository:** `{st.session_state.repo_path.name}`")

        st.write(f"**Location:** `{st.session_state.repo_path}`")

        st.write(
            f"**Files:** {repo.get('total_files',0)}"
        )

        st.write(
            f"**Folders:** {repo.get('total_folders',0)}"
        )

    with right:

        st.markdown("### 💻 Languages")

        languages = repo.get("languages", {})

        if languages:

            for language, count in languages.items():

                st.write(f"**{language}** ({count})")

        else:

            st.info("No languages detected.")

    st.divider()

    # =====================================================
    # AI SUMMARY
    # =====================================================

    st.subheader("🤖 AI Repository Summary")

    if st.session_state.analysis is not None:

        st.success("Repository analysed successfully.")

        st.markdown(st.session_state.analysis)

    else:

        st.warning("Repository analysis not available.")

    st.divider()

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.subheader("⚡ Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "💬 Open AI Chat",
            use_container_width=True
        ):
            st.session_state.selected_page = "💬 AI Chat"
            st.rerun()

    with c2:

        if st.button(
            "📁 Open Explorer",
            use_container_width=True
        ):
            st.session_state.selected_page = "📁 Explorer"
            st.rerun()

    with c3:

        if st.button(
            "🏛️ Architecture",
            use_container_width=True
        ):
            st.session_state.selected_page = "🏛️ Architecture"
            st.rerun()

else:

    st.info(
        "👈 Enter a GitHub repository from the sidebar and click **Analyze Repository**."
    )
    # ==========================================================
# AI CHAT
# ==========================================================

if st.session_state.selected_page == "💬 AI Chat":

    st.header("💬 AI Repository Chat")

    if not st.session_state.repository_loaded:

        st.warning("Please analyse a repository first.")

    else:

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display previous messages
        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(
            "Ask anything about the repository..."
        )

        if question:

            # User message
            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):
                st.markdown(question)

            # AI response
            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:

                        chat = RepositoryChat(
                            st.session_state.vector_store
                        )

                        answer = chat.ask(question)

                    except Exception as e:

                        answer = f"Error: {e}"

                st.markdown(answer)

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "🗑 Clear Chat",
                use_container_width=True
            ):

                st.session_state.chat_history = []

                st.rerun()

        with c2:

            st.info(
                f"Messages : {len(st.session_state.chat_history)}"
            )
            # ==========================================================
# EXPLORER
# ==========================================================

if st.session_state.selected_page == "📁 Explorer":

    st.header("📁 Repository Explorer")

    if not st.session_state.repository_loaded:

        st.warning("Please analyse a repository first.")

    else:

        tree = get_repository_tree(
            st.session_state.repo_path
        )

        files = [
            item["path"]
            for item in tree
            if item["is_file"]
        ]

        if not files:

            st.info("No files found.")

        else:

            col1, col2 = st.columns([1, 2])

            with col1:

                st.subheader("Repository Files")

                selected = st.selectbox(
                    "Choose a file",
                    files
                )

            with col2:

                file_path = (
                    st.session_state.repo_path / selected
                )

                tab1, tab2 = st.tabs(
                    [
                        "📄 Source Code",
                        "🤖 AI Explanation"
                    ]
                )

                with tab1:

                    try:

                        code = file_path.read_text(
                            encoding="utf-8",
                            errors="ignore"
                        )

                        extension = file_path.suffix.replace(".", "")

                        st.code(
                            code,
                            language=extension
                        )

                    except Exception as e:

                        st.error(str(e))

                with tab2:

                    if st.button(
                        "Explain File",
                        use_container_width=True
                    ):

                        with st.spinner(
                            "AI is analysing the file..."
                        ):

                            explainer = FileExplainer()

                            explanation = explainer.explain(
                                file_path
                            )

                        st.markdown(explanation)
                        # ==========================================================
# SOFTWARE ARCHITECTURE
# ==========================================================

if st.session_state.selected_page == "🏛️ Architecture":

    st.header("🏛️ Software Architecture")

    if not st.session_state.repository_loaded:

        st.warning("Please analyse a repository first.")

    else:

        repo_path = st.session_state.repo_path

        tab1, tab2, tab3 = st.tabs(
            [
                "📦 Dependency Graph",
                "📞 Call Graph",
                "🏗 Mermaid Diagram"
            ]
        )

        # =====================================
        # Dependency Graph
        # =====================================

        with tab1:

            st.write(
                "Visualise module dependencies."
            )

            if st.button(
                "Generate Dependency Graph",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating dependency graph..."
                ):

                    try:

                        dependency = DependencyGraph()

                        graph = dependency.build(
                            repo_path
                        )

                        st.success(
                            "Dependency graph generated."
                        )

                        st.json(graph)

                    except Exception as e:

                        st.error(str(e))

        # =====================================
        # Call Graph
        # =====================================

        with tab2:

            st.write(
                "Visualise function call relationships."
            )

            if st.button(
                "Generate Call Graph",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating call graph..."
                ):

                    try:

                        call_graph = CallGraph()

                        graph = call_graph.build(
                            repo_path
                        )

                        st.success(
                            "Call graph generated."
                        )

                        st.json(graph)

                    except Exception as e:

                        st.error(str(e))

        # =====================================
        # Mermaid Diagram
        # =====================================

        with tab3:

            st.write(
                "Generate a Mermaid architecture diagram."
            )

            if st.button(
                "Generate Mermaid Diagram",
                use_container_width=True
            ):

                with st.spinner(
                    "Building architecture..."
                ):

                    try:

                        dependency = DependencyGraph()

                        dependency_graph = dependency.build(
                            repo_path
                        )

                        diagram = ArchitectureDiagram()

                        mermaid = diagram.generate(
                            dependency_graph
                        )

                        st.success(
                            "Architecture diagram generated."
                        )

                        st.code(
                            mermaid,
                            language="text"
                        )

                        st.info(
                            "Copy the Mermaid code into https://mermaid.live to view the diagram."
                        )

                    except Exception as e:

                        st.error(str(e))
                        # ==========================================================
# CODE REVIEW | SECURITY | REFACTORING
# ==========================================================

if st.session_state.selected_page == "🔍 Review":

    st.header("🔍 Code Quality & Security")

    if not st.session_state.repository_loaded:

        st.warning("Please analyse a repository first.")

    else:

        repo_path = st.session_state.repo_path

        review_tab, security_tab, refactor_tab = st.tabs(
            [
                "📝 Code Review",
                "🛡 Security Scan",
                "🔧 Refactoring"
            ]
        )

        # ======================================================
        # CODE REVIEW
        # ======================================================

        with review_tab:

            st.info(
                "Generate an AI-powered review of your repository."
            )

            if st.button(
                "🚀 Start Code Review",
                use_container_width=True
            ):

                progress = st.progress(0)

                with st.spinner("Reviewing repository..."):

                    try:

                        progress.progress(25)

                        reviewer = RepositoryReviewer()

                        progress.progress(60)

                        review = reviewer.review(repo_path)

                        progress.progress(100)

                        st.success(
                            "✅ Code Review Completed"
                        )

                        st.markdown(review)

                    except Exception as e:

                        st.error(str(e))

        # ======================================================
        # SECURITY
        # ======================================================

        with security_tab:

            st.info(
                "Scan the repository for common security issues."
            )

            if st.button(
                "🛡 Run Security Scan",
                use_container_width=True
            ):

                progress = st.progress(0)

                with st.spinner("Scanning repository..."):

                    try:

                        progress.progress(30)

                        scanner = SecurityScanner()

                        progress.progress(60)

                        report = scanner.scan(repo_path)

                        progress.progress(100)

                        st.success(
                            "✅ Security Scan Completed"
                        )

                        st.markdown(report)

                    except Exception as e:

                        st.error(str(e))

        # ======================================================
        # REFACTORING
        # ======================================================

        with refactor_tab:

            st.info(
                "Receive AI-powered refactoring suggestions."
            )

            if st.button(
                "✨ Analyse Refactoring",
                use_container_width=True
            ):

                progress = st.progress(0)

                with st.spinner("Analysing repository..."):

                    try:

                        progress.progress(30)

                        advisor = RefactoringAdvisor()

                        progress.progress(60)

                        suggestions = advisor.analyze(
                            repo_path
                        )

                        progress.progress(100)

                        st.success(
                            "✅ Refactoring Suggestions Generated"
                        )

                        st.markdown(suggestions)

                    except Exception as e:

                        st.error(str(e))
                        # ==========================================================
# REPORTS
# ==========================================================

if st.session_state.selected_page == "📄 Reports":

    st.header("📄 AI Repository Reports")

    if not st.session_state.repository_loaded:

        st.warning(
            "Please analyse a repository first."
        )

    else:

        tab1, tab2 = st.tabs(
            [
                "📑 AI Report",
                "📥 Export PDF"
            ]
        )

        # ==================================================
        # AI REPORT
        # ==================================================

        with tab1:

            st.write(
                "Generate a complete AI report for the repository."
            )

            if st.button(
                "🚀 Generate Report",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating report..."
                ):

                    try:

                        generator = ReportGenerator()

                        report = generator.generate(
                            st.session_state.repo_path
                        )

                        st.session_state.report = report

                        st.success(
                            "✅ Report Generated"
                        )

                        st.markdown(report)

                    except Exception as e:

                        st.error(str(e))

        # ==================================================
        # EXPORT PDF
        # ==================================================

        with tab2:

            if st.session_state.report is None:

                st.info(
                    "Generate a report first."
                )

            else:

                st.success(
                    "Report available for export."
                )

                if st.button(
                    "📥 Export PDF",
                    use_container_width=True
                ):

                    try:

                        pdf = PDFGenerator()

                        output_file = "repository_report.pdf"

                        pdf.create(
                            st.session_state.report,
                            output_file
                        )

                        with open(
                            output_file,
                            "rb"
                        ) as f:

                            st.download_button(
                                "⬇ Download Report",
                                f,
                                file_name="repository_report.pdf",
                                mime="application/pdf"
                            )

                        st.success(
                            "PDF exported successfully."
                        )

                    except Exception as e:

                        st.error(str(e))
                        # ==========================================================


        # ==================================================
        # STATUS
        # ==================================================

        with tab2:

            st.subheader("System Status")

            c1, c2 = st.columns(2)

            with c1:

                st.success("Repository Loaded")

                st.success("Vector Database Ready")

                st.success("AI Chat Ready")

                st.success("Explorer Ready")

            with c2:

                st.success("Architecture Ready")

                st.success("Security Ready")

                st.success("Reports Ready")

                if st.session_state.mcp_agent:

                    st.success("MCP Connected")

                else:

                    st.warning("MCP Not Connected")

        # ==================================================
        # ABOUT
        # ==================================================

        with tab3:

            st.markdown("""
### AI Codebase Architect

A professional repository intelligence platform.

### Features

- Repository Analysis
- RAG Knowledge Base
- AI Repository Chat
- File Explorer
- Architecture Analysis
- AI Code Review
- Security Scanner
- Refactoring Suggestions
- AI Report Generator
- PDF Export
- MCP Integration

---

Version **2.0**
            """)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

left, right = st.columns([3, 1])

with left:

    st.caption(
        "🏗 AI Codebase Architect | Repository Intelligence Platform"
    )

with right:

    st.caption("Version 2.0")
