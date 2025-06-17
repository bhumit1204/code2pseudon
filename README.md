
# Code2Pseudo  
**Bridging Code & Clarity with AI**
---

## 🔹 Short Description

**Code2Pseudo**: Your AI-powered Flask app converts code to pseudocode & vice-versa using Meta Llama 3.3. Browse community snippets & chat-generate pseudocode, with data stored in Zilliz Milvus. Simplify code comprehension effortlessly!

---

## 🔸 Long Description

**Code2Pseudo**, developed by **Team Code Catalysts** for the *Trae AI Hackathon*, is an innovative Flask application designed to bridge the gap between complex programming languages and easily understandable pseudocode.

Our app facilitates **bi-directional conversion**, allowing users to transform code from virtually any language into clear pseudocode and, importantly, convert pseudocode back into functional code. This capability enhances code comprehension, simplifies technical explanations for non-developers, and streamlines the development workflow.

At its core, Code2Pseudo leverages the powerful **Meta Llama 3.3 8B model**, fine-tuned with precise system prompts for highly accurate and contextually relevant conversions. Using **OpenRouter** ensures seamless and efficient interaction with the AI model.

Beyond conversion, Code2Pseudo offers a unique **community browsing feature** powered by **Zilliz Milvus**, allowing users to explore a growing repository of shared code and pseudocode snippets. A dynamic **chat-based pseudocode generator** enables interactive pseudocode creation from natural language input.

> **Code2Pseudo is more than a tool; it's a collaborative platform aimed at making programming logic accessible to everyone.**

---

## 🌟 Features

- **Universal Language Support**  
  Converts code from multiple programming languages (e.g., Python, Java, C++, JavaScript) into clear pseudocode.

- **Bi-directional Conversion**  
  Convert code to pseudocode and vice-versa (pseudocode to working code).

- **Chat-Based Pseudocode Generator**  
  Interactively generate pseudocode from natural language descriptions.

- **Community Showcase (Data Browser)**  
  Explore a library of user-generated code and pseudocode.

- **Intuitive User Interface**  
  Clean, user-friendly design with smooth navigation.

---

## 🧰 Tech Stack
- **Trae IDE**  
  A powerful IDE built with AI agent within it, checkout this images of the IDE.
  ![Screenshot 2025-06-15 092737](https://github.com/user-attachments/assets/0aa72870-fd3f-458e-beb8-1a6c31227298)
  
  ![Screenshot 2025-06-15 104316](https://github.com/user-attachments/assets/dcf27ada-6e19-408f-a5c2-dc7bc8b0a639)

- **Flask App**  
  Lightweight, flexible web framework powering the frontend and backend.

- **OpenRouter**  
  Unified API gateway for communicating with large language models.

- **Meta Llama 3.3 8B**  
  Core AI model for smart code/pseudocode conversion.

- **Zilliz Milvus**  
  High-performance vector database for storing and searching shared snippets.

---

## 🚀 Getting Started

To run **Code2Pseudo** locally:

### 1. Clone the Repository

```bash
git clone https://github.com/YourGitHubUsername/Code2Pseudo.git
cd Code2Pseudo
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
ZILLIZ_MILVUS_HOST=your_milvus_host
ZILLIZ_MILVUS_PORT=your_milvus_port
# Add other necessary keys here
```

### 5. Run the Flask Application

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to access the app.

---

## 🛠 How to Use

* **Code Conversion**:
  Paste code, select "pseudocode", and click *Convert*.

* **Pseudocode Conversion**:
  Paste pseudocode, select target language (e.g., Python), and click *Convert*.

* **Chat-Based Generation**:
  Navigate to the chat interface, describe your logic, and receive pseudocode.

* **Browse Community Content**:
  Head to the 'Browse' tab to explore and learn from user submissions.

---

## 🔮 Future Enhancements

* **IDE Integrations**
  Plugins for VSCode and other IDEs to use Code2Pseudo within development environments.

* **Advanced Customization**
  Define pseudocode formatting style and detail level.

* **Version Control Integration**
  Link converted outputs directly to Git repositories.

* **Expanded AI Model Options**
  Add support for other AI models via OpenRouter.

* **Specialized Domain Support**
  Domain-specific pseudocode conversion (e.g., ML, data science).
