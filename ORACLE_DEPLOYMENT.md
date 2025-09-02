# 🚀 Oracle Cloud Deployment Guide

This guide will help you deploy your Collatz Conjecture app to Oracle Cloud Infrastructure using GitHub Actions.

## 📋 Prerequisites

1. **Oracle Cloud Account** (Free Tier available)
2. **GitHub Repository** with your code
3. **Docker** installed locally for testing
4. **Oracle Cloud CLI** (optional, for manual deployment)

## 🏗️ Deployment Options

### Option 1: Oracle Container Engine for Kubernetes (OKE)
- **Best for**: Production, scalability
- **Complexity**: High
- **Cost**: Pay-as-you-use

### Option 2: Oracle Cloud Infrastructure Compute (VM)
- **Best for**: Simple deployment, full control
- **Complexity**: Medium
- **Cost**: Free tier eligible

### Option 3: Oracle Functions (Serverless)
- **Best for**: Event-driven, lightweight
- **Complexity**: Medium
- **Cost**: Free tier eligible

## 🐳 Docker Deployment (Recommended)

### 1. Test Locally
```bash
# Build the image
docker build -t collatz-conjecture .

# Run locally
docker run -p 8000:8000 collatz-conjecture

# Test with docker-compose
docker-compose up
```

### 2. Push to Oracle Container Registry
```bash
# Login to Oracle Container Registry
docker login <region>.ocir.io

# Tag your image
docker tag collatz-conjecture:latest <region>.ocir.io/<tenancy>/<repo>/collatz-conjecture:latest

# Push to registry
docker push <region>.ocir.io/<tenancy>/<repo>/collatz-conjecture:latest
```

## ☁️ Oracle Cloud Infrastructure Setup

### 1. Create Compute Instance
- **Shape**: VM.Standard.A1.Flex (ARM-based, free tier eligible)
- **OS**: Oracle Linux 8 or Ubuntu 20.04
- **Memory**: 6GB RAM
- **Storage**: 50GB boot volume

### 2. Configure Security Lists
- **Port 22**: SSH access
- **Port 8000**: Flask application
- **Port 80/443**: HTTP/HTTPS (optional)

### 3. Install Dependencies
```bash
# Update system
sudo yum update -y  # Oracle Linux
# or
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Docker
sudo yum install -y docker  # Oracle Linux
# or
sudo apt install -y docker.io  # Ubuntu

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

### 4. Deploy Application
```bash
# Pull your image
docker pull <region>.ocir.io/<tenancy>/<repo>/collatz-conjecture:latest

# Run the application
docker run -d \
  --name collatz-app \
  -p 8000:8000 \
  --restart unless-stopped \
  <region>.ocir.io/<tenancy>/<repo>/collatz-conjecture:latest
```

## 🔄 GitHub Actions Automation

The `.github/workflows/deploy-oracle.yml` file provides a template for automated deployment.

### Customize the Workflow:
1. **Add Oracle Cloud credentials** as GitHub secrets
2. **Configure your specific Oracle Cloud region** and tenancy
3. **Add deployment steps** for your chosen method

### Required Secrets:
- `ORACLE_USER_OCID`
- `ORACLE_TENANCY_OCID`
- `ORACLE_FINGERPRINT`
- `ORACLE_PRIVATE_KEY`
- `ORACLE_REGION`

## 📊 Monitoring & Maintenance

### Health Checks
- **Endpoint**: `/api/health`
- **Docker healthcheck**: Built into the container
- **Load balancer**: Configure for high availability

### Logs
```bash
# View application logs
docker logs collatz-app

# Follow logs in real-time
docker logs -f collatz-app
```

### Updates
```bash
# Pull latest image
docker pull <region>.ocir.io/<tenancy>/<repo>/collatz-conjecture:latest

# Stop current container
docker stop collatz-app

# Remove old container
docker rm collatz-app

# Start new container
docker run -d \
  --name collatz-app \
  -p 8000:8000 \
  --restart unless-stopped \
  <region>.ocir.io/<tenancy>/<repo>/collatz-conjecture:latest
```

## 💰 Cost Optimization

### Free Tier Benefits:
- **2 AMD-based Compute VMs** with 1/8 OCPU and 1 GB memory each
- **4 ARM-based Compute VMs** with 1/24 OCPU and 1 GB memory each
- **200 GB total storage**
- **10 TB data transfer**

### Recommendations:
- Use ARM-based VMs (VM.Standard.A1.Flex) for better free tier utilization
- Monitor usage in Oracle Cloud Console
- Set up billing alerts

## 🚨 Troubleshooting

### Common Issues:
1. **Port not accessible**: Check security lists and firewall rules
2. **Container won't start**: Check logs with `docker logs`
3. **Memory issues**: Adjust VM shape if needed
4. **Network connectivity**: Verify VCN and subnet configuration

### Debug Commands:
```bash
# Check container status
docker ps -a

# Inspect container
docker inspect collatz-app

# Execute commands in container
docker exec -it collatz-app /bin/bash

# Check system resources
docker stats collatz-app
```

## 🔗 Useful Links

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [Oracle Cloud Documentation](https://docs.oracle.com/en-us/iaas/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Next Steps**: Test the Docker build locally, then choose your preferred Oracle Cloud deployment method and customize the GitHub Actions workflow accordingly.
