#!/bin/bash
# Banner with developer name
banner () {
echo -e "\n######################################################"
echo -e "#                                                    #"
echo -e "#  Docker & Docker Compose Setup by FancybearIN     #"
echo -e "#                                                    #"
echo -e "######################################################\n"
}

banner

# Determine the operating system
OS=$(uname -s)

# Function to install packages using apt
apt_install() {
  sudo apt update
  sudo apt install -y "$@"
}

# Function to install packages using pacman
pacman_install() {
  sudo pacman -S --noconfirm "$@"
}

# Function to remove packages using apt
apt_remove() {
  sudo apt-get remove --purge "$@" 2>/dev/null || true
}

# Function to remove packages using pacman
pacman_remove() {
  sudo pacman -Rns --noconfirm "$@"
}

# Function to check if a command exists
command_exists() {
  command -v "$1" &> /dev/null
}

# Remove old packages
if [[ "$OS" == "Linux" ]]; then
  if command_exists apt-get; then
    apt_remove docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc curl git 
  elif command_exists pacman; then
    pacman_remove docker docker-compose curl git 
  fi
fi

# Install Docker
if ! command_exists docker; then
  if [[ "$OS" == "Linux" ]]; then
    if command_exists apt-get; then
      echo "Docker is not installed. Installing Docker..."
      apt_install docker.io
    elif command_exists pacman; then
      echo "Docker is not installed. Installing Docker..."
      pacman_install docker
    fi
  fi
fi

# Install Docker Compose
if ! command_exists docker-compose; then
  if [[ "$OS" == "Linux" ]]; then
    if command_exists apt-get; then
      echo "Docker Compose is not installed. Installing Docker Compose..."
      sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose
    elif command_exists pacman; then
      echo "Docker Compose is not installed. Installing Docker Compose..."
      pacman_install docker-compose
    fi
  fi
fi

# Start Docker and Docker Compose services
dock() {
  if ! docker ps -a &> /dev/null; then
    echo "Docker is not running. Starting Docker..."
    if [[ "$OS" == "Linux" ]]; then
      if command_exists systemctl; then
        sudo systemctl enable docker
        sudo systemctl start docker
      fi
    fi
  fi
}

# Service start the docker compose
dock_C() {
  if ! docker-compose ps -a &> /dev/null; then
    echo "Docker Compose is not running. Starting Docker Compose..."
    if [[ "$OS" == "Linux" ]]; then
      if command_exists systemctl; then
        sudo systemctl enable docker-compose
        sudo systemctl start docker-compose
      fi
    fi
  fi
}

# Function to clone GitHub/GitLab repository
github() {
  # Get the username
  username=$(logname)

  # Create the github directory if it doesn't exist
  mkdir -p "/home/$username/github"
  cd "/home/$username/github"

  read -p "Enter the GitHub or GitLab URL: " -r url
  git clone "$url"
  cd $(basename "$url" .git)  # Navigate to the cloned repository directory
}


# Dockerfile creation function for Node.js
create_dockerfile_node() {
  read -p "Do you want to use the latest Node.js version or a specific version? (latest/specific): " -r version_choice

  case $version_choice in
    latest)
      node_version="node:latest"
      ;;
    specific)
      read -p "Enter the specific Node.js version: " -r node_version
      node_version="node:$node_version"
      ;;
    *)
      echo "Invalid choice. Please enter 'latest' or 'specific'."
      exit 1
      ;;
  esac

  read -p "Enter the working directory location (default: /app): " -r workdir
  if [[ -z "$workdir" ]]; then
    workdir="/app"
  fi

  echo "FROM $node_version" > Dockerfile
  echo "WORKDIR $workdir" >> Dockerfile
  echo "COPY package.json package-lock.json $workdir" >> Dockerfile
  echo "RUN npm install" >> Dockerfile
  echo "COPY . $workdir" >> Dockerfile
  echo "CMD [\"npm\", \"start\"]" >> Dockerfile

  echo "Dockerfile created successfully!"
  cat Dockerfile
}

# Dockerfile creation function for Django
create_dockerfile_django() {
  read -p "Do you want to use the latest Python version or a specific version? (latest/specific): " -r version_choice

  case $version_choice in
    latest)
      python_version="python:latest"
      ;;
    specific)
      read -p "Enter the specific Python version: " -r python_version
      python_version="python:$python_version"
      ;;
    *)
      echo "Invalid choice. Please enter 'latest' or 'specific'."
      exit 1
      ;;
  esac

  read -p "Enter the working directory location (default: /app): " -r workdir
  if [[ -z "$workdir" ]]; then
    workdir="/app"
  fi

  echo "FROM $python_version" > Dockerfile
  echo "WORKDIR $workdir" >> Dockerfile
  echo "COPY requirements.txt $workdir" >> Dockerfile
  echo "RUN pip install -r requirements.txt" >> Dockerfile
  echo "COPY . $workdir" >> Dockerfile
  echo "CMD [\"python\", \"manage.py\", \"runserver\", \"0.0.0.0:8000\"]" >> Dockerfile

  echo "Dockerfile created successfully!"
  cat Dockerfile
}

# Dockerfile creation function for Node.js
build_dockerfile_node() {
  # ... (Previous code remains the same) ...

  echo "Dockerfile created successfully!"
  cat Dockerfile

  # Build the Docker image
  read -p "Enter the image name (default: my-node-app): " -r image_name
  if [[ -z "$image_name" ]]; then
    image_name="my-node-app"
  fi
  docker build -t "$image_name" .
  echo "Docker image built successfully!"
}

# Dockerfile creation function for Django
build_dockerfile_django() {
  # ... (Previous code remains the same) ...

  echo "Dockerfile created successfully!"
  cat Dockerfile

  # Build the Docker image
  read -p "Enter the image name (default: my-django-app): " -r image_name
  if [[ -z "$image_name" ]]; then
    image_name="my-django-app"
  fi
  docker build -t "$image_name" .
  echo "Docker image built successfully!"
}

# Function to build Docker image for Node.js
build_dockerfile_node() {
  read -p "Enter the image name (default: my-node-app): " -r image_name
  if [[ -z "$image_name" ]]; then
    image_name="my-node-app"
  fi
  docker build -t "$image_name" .
  echo "Docker image built successfully!"
}

# Function to build Docker image for Django
build_dockerfile_django() {
  read -p "Enter the image name (default: my-django-app): " -r image_name
  if [[ -z "$image_name" ]]; then
    image_name="my-django-app"
  fi
  docker build -t "$image_name" .
  echo "Docker image built successfully!"
}

# Function to create docker-compose.yml
create_docker_compose() {
  read -p "Enter the service name (default: app): " -r service_name
  if [[ -z "$service_name" ]]; then
    service_name="app"
  fi

  read -p "Enter the port to expose (default: 3000): " -r port
  if [[ -z "$port" ]]; then
    port="3000"
  fi

  cat <<EOF > docker-compose.yml
version: '3.7'

services:
  $service_name:
    build: .
    ports:
      - "$port:$port"
EOF

  echo "docker-compose.yml created successfully!"
  cat docker-compose.yml
}

#clear

banner
# Ask user if they want to run Docker and Docker Compose
read -p "Do you want to run Service Docker and Docker Compose? (y/n): " -r answer
if [[ $answer =~ ^[Yy]$ ]]; then
  dock
  dock_C
fi

# Ask user for project type
read -p "Project based on (node/django): " -r based

case $based in
  node)
    echo "Building Docker image based on Node.js..."
    github
    create_dockerfile_node
    build_dockerfile_node
    create_docker_compose
    ;;
  django)
    echo "Building Docker image based on Django with Python (env)..."
    github
    create_dockerfile_django
    build_dockerfile_django
    create_docker_compose
    ;;
  *)
    echo "Invalid option. Please choose 'node' or 'django'."
    continue
    # exit 1
    ;;
esac
