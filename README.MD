# 🍼 Asisten Medis Stunting Indonesia (Indonesia Stunting Medical Assistant)

An AI-powered chatbot that helps mothers learn more about **stunting in Indonesia**—specializing in Indonesian context, government programs, and local solutions.  
Built using **Streamlit** with secure authentication, user management, and comprehensive knowledge powered by **GPT-5** focusing specifically on Indonesia.

**🌏 Available in English and Indonesian (Bahasa Indonesia)**
**🇮🇩 Specialized in Indonesian Stunting Context**

---

## 📌 Features

- **🔐 Secure Authentication**: User registration, login, and profile management
- **🤖 GPT-5 Powered Chatbot**: Most advanced AI for dynamic, Indonesia-focused responses
- **🌏 Bilingual Support**: English and Indonesian language support
- **🇮🇩 Indonesia-Specific Knowledge**: Focused on Indonesian stunting context and solutions
- **💬 Chat History**: Save and review your conversations
- **👤 User Profiles**: Manage your account and view statistics
- **📊 Growth Monitoring**: Track child development and identify risk factors
- **🌐 Responsive UI**: Beautiful Streamlit interface optimized for all devices
- **🔒 Data Security**: SQLite database with encrypted passwords
- **🚀 Dynamic AI Responses**: Engaging, conversational, and Indonesia-focused information

---

## 🇮🇩 Indonesia-Focused Stunting Knowledge

### **Why Indonesia-Specific Focus Matters:**

**🌏 Local Context Understanding:**
- **Regional Variations**: Different stunting prevalence across Indonesian provinces
- **Cultural Relevance**: Solutions that fit Indonesian family practices and beliefs
- **Government Programs**: Information about Indonesian stunting reduction initiatives
- **Local Success Stories**: Best practices from Indonesian communities

**🏥 Healthcare System Integration:**
- **Available Services**: Indonesian healthcare facilities and programs
- **Government Support**: Stunting Reduction Program (Program Penurunan Stunting)
- **Community Programs**: Local health center (Puskesmas) initiatives
- **Traditional Practices**: Integration with Indonesian cultural approaches

### **🇮🇩 4 Main Topics Covered:**

#### **1. STUNTING (Situasi Stunting di Indonesia)**
- **Current Prevalence**: Latest data from Indonesian Ministry of Health
- **Regional Distribution**: Stunting rates across different provinces
- **Risk Factors**: Specific to Indonesian context and environment
- **Trends**: Progress and challenges in Indonesia

#### **2. PENCEGAHAN (Prevention Strategies in Indonesia)**
- **Government Programs**: National stunting reduction initiatives
- **Community Strategies**: Local prevention approaches
- **Family Practices**: Practical tips for Indonesian families
- **Healthcare Integration**: Role of Puskesmas and health workers

#### **3. SOLUSI (Solutions Available in Indonesia)**
- **Medical Services**: Available treatment and interventions
- **Nutrition Programs**: Government and community nutrition initiatives
- **Rehabilitation**: Recovery and support programs
- **Monitoring**: Growth tracking and assessment tools

#### **4. DAMPAK (Impact on Indonesia)**
- **Child Development**: Effects on Indonesian children
- **Family Impact**: Economic and social consequences
- **National Development**: Long-term implications for Indonesia
- **Economic Cost**: Financial impact on Indonesian society

---

## 🚀 GPT-5 AI Capabilities

### **Why GPT-5 Makes the Difference:**

**🤖 Advanced Intelligence:**
- **Latest Information**: Access to the most current research and data about stunting
- **Dynamic Responses**: Every answer is unique, engaging, and conversational
- **Contextual Understanding**: Better comprehension of complex questions and follow-ups
- **Multilingual Excellence**: Superior language understanding for both English and Indonesian

**💡 Enhanced User Experience:**
- **Practical Examples**: Real-world scenarios and relatable case studies
- **Actionable Tips**: Specific, implementable advice for parents and caregivers
- **Interactive Style**: Engaging conversation that feels like talking to a knowledgeable friend
- **Rich Formatting**: Beautiful responses with emojis, bullet points, and structured information

**📊 Comprehensive Coverage:**
- **Evidence-Based**: Latest medical guidelines and research findings
- **Personalized**: Tailored responses based on the specific question context
- **Educational**: Progressive learning with detailed explanations and examples
- **Supportive**: Encouraging and positive tone for parents seeking help

### **Sample GPT-5 Responses:**

**🇺🇸 English Example:**
> "Great question! 🍼 Stunting is indeed a serious concern, but the good news is that it's largely preventable! Here's what you need to know:
> 
> **What is Stunting?** 
> Stunting occurs when a child's height is significantly below average for their age. Think of it as your child being "stuck" at a certain height percentile.
> 
> **The Critical Window** ⏰
> The first 1000 days (conception to age 2) are absolutely crucial! This is when your child's growth foundation is built.
> 
> **Practical Prevention Tips** 🌱
> 1. **Pregnancy**: Focus on iron-rich foods, take prenatal vitamins
> 2. **0-6 months**: Exclusive breastfeeding (no water, no formula)
> 3. **6+ months**: Introduce diverse, protein-rich complementary foods
> 
> **Quick Fact**: Did you know that proper nutrition in the first 1000 days can increase a child's adult height by up to 20cm? 📏"

**🇮🇩 Indonesian Example:**
> "Pertanyaan yang sangat bagus! 🍼 Stunting memang masalah serius, tapi kabar baiknya adalah ini bisa dicegah! Mari kita bahas:
> 
> **Apa itu Stunting?**
> Stunting terjadi ketika tinggi badan anak jauh di bawah rata-rata untuk usianya. Bayangkan seperti anak Anda "terjebak" pada persentil tinggi tertentu.
> 
> **Jendela Kritis** ⏰
> 1000 hari pertama (konsepsi hingga usia 2 tahun) sangat penting! Ini adalah saat fondasi pertumbuhan anak Anda dibangun.
> 
> **Tips Pencegahan Praktis** 🌱
> 1. **Kehamilan**: Fokus pada makanan kaya zat besi, minum vitamin prenatal
> 2. **0-6 bulan**: ASI eksklusif (tidak ada air, tidak ada susu formula)
> 3. **6+ bulan**: Perkenalkan makanan pendamping yang beragam dan kaya protein
> 
> **Fakta Cepat**: Tahukah Anda bahwa nutrisi yang tepat dalam 1000 hari pertama dapat meningkatkan tinggi badan dewasa anak hingga 20cm? 📏"

---

## 🛠 Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/) - Modern web app framework
- **Backend Logic**: Python 3.8+
- **AI Model**: **GPT-5 (GPT-4o)** - Most advanced AI language model for dynamic responses
- **Authentication**: Custom secure authentication system
- **Database**: SQLite with automatic backup
- **Environment Management**: `python-dotenv`
- **Data Processing**: Pandas for analytics
- **Language Support**: Bilingual (English & Indonesian)

---

## 📂 Project Structure

```
stunting_medical_assistant/
├── app.py                 # Main Streamlit application
├── auth_utils.py          # Authentication utilities
├── registration.py        # User registration component
├── user_profile.py        # User profile management
├── stunting_knowledge.py  # Comprehensive knowledge base
├── config.yaml            # Application configuration
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.MD             # This file
└── stunting_assistant.db  # SQLite database (created automatically)
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (optional, for enhanced responses)

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd stunting_medical_assistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```bash
# OpenAI API Configuration (REQUIRED for GPT-5 experience)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# App Configuration
APP_TITLE=Stunting Medical Assistant
APP_VERSION=1.0.0
```

**🚀 Getting Your OpenAI API Key:**
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up or log in to your account
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

**💡 Why GPT-5 Matters:**
- **Dynamic Responses**: Every answer is unique and engaging
- **Latest Information**: Access to current research and guidelines
- **Better Understanding**: Superior comprehension of complex questions
- **Multilingual Excellence**: Better support for both English and Indonesian

### 4. Run the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will open in your browser at http://localhost:8501
```

---

## 🔐 Default Login

A demo account is automatically created for testing:

- **Username**: `demo`
- **Password**: `demo123`

---

## 📱 Usage Guide

### For New Users

1. **Register**: Create a new account with your email and name
2. **Login**: Access your personalized dashboard
3. **Start Chatting**: Ask questions about stunting prevention and treatment
4. **Track Progress**: View your chat history and learning progress

### Available Topics

The chatbot can help you with:

- **What is stunting?** - Definition and characteristics
- **Causes** - Risk factors and contributing conditions
- **Prevention** - Strategies for different life stages
- **Treatment** - Management approaches and interventions
- **Growth Monitoring** - Assessment tools and frequency
- **Nutrition Guidelines** - Evidence-based recommendations
- **Risk Factors** - Individual and community risks
- **Early Warning Signs** - Recognition and when to seek help

### Sample Questions

**🇺🇸 English (Indonesia Focus):**
- "What's the current stunting situation in Indonesia?"
- "What government programs prevent stunting in Indonesia?"
- "How to prevent stunting in rural Indonesian villages?"
- "What healthcare services are available for stunting in Indonesia?"
- "What's the economic impact of stunting on Indonesia?"

**🇮🇩 Indonesian (Fokus Indonesia):**
- "Bagaimana situasi stunting di Indonesia saat ini?"
- "Apa program pemerintah untuk mencegah stunting?"
- "Bagaimana cara mencegah stunting di desa Indonesia?"
- "Layanan kesehatan apa yang tersedia untuk stunting di Indonesia?"
- "Apa dampak ekonomi stunting pada Indonesia?"

**🌟 4 Topik Utama (4 Main Topics):**
1. **STUNTING**: "Berapa prevalensi stunting di Jawa Barat?"
2. **PENCEGAHAN**: "Program apa yang ada di Puskesmas untuk mencegah stunting?"
3. **SOLUSI**: "Bagaimana cara mengobati stunting di Indonesia?"
4. **DAMPAK**: "Apa dampak stunting pada pembangunan Indonesia?"

---

## 🏗 Architecture

### Authentication System

- **Secure Password Hashing**: SHA-256 encryption
- **Session Management**: Secure cookie-based sessions
- **User Profiles**: Comprehensive account management
- **Access Control**: Role-based permissions (future enhancement)

### Knowledge Base

- **Local Expertise**: Built-in comprehensive stunting information
- **AI Enhancement**: OpenAI API integration for complex queries
- **Fallback System**: Local knowledge when AI is unavailable
- **Keyword Matching**: Intelligent response selection

### Database Design

- **Users Table**: Secure user account storage
- **Chat History**: Persistent conversation storage
- **Analytics**: User engagement and learning metrics
- **Backup System**: Automatic database backups

---

## 🔧 Configuration Options

### App Settings (`config.yaml`)

```yaml
app:
  title: Stunting Medical Assistant
  version: 1.0.0
  description: AI-powered chatbot for stunting education

features:
  openai_integration: true
  knowledge_base: true
  user_management: true
  chat_history: true

security:
  password_min_length: 6
  session_timeout_hours: 24
  max_login_attempts: 5
```

### Environment Variables (`.env`)

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Database
DATABASE_URL=sqlite:///stunting_assistant.db

# App Settings
APP_TITLE=Stunting Medical Assistant
APP_VERSION=1.0.0
```

---

## 🚀 Deployment

### Local Development

```bash
# Development mode with auto-reload
streamlit run app.py --server.runOnSave true
```

### Production Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501

# Run with gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:main
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🧪 Testing

### Manual Testing

1. **User Registration**: Test account creation
2. **Authentication**: Test login/logout functionality
3. **Chat Interface**: Test stunting-related queries
4. **Profile Management**: Test user settings
5. **Data Persistence**: Verify chat history storage

### Automated Testing (Future Enhancement)

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

---

## 🔒 Security Features

- **Password Encryption**: SHA-256 hashing
- **Session Management**: Secure cookie handling
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: Parameterized queries
- **XSS Prevention**: Output sanitization

---

## 📊 Analytics & Monitoring

### User Metrics

- **Registration Rate**: New user signups
- **Engagement**: Chat frequency and duration
- **Learning Progress**: Topic coverage and retention
- **User Satisfaction**: Response quality ratings

### System Metrics

- **Performance**: Response times and throughput
- **Error Rates**: API failures and system errors
- **Resource Usage**: Memory and CPU utilization
- **Database Health**: Connection status and performance

---

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Standards

- **Python**: PEP 8 compliance
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit tests for new features
- **Security**: Security review for authentication changes

---

## 📚 Resources

### Stunting Information

- [WHO Growth Standards](https://www.who.int/tools/child-growth-standards)
- [UNICEF Stunting Report](https://data.unicef.org/topic/nutrition/stunting/)
- [Global Nutrition Report](https://globalnutritionreport.org/)

### Technical Documentation

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 🆘 Support

### Common Issues

1. **Database Connection Error**: Check file permissions and path
2. **OpenAI API Error**: Verify API key and internet connection
3. **Authentication Issues**: Clear browser cookies and restart
4. **Performance Issues**: Check system resources and database size

### Getting Help

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs via GitHub issues
- **Community**: Join our discussion forum
- **Email**: Contact support team

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **WHO**: For growth standards and medical guidelines
- **UNICEF**: For global nutrition data and insights
- **OpenAI**: For AI language model capabilities
- **Streamlit**: For the excellent web app framework
- **Open Source Community**: For the tools and libraries that made this possible

---

## 📈 Roadmap

### Version 1.1 (Next Release)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Integration with health systems

### Version 1.2 (Future)
- [ ] Machine learning for personalized recommendations
- [ ] Voice interface support
- [ ] Offline mode capabilities
- [ ] Community features and forums

### Version 2.0 (Long-term)
- [ ] AI-powered growth prediction
- [ ] Telemedicine integration
- [ ] Blockchain for data security
- [ ] Global deployment and localization

---

**Made with ❤️ for better child health worldwide**

