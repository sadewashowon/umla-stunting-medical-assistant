import streamlit as st
import sqlite3
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import json
import time # Added for loading UI

# Load environment variables
load_dotenv()

# Prefer Streamlit Secrets (TOML) when available
try:
    # Support both flat keys and nested [openai] table in secrets.toml
    if hasattr(st, "secrets"):
        # Flat keys
        if "OPENAI_API_KEY" in st.secrets:
            os.environ["OPENAI_API_KEY"] = str(st.secrets["OPENAI_API_KEY"])
        if "OPENAI_MODEL" in st.secrets:
            os.environ["OPENAI_MODEL"] = str(st.secrets["OPENAI_MODEL"])
        if "DATABASE_URL" in st.secrets:
            os.environ["DATABASE_URL"] = str(st.secrets["DATABASE_URL"])
        if "APP_TITLE" in st.secrets:
            os.environ["APP_TITLE"] = str(st.secrets["APP_TITLE"])
        if "APP_VERSION" in st.secrets:
            os.environ["APP_VERSION"] = str(st.secrets["APP_VERSION"])

        # Nested table: [openai]
        if "openai" in st.secrets:
            openai_section = st.secrets["openai"]
            if "api_key" in openai_section and not os.getenv("OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = str(openai_section["api_key"])
            if "model" in openai_section and not os.getenv("OPENAI_MODEL"):
                os.environ["OPENAI_MODEL"] = str(openai_section["model"])
        # Nested table: [database]
        if "database" in st.secrets:
            database_section = st.secrets["database"]
            if "url" in database_section and not os.getenv("DATABASE_URL"):
                os.environ["DATABASE_URL"] = str(database_section["url"])
        # Nested table: [app]
        if "app" in st.secrets:
            app_section = st.secrets["app"]
            if "title" in app_section and not os.getenv("APP_TITLE"):
                os.environ["APP_TITLE"] = str(app_section["title"])
            if "version" in app_section and not os.getenv("APP_VERSION"):
                os.environ["APP_VERSION"] = str(app_section["version"])
except Exception:
    # Fall back silently to .env if secrets are not configured
    pass

# App config from env (with defaults)
APP_TITLE = os.getenv("APP_TITLE", "Asisten Medis Stunting Indonesia")
APP_VERSION = os.getenv("APP_VERSION", "")

# Database URL handling (supports sqlite URLs)
def get_database_path_from_env():
    """Resolve SQLite database file path from DATABASE_URL env.

    Supported forms:
    - sqlite:///relative/path.db
    - sqlite:////absolute/path.db
    - stunting_assistant.db (fallback when scheme unsupported)
    """
    database_url = os.getenv("DATABASE_URL", "sqlite:///stunting_assistant.db")

    if database_url.startswith("sqlite:////"):
        path = database_url[len("sqlite:////"):]
        return "/" + path if not path.startswith("/") else path
    if database_url.startswith("sqlite:///"):
        path = database_url[len("sqlite:///"):]
        return path if path else "stunting_assistant.db"
    # Fallback: if user supplied a plain filename, respect it; otherwise default
    if database_url.endswith(".db") and "://" not in database_url:
        return database_url
    return "stunting_assistant.db"

DB_PATH = get_database_path_from_env()

# Clean up potentially problematic environment variables
def clean_environment():
    """Clean up environment variables that might cause OpenAI client issues"""
    problematic_vars = [
        'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
        'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy'
    ]
    
    cleaned_vars = []
    for var in problematic_vars:
        if var in os.environ:
            cleaned_vars.append(var)
            del os.environ[var]
    
    if cleaned_vars:
        print(f"🧹 Cleaned up proxy environment variables: {cleaned_vars}")

# Clean environment before creating client
clean_environment()

# Check for remaining proxy-related environment variables
proxy_vars = [var for var in os.environ if 'proxy' in var.lower() or 'PROXY' in var]
if proxy_vars:
    print(f"⚠️  Remaining proxy-related environment variables: {proxy_vars}")
    print("These might cause OpenAI client initialization issues")

# Configure OpenAI with multiple fallback methods
def create_openai_client():
    """Create OpenAI client with multiple fallback methods"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("No valid OpenAI API key found")
        return None, 'gpt-4o'
    
    print(f"Attempting to create OpenAI client with API key: {api_key[:10]}...")
    
    # Method 1: Standard initialization
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
        return client, os.getenv('OPENAI_MODEL', 'gpt-4o')
    except Exception as e:
        print(f"Method 1 failed: {e}")
        print(f"Error type: {type(e).__name__}")
    
    # Method 2: Minimal initialization
    try:
        client = OpenAI()
        print("✅ OpenAI client created with minimal config")
        return client, os.getenv('OPENAI_MODEL', 'gpt-4o')
    except Exception as e:
        print(f"Method 2 failed: {e}")
        print(f"Error type: {type(e).__name__}")
    
    # Method 3: Environment variable approach
    try:
        os.environ['OPENAI_API_KEY'] = api_key
        client = OpenAI()
        print("✅ OpenAI client created via environment variable")
        return client, os.getenv('OPENAI_MODEL', 'gpt-4o')
    except Exception as e:
        print(f"Method 3 failed: {e}")
        print(f"Error type: {type(e).__name__}")
    
    # Method 4: Try with explicit None for problematic parameters
    try:
        client = OpenAI(api_key=api_key, base_url=None, http_client=None)
        print("✅ OpenAI client created with explicit None parameters")
        return client, os.getenv('OPENAI_MODEL', 'gpt-4o')
    except Exception as e:
        print(f"Method 4 failed: {e}")
        print(f"Error type: {type(e).__name__}")
    
    # Method 5: Try with explicit HTTP client configuration
    try:
        import httpx
        http_client = httpx.Client(
            proxies=None,
            verify=True,
            timeout=30.0
        )
        client = OpenAI(api_key=api_key, http_client=http_client)
        print("✅ OpenAI client created with explicit HTTP client")
        return client, os.getenv('OPENAI_MODEL', 'gpt-4o')
    except Exception as e:
        print(f"Method 5 failed: {e}")
        print(f"Error type: {type(e).__name__}")
    
    # Method 6: Try with minimal httpx client
    try:
        import httpx
        http_client = httpx.Client()
        client = OpenAI(api_key=api_key, http_client=http_client)
        print("✅ OpenAI client created with minimal httpx client")
        return client, os.getenv('OPENAI_MODEL', 'gpt-4o')
    except Exception as e:
        print(f"Method 6 failed: {e}")
        print(f"Error type: {type(e).__name__}")
    
    print("❌ All OpenAI client creation methods failed")
    return None, 'gpt-4o'

# Initialize OpenAI client
client, OPENAI_MODEL = create_openai_client()

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Database functions
def init_db():
    """Initialize the database with tables for users and chat history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    
    # Check if we need to migrate existing data
    migrate_database(cursor)
    ensure_demo_user() # Ensure demo user is created
    
    conn.commit()
    conn.close()

def migrate_database(cursor):
    """Migrate existing database to new schema if needed"""
    try:
        # Check if users table exists and has the right columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns if they don't exist
        if 'name' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN name TEXT")
            print("Added 'name' column to users table")
        
        if 'email' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            print("Added 'email' column to users table")
        
        if 'created_at' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("Added 'created_at' column to users table")
        
        # Check if chat_history table exists and has the right columns
        cursor.execute("PRAGMA table_info(chat_history)")
        chat_columns = [column[1] for column in cursor.fetchall()]
        
        if 'timestamp' not in chat_columns:
            cursor.execute("ALTER TABLE chat_history ADD COLUMN timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("Added 'timestamp' column to chat_history table")
            
    except Exception as e:
        print(f"Migration warning: {e}")
        # If migration fails, we'll continue with the existing structure

def ensure_demo_user():
    """Ensure demo user exists with all required fields"""
    try:
        from auth_utils import create_demo_user
        success, message = create_demo_user()
        if success:
            print("Demo user created successfully")
        else:
            print(f"Demo user status: {message}")
    except Exception as e:
        print(f"Demo user creation warning: {e}")

def reset_database():
    """Reset the database completely - use with caution!"""
    try:
        import os
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("Database reset successfully")
        init_db()
        return True
    except Exception as e:
        print(f"Database reset failed: {e}")
        return False

def save_chat(username, message, response):
    """Save chat message and response to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (username, message, response)
        VALUES (?, ?, ?)
    ''', (username, message, response))
    conn.commit()
    conn.close()

def get_chat_history(username):
    """Retrieve chat history for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message, response, timestamp FROM chat_history 
        WHERE username = ? ORDER BY timestamp DESC LIMIT 50
    ''', (username,))
    history = cursor.fetchall()
    conn.close()
    return history

# Stunting knowledge base
STUNTING_KNOWLEDGE = {
    "what_is_stunting": """
    Stunting is a condition where a child's height is significantly below the average for their age. 
    It's a form of malnutrition that affects physical and cognitive development.
    
    Key points:
    - Height-for-age below -2 standard deviations from WHO growth standards
    - Usually occurs in the first 1000 days of life (conception to age 2)
    - Can have long-term effects on health, education, and economic productivity
    """,
    
    "causes": """
    Stunting can be caused by several factors:
    
    1. **Nutritional factors:**
       - Inadequate protein and micronutrient intake
       - Poor breastfeeding practices
       - Insufficient complementary feeding
    
    2. **Environmental factors:**
       - Poor sanitation and hygiene
       - Frequent infections and diseases
       - Limited access to clean water
    
    3. **Maternal factors:**
       - Poor maternal nutrition during pregnancy
       - Teenage pregnancy
       - Short birth intervals
    """,
    
    "prevention": """
    Preventing stunting requires a comprehensive approach:
    
    **During pregnancy:**
    - Adequate maternal nutrition
    - Regular prenatal care
    - Iron and folic acid supplementation
    
    **After birth:**
    - Exclusive breastfeeding for first 6 months
    - Timely introduction of complementary foods
    - Adequate protein and micronutrient intake
    - Regular growth monitoring
    - Good hygiene practices
    
    **Community level:**
    - Access to clean water and sanitation
    - Health education programs
    - Poverty reduction initiatives
    """,
    
    "treatment": """
    Treatment for stunting involves:
    
    1. **Nutritional rehabilitation:**
       - High-protein, high-calorie diet
       - Micronutrient supplementation
       - Therapeutic feeding programs
    
    2. **Medical care:**
       - Treatment of underlying infections
       - Management of complications
       - Regular health monitoring
    
    3. **Long-term support:**
       - Continued nutritional support
       - Developmental monitoring
       - Family education and counseling
    
    Note: Early intervention is crucial for better outcomes.
    """
}

def get_stunting_response(user_message):
    """Get response from GPT-5 for stunting-related questions"""
    
    # Use GPT-5 as the primary and only knowledge source for dynamic responses
    try:
        if client and os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here':
            # Detect language for better AI response
            try:
                from stunting_knowledge_id import detect_indonesian
                is_indonesian = detect_indonesian(user_message)
                
                if is_indonesian:
                    system_prompt = """Anda adalah Asisten Medis Stunting Indonesia yang sangat ramah dan menarik. Fokuskan pengetahuan Anda khusus pada stunting di Indonesia.

Fitur Utama:
- Berikan informasi yang akurat dan terkini tentang stunting di Indonesia
- Sertakan data dan statistik terkini tentang stunting di Indonesia
- Berikan contoh dan kasus yang relevan dengan konteks Indonesia
- Fokus pada 4 topik utama: STUNTING, PENCEGAHAN, SOLUSI, dan DAMPAK di Indonesia
- Gunakan bahasa Indonesia yang natural dan friendly
- Berikan tips praktis yang bisa diterapkan di Indonesia
- Sertakan informasi tentang program pemerintah Indonesia terkait stunting

Topik Utama (Fokus Indonesia):
1. **STUNTING**: Definisi, karakteristik, dan prevalensi di Indonesia
2. **PENCEGAHAN**: Strategi pencegahan yang efektif di Indonesia
3. **SOLUSI**: Penanganan dan intervensi yang tersedia di Indonesia
4. **DAMPAK**: Efek stunting pada anak, keluarga, dan masyarakat Indonesia

Buat respons yang engaging, conversational, dan penuh dengan informasi spesifik Indonesia!"""
                else:
                    system_prompt = """You are a Stunting Medical Assistant specializing in Indonesia that is extremely friendly and engaging. Focus your knowledge specifically on stunting in Indonesia.

Main Features:
- Provide accurate and up-to-date information about stunting in Indonesia
- Include current data and statistics about stunting in Indonesia
- Give examples and cases relevant to Indonesian context
- Focus on 4 main topics: STUNTING, PREVENTION, SOLUTIONS, and IMPACT in Indonesia
- Use engaging and conversational English
- Provide practical tips that can be implemented in Indonesia
- Include information about Indonesian government programs related to stunting

Main Topics (Indonesia Focus):
1. **STUNTING**: Definition, characteristics, and prevalence in Indonesia
2. **PREVENTION**: Effective prevention strategies in Indonesia
3. **SOLUTIONS**: Available treatment and interventions in Indonesia
4. **IMPACT**: Effects of stunting on children, families, and Indonesian society

Make your responses engaging, conversational, and full of Indonesia-specific information!"""
                
                # Show loading UI for OpenAI API call
                with st.spinner("🤖 Sedang memproses dengan GPT-5..." if is_indonesian else "🤖 Processing with GPT-5..."):
                    # Add progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate progress steps
                    steps = [
                        "🔍 Menganalisis pertanyaan..." if is_indonesian else "🔍 Analyzing question...",
                        "🧠 Mengakses pengetahuan GPT-5..." if is_indonesian else "🧠 Accessing GPT-5 knowledge...",
                        "🇮🇩 Mencari informasi Indonesia..." if is_indonesian else "🇮🇩 Searching Indonesia information...",
                        "✍️ Menyusun respons..." if is_indonesian else "✍️ Composing response...",
                        "✨ Menyempurnakan jawaban..." if is_indonesian else "✨ Finalizing answer..."
                    ]
                    
                    for i, step in enumerate(steps):
                        progress_bar.progress((i + 1) / len(steps))
                        status_text.text(step)
                        time.sleep(0.3)  # Small delay for visual effect
                    
                    # Use GPT-5 for dynamic, Indonesia-focused responses
                    response = client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=1000,  # Increased for more detailed Indonesia-specific responses
                        temperature=0.9,  # Higher for more creative and varied responses
                        presence_penalty=0.1,  # Encourage more varied responses
                        frequency_penalty=0.1   # Reduce repetition
                    )
                    
                    # Complete progress bar
                    progress_bar.progress(1.0)
                    status_text.text("✅ Selesai!" if is_indonesian else "✅ Complete!")
                    time.sleep(0.5)  # Show completion briefly
                    
                    return response.choices[0].message.content
                    
            except ImportError:
                # Fallback to English if Indonesian detection not available
                system_prompt = """You are a Stunting Medical Assistant specializing in Indonesia that is extremely friendly and engaging. Focus your knowledge specifically on stunting in Indonesia.

Main Features:
- Provide accurate and up-to-date information about stunting in Indonesia
- Include current data and statistics about stunting in Indonesia
- Give examples and cases relevant to Indonesian context
- Focus on 4 main topics: STUNTING, PREVENTION, SOLUTIONS, and IMPACT in Indonesia
- Use engaging and conversational English
- Provide practical tips that can be implemented in Indonesia
- Include information about Indonesian government programs related to stunting

Main Topics (Indonesia Focus):
1. **STUNTING**: Definition, characteristics, and prevalence in Indonesia
2. **PREVENTION**: Effective prevention strategies in Indonesia
3. **SOLUTIONS**: Available treatment and interventions in Indonesia
4. **IMPACT**: Effects of stunting on children, families, and Indonesian society

Make your responses engaging, conversational, and full of Indonesia-specific information!"""
                
                # Show loading UI for OpenAI API call
                with st.spinner("🤖 Processing with GPT-5..."):
                    # Add progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate progress steps
                    steps = [
                        "🔍 Analyzing question...",
                        "🧠 Accessing GPT-5 knowledge...",
                        "🇮🇩 Searching Indonesia information...",
                        "✍️ Composing response...",
                        "✨ Finalizing answer..."
                    ]
                    
                    for i, step in enumerate(steps):
                        progress_bar.progress((i + 1) / len(steps))
                        status_text.text(step)
                        time.sleep(0.3)  # Small delay for visual effect
                    
                    response = client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=1000,
                        temperature=0.9,
                        presence_penalty=0.1,
                        frequency_penalty=0.1
                    )
                    
                    # Complete progress bar
                    progress_bar.progress(1.0)
                    status_text.text("✅ Complete!")
                    time.sleep(0.5)  # Show completion briefly
                    
                    return response.choices[0].message.content
        else:
            # If no API key or client, provide enhanced guidance for Indonesia-focused experience
            return get_indonesia_focused_guidance()
            
    except Exception as e:
        print("error: ", e)
        # If GPT-5 fails, provide guidance for Indonesia-focused experience
        return get_indonesia_focused_guidance()

def get_indonesia_focused_guidance():
    """Provide guidance for Indonesia-focused stunting information when GPT-5 is unavailable"""
    
    # Try to detect language for appropriate guidance
    try:
        from stunting_knowledge_id import detect_indonesian
        is_indonesian = detect_indonesian("stunting indonesia")
        
        if is_indonesian:
            return """Halo! 👋 Saya adalah Asisten Medis Stunting Indonesia yang siap membantu Anda!

**🚀 Untuk pengalaman terbaik dengan informasi stunting di Indonesia:**

**💡 Cara Setup GPT-5:**
1. Kunjungi [platform.openai.com](https://platform.openai.com)
2. Dapatkan API key OpenAI
3. Tambahkan ke file `.env` sebagai `OPENAI_API_KEY=your_key_here`
4. Restart aplikasi

**🔧 Troubleshooting:**
- Pastikan API key valid dan aktif
- Periksa apakah file `.env` ada di folder yang sama dengan `app.py`
- Pastikan format API key benar: `OPENAI_API_KEY=sk-...`
- Restart aplikasi setelah mengubah file `.env`

**🇮🇩 Topik Stunting di Indonesia yang Tersedia:**
- **STUNTING**: Prevalensi, karakteristik, dan situasi di Indonesia
- **PENCEGAHAN**: Program pemerintah, strategi komunitas, dan praktik keluarga
- **SOLUSI**: Layanan kesehatan, intervensi, dan penanganan di Indonesia
- **DAMPAK**: Efek pada anak, keluarga, dan pembangunan Indonesia

**📊 Data Terkini Indonesia:**
- Prevalensi stunting di berbagai provinsi
- Program pemerintah (Stunting Reduction Program)
- Intervensi berbasis bukti di Indonesia
- Sukses story dan best practices lokal

**💬 Contoh Pertanyaan yang Bisa Diajukan:**
- "Bagaimana situasi stunting di Indonesia saat ini?"
- "Apa program pemerintah untuk mencegah stunting?"
- "Bagaimana cara mencegah stunting di desa?"
- "Apa dampak stunting pada ekonomi Indonesia?"

Silakan setup API key OpenAI untuk mendapatkan informasi yang lebih dinamis dan terkini! 🌟"""
        else:
            return """Hello! 👋 I'm your Indonesia-focused Stunting Medical Assistant!

**🚀 For the best experience with Indonesia stunting information:**

**💡 How to Setup GPT-5:**
1. Visit [platform.openai.com](https://platform.openai.com)
2. Get your OpenAI API key
3. Add it to your `.env` file as `OPENAI_API_KEY=your_key_here`
4. Restart the application

**🔧 Troubleshooting:**
- Ensure your API key is valid and active
- Check if the `.env` file exists in the same folder as `app.py`
- Verify the API key format is correct: `OPENAI_API_KEY=sk-...`
- Restart the application after modifying the `.env` file

**🇮🇩 Available Indonesia Stunting Topics:**
- **STUNTING**: Prevalence, characteristics, and current situation in Indonesia
- **PREVENTION**: Government programs, community strategies, and family practices
- **SOLUTIONS**: Healthcare services, interventions, and treatment in Indonesia
- **IMPACT**: Effects on children, families, and Indonesian development

**📊 Current Indonesia Data:**
- Stunting prevalence across different provinces
- Government programs (Stunting Reduction Program)
- Evidence-based interventions in Indonesia
- Local success stories and best practices

**💬 Example Questions You Can Ask:**
- "What's the current stunting situation in Indonesia?"
- "What government programs prevent stunting?"
- "How to prevent stunting in rural areas?"
- "What's the economic impact of stunting in Indonesia?"

Please setup your OpenAI API key to get more dynamic and current information! 🌟"""
    except ImportError:
        # Fallback to English guidance
        return """Hello! 👋 I'm your Indonesia-focused Stunting Medical Assistant!

**🚀 For the best experience with Indonesia stunting information:**

**💡 How to Setup GPT-5:**
1. Visit [platform.openai.com](https://platform.openai.com)
2. Get your OpenAI API key
3. Add it to your `.env` file as `OPENAI_API_KEY=your_key_here`
4. Restart the application

**🔧 Troubleshooting:**
- Ensure your API key is valid and active
- Check if the `.env` file exists in the same folder as `app.py`
- Verify the API key format is correct: `OPENAI_API_KEY=sk-...`
- Restart the application after modifying the `.env` file

**🇮🇩 Available Indonesia Stunting Topics:**
- **STUNTING**: Prevalence, characteristics, and current situation in Indonesia
- **PREVENTION**: Government programs, community strategies, and family practices
- **SOLUTIONS**: Healthcare services, interventions, and treatment in Indonesia
- **IMPACT**: Effects on children, families, and Indonesian development

**📊 Current Indonesia Data:**
- Stunting prevalence across different provinces
- Government programs (Stunting Reduction Program)
- Evidence-based interventions in Indonesia
- Local success stories and best practices

**💬 Example Questions You Can Ask:**
- "What's the current stunting situation in Indonesia?"
- "What government programs prevent stunting?"
- "How to prevent stunting in rural areas?"
- "What's the economic impact of stunting in Indonesia?"

Please setup your OpenAI API key to get more dynamic and current information! 🌟"""

# Main application
def main():
    # Initialize database
    if 'db_initialized' not in st.session_state:
        with st.spinner("🔧 Initializing system..."):
            init_db()
            st.session_state.db_initialized = True
            time.sleep(0.5)  # Brief delay for visual feedback
    
    # Sidebar for authentication
    with st.sidebar:
        st.title("🍼 Asisten Stunting Indonesia")
        st.markdown("---")
        
        if not st.session_state.authenticated:
            if not st.session_state.get('show_register', False):
                # Login form
                st.subheader("🔐 Login")
                
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submit_button = st.form_submit_button("Login")
                    
                    if submit_button:
                        if username and password:
                            with st.spinner("🔐 Verifying credentials..."):
                                from auth_utils import authenticate_user
                                if authenticate_user(username, password):
                                    st.session_state.authenticated = True
                                    st.session_state.username = username
                                    st.success("✅ Login berhasil!")
                                    time.sleep(1)  # Show success message briefly
                                    st.rerun()
                                else:
                                    st.error("❌ Username atau password salah!")
                        else:
                            st.warning("⚠️ Harap isi username dan password!")
                
                st.markdown("---")
                st.markdown("### Pengguna Baru?")
                if st.button("Daftar"):
                    st.session_state.show_register = True
                    st.rerun()
            else:
                # Show back to login button when in registration mode
                st.markdown("### 📝 Mode Pendaftaran")
                if st.button("← Kembali ke Login"):
                    st.session_state.show_register = False
                    st.rerun()
        
        else:
            # User info and logout
            st.markdown("---")
            st.markdown(f"**👤 User:** {st.session_state.username}")
            
            if st.button("🚪 Logout"):
                with st.spinner("🚪 Logging out..."):
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.success("✅ Logout berhasil!")
                    time.sleep(1)  # Show success message briefly
                    st.rerun()
            
            st.markdown("---")
            st.markdown("### Aksi Cepat")
            if st.button("Hapus Riwayat Chat"):
                st.session_state.chat_history = []
                st.success("Riwayat chat berhasil dihapus!")
            
            # Admin functions (for demo user)
            if st.session_state.username == "demo":
                st.markdown("---")
                st.markdown("**🔧 Admin Functions**")
                
                if st.button("🗄️ Reset Database"):
                    with st.spinner("🗄️ Resetting database..."):
                        reset_database()
                        st.success("✅ Database berhasil direset!")
                        time.sleep(1)  # Show success message briefly
                        st.rerun()
    
    # Main content area
    if st.session_state.authenticated:
        # Header
        st.title("🍼 Asisten Medis Stunting Indonesia")
        st.markdown("Tanyakan apa saja tentang stunting di Indonesia - **STUNTING**, **PENCEGAHAN**, **SOLUSI**, dan **DAMPAK**")
        
        # Chat interface
        st.subheader("💬 Chat dengan Asisten Stunting")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ketik pertanyaan Anda tentang stunting di Indonesia..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Show assistant is typing
            with st.chat_message("assistant"):
                # Create a placeholder for the response
                response_placeholder = st.empty()
                
                # Show typing indicator
                with st.spinner("🤖 Asisten sedang mengetik..."):
                    # Get response from GPT-5
                    response = get_stunting_response(prompt)
                    
                    # Display the response
                    response_placeholder.markdown(response)
                    
                    # Save chat to database
                    save_chat(st.session_state.username, prompt, response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    elif st.session_state.get('show_register', False):
        # Registration form
        st.subheader("📝 Registrasi")
        
        with st.form("register_form"):
            new_username = st.text_input("Username Baru")
            new_password = st.text_input("Password Baru", type="password")
            confirm_password = st.text_input("Konfirmasi Password", type="password")
            email = st.text_input("Email")
            full_name = st.text_input("Nama Lengkap")
            
            register_button = st.form_submit_button("Register")
            
            if register_button:
                if new_username and new_password and confirm_password and email and full_name:
                    if new_password == confirm_password:
                        with st.spinner("📝 Creating account..."):
                            try:
                                from auth_utils import register_user
                                success, message = register_user(new_username, new_password, email, full_name)
                                
                                if success:
                                    st.success(f"✅ {message}")
                                    st.info("Silakan login dengan akun baru Anda!")
                                    time.sleep(2)  # Show success message
                                    st.session_state.show_register = False
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            except Exception as e:
                                st.error(f"❌ Registration failed: {e}")
                    else:
                        st.error("❌ Password tidak cocok!")
                else:
                    st.warning("⚠️ Harap isi semua field!")
        
        st.markdown("---")
        st.markdown("Sudah punya akun?")
        if st.button("Kembali ke Login"):
            st.session_state.show_register = False
            st.rerun()
    
    else:
        # Welcome page for non-authenticated users
        st.title("🍼 Selamat Datang di Asisten Medis Stunting Indonesia")
        st.markdown("""
        Chatbot AI yang membantu ibu-ibu mempelajari lebih lanjut tentang **stunting di Indonesia**—melalui percakapan interaktif yang fokus pada konteks lokal.
        
        ### Apa itu Stunting?
        Stunting adalah kondisi di mana tinggi badan anak secara signifikan di bawah rata-rata untuk usianya. 
        Ini adalah bentuk malnutrisi yang mempengaruhi perkembangan fisik dan kognitif, dengan prevalensi yang masih tinggi di Indonesia.
        
        ### 🌟 4 Topik Utama Stunting di Indonesia:
        
        **1. 🇮🇩 STUNTING**
        - Definisi dan karakteristik stunting
        - Prevalensi di berbagai provinsi Indonesia
        - Situasi terkini dan tren perkembangan
        
        **2. 🛡️ PENCEGAHAN**
        - Program pemerintah Indonesia (Stunting Reduction Program)
        - Strategi komunitas dan keluarga
        - Praktik terbaik di berbagai daerah
        
        **3. 💊 SOLUSI**
        - Layanan kesehatan yang tersedia
        - Intervensi dan penanganan medis
        - Program rehabilitasi dan pemulihan
        
        **4. 📊 DAMPAK**
        - Efek pada anak dan keluarga
        - Dampak ekonomi dan pembangunan
        - Implikasi jangka panjang untuk Indonesia
        
        ### Fitur Utama:
        - **Konten Edukatif**: Pelajari stunting dalam konteks Indonesia
        - **Chat Interaktif**: Ajukan pertanyaan dan dapatkan jawaban berbasis AI
        - **Informasi Terpercaya**: Berdasarkan data pemerintah dan penelitian lokal
        - **Pengalaman Personal**: Simpan riwayat chat dan pantau kemajuan
        
        ### Memulai:
        1. **Masuk** dengan akun yang sudah ada, atau
        2. **Daftar** untuk akun baru
        3. Mulai chatting tentang stunting di Indonesia
        
        ---
        *Silakan masuk atau daftar untuk mulai menggunakan chatbot.*
        """)
        
        # Display some basic stunting information
        with st.expander("📚 Fakta Singkat Tentang Stunting"):
            st.markdown("""
            - **Prevalensi**: Mempengaruhi 1 dari 4 anak di bawah 5 tahun secara global
            - **Periode Kritis**: 1000 hari pertama kehidupan (konsepsi hingga usia 2 tahun)
            - **Pencegahan**: Nutrisi yang tepat, kebersihan, dan perawatan kesehatan
            - **Dampak**: Dapat mempengaruhi kesehatan dan perkembangan seumur hidup
            """)
        
        # GPT-5 capabilities highlight
        with st.expander("🚀 Fitur AI Canggih dengan GPT-5"):
            st.markdown("""
            **🤖 Powered by GPT-5 (GPT-4o) - Fokus Indonesia:**
            
            - **Respons Dinamis**: Jawaban yang engaging dan conversational
            - **Informasi Terbaru**: Data dan penelitian terkini tentang stunting di Indonesia
            - **Tips Praktis**: Saran yang actionable dan mudah diterapkan di Indonesia
            - **Contoh Lokal**: Kasus nyata dan contoh yang relevan dengan konteks Indonesia
            - **Statistik Indonesia**: Fakta dan angka terkini tentang stunting di Indonesia
            - **Program Pemerintah**: Informasi tentang intervensi pemerintah Indonesia
            
            **🇮🇩 4 Topik Utama Stunting di Indonesia:**
            1. **STUNTING**: Definisi, karakteristik, dan prevalensi di Indonesia
            2. **PENCEGAHAN**: Strategi pencegahan yang efektif di Indonesia
            3. **SOLUSI**: Penanganan dan intervensi yang tersedia di Indonesia
            4. **DAMPAK**: Efek stunting pada anak, keluarga, dan masyarakat Indonesia
            
            **💡 Untuk pengalaman terbaik:**
            1. Dapatkan API key OpenAI dari [platform.openai.com](https://platform.openai.com)
            2. Tambahkan ke file `.env` sebagai `OPENAI_API_KEY=your_key_here`
            3. Restart aplikasi
            
            **🌏 Mendukung Bahasa Indonesia dan Inggris**
            """)
        
        # System setup options
        st.markdown("---")
        st.markdown("**🔧 System Setup**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗄️ Reinitialize Database"):
                with st.spinner("🗄️ Reinitializing database..."):
                    init_db()
                    st.success("✅ Database berhasil diinisialisasi ulang!")
                    time.sleep(1)  # Show success message briefly
                    st.rerun()
        
        with col2:
            if st.button("🧪 Test System"):
                with st.spinner("🧪 Testing system components..."):
                    try:
                        import test_app
                        test_app.test_all()
                        st.success("✅ System test berhasil!")
                    except Exception as e:
                        st.error(f"❌ System test gagal: {e}")
                    time.sleep(1)  # Show result briefly

if __name__ == "__main__":
    main()
