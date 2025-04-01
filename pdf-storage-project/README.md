# PDF Storage Docker Service

## 🖥️ Setting Up WSL (Windows Subsystem for Linux)

### 1. Enable WSL on Windows
1. Open PowerShell as Administrator
2. Run the following command:
```powershell
wsl --install
```

### 2. Install Ubuntu (Recommended)
1. Open Microsoft Store
2. Search for "Ubuntu"
3. Install the latest LTS version

### 3. Initial WSL Setup
After installation, open Ubuntu and:
```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    curl \
    git \
    wget \
    software-properties-common
```

### 4. Install Docker in WSL
```bash
# Remove any existing Docker installations
sudo apt-get remove docker docker-engine docker.io containerd runc

# Set up Docker repository
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installations
docker --version
docker-compose --version
```

### 5. Project Setup
Create a directory for your projects:
```bash
# Create projects directory
mkdir -p ~/projects/pdf-storage
cd ~/projects/pdf-storage
```

## 📂 Project Structure
```
pdf-storage/
│
├── pdfs/
│   ├── informatics/
│   │   └── (place your PDFs here)
│   └── cscience/
│       └── (place your PDFs here)
│
├── docker/
│   ├── postgres/
│   │   └── init.sql
│   └── app/
│       ├── Dockerfile
│       └── requirements.txt
│
├── src/
│   └── app.py
│
├── .env
├── docker-compose.yml
└── README.md
```

## 🚀 Starting the Service
```bash
# Navigate to project directory
cd ~/projects/pdf-storage

# Create PDF directories if not exist
mkdir -p pdfs/informatics pdfs/cscience

# Configure environment variables
nano .env
# Edit POSTGRES_USER and POSTGRES_PASSWORD

# Build and start the service
docker-compose up --build -d
```

## 🌐 Accessing the Service
- **Web Interface**: `http://localhost:5000`
- **List PDFs**: `http://localhost:5000/pdfs`
- **Open PDF**: `http://localhost:5000/<10-digit-hash-code>`

## 🔧 Troubleshooting WSL

### Common Issues
- **Docker not starting**:
  ```bash
  # Restart Docker service
  sudo service docker start
  ```

- **Permission issues**:
  ```bash
  # Ensure you're in the docker group
  newgrp docker
  ```

### Resetting Docker
```bash
# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Prune system
docker system prune -a
```

## 📝 Notes
- Always keep your WSL and Docker updated
- Use strong, unique passwords in `.env`
- Backup your PDFs regularly

---