# 🚀 **Network Latency Optimizer**

## 📋 **Project Overview**

**Network Latency Optimizer** is a web application that lets you:

- Upload and analyze PCAP files 📂
- Detect latency anomalies using an **One-Class SVM** model 🤖
- Optimize network paths using **Dijkstra's Algorithm** 🛠️

The application has a **React** frontend and a **Django** backend, offering project management, bulk uploads, and detailed analysis reports.

---

## 📂 **Project Structure**

```bash
Network-Latency-Optimizer/
│
├── backend/                  # 🐍 Django Backend
│   ├── manage.py             # Django entry point
│   ├── backend/              # Django project settings
│   ├── api/                  # API endpoints
│   │   ├── models.py         # Database models
│   │   ├── views.py          # API views
│   │   ├── serializers.py    # Serializers
│   │   └── urls.py           # API URLs
│   └── requirements.txt      # Backend dependencies
│
├── frontend/                 # ⚛️ React Frontend
│   ├── public/               # Public assets
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   ├── pages/            # React pages
│   │   ├── App.js            # Main component
│   │   └── index.js          # Entry point
│   └── package.json          # Frontend dependencies
│
└── venv/                     # 🐍 Virtual environment
```

---

## 🛠️ **Technologies Used**

### Backend 🐍

- **Django**: Web framework
- **Django REST Framework**: APIs
- **SQLite**: Database
- **django-cors-headers**: CORS management
- **scapy**: PCAP analysis
- **pandas & numpy**: Data manipulation

### Frontend ⚛️

- **React**: UI library
- **Axios**: API calls
- **Bootstrap / Tailwind CSS**: UI styling

### Machine Learning 🤖

- **One-Class SVM**: Anomaly detection
- **Dijkstra's Algorithm**: Path optimization

---

## 🌟 **Features**

### 1️⃣ **Create a Project**

- Create new projects by entering a name and description.

```bash
📝 Project Name: My Network Analysis
📝 Description: Analyzing network latency anomalies
```

[Create Project]

### 2️⃣ **Upload PCAP Files 📂**

- Bulk upload multiple PCAP files and view them in a list.

### 3️⃣ **Delete Files or Projects 🗑️**

- Delete unwanted files or entire projects with a click.

### 4️⃣ **Analyze Network Data 🕵️**

- Click **Analyze** to detect anomalies and optimize paths.

[Upload and Analyze]

### 5️⃣ **View Analysis Results 📊**

- See detailed results:
  - **Anomalies Detected**: Total anomalies found
  - **Average Latency**: Average latency in ms
  - **Optimization Table**: Current path, optimized path, and predicted latency.

---

## 🔎 **How It Works**

### 🚨 **Anomaly Detection**

- Uses an **One-Class SVM** model to detect abnormal latency patterns in the network data.

### 🗺️ **Path Optimization**

- Implements **Dijkstra's Algorithm** to find the shortest and most efficient path, minimizing latency.

---

## 📈 **Planned Enhancements**

1. **More Anomaly Parameters**:
   - Detect anomalies based on:
     - Packet Size 📦
     - Protocol Type 📡
     - Ports 🛠️

2. **Additional Metrics**:
   - Jitter
   - Packet Loss 📉
   - Timestamp ⏱️

3. **Charts and Graphs**:
   - **Latency Trends** 📊
   - **Jitter Distribution** 📈
   - **Anomaly Heatmaps** 🗺️

---

## 🛠️ **Installation Instructions**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/network-latency-optimizer.git
cd network-latency-optimizer
```

### 2. Backend Setup 🐍

```bash
cd backend
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### 3. Frontend Setup ⚛️

```bash
cd frontend
npm install
npm start
```

---

## 🚀 **Usage**

1. **Create a Project** 📝  
2. **Upload PCAP Files** 📂  
3. **Analyze Data** 🕵️‍♂️  
4. **View Results** 📊  

---

## 🖼️ **Screenshots**

1. **Project Creation**  

   ![image](https://github.com/user-attachments/assets/311fe5da-5cc3-43c9-9ad4-6c6dfdd247e5)


2. **PCAP Upload and Analysis** 

   ![image](https://github.com/user-attachments/assets/97cf95d0-9358-4b56-a961-cea72ad5a21a)


✨ Happy Coding! ✨
