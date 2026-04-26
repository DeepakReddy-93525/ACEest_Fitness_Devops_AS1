# Docker Hub Setup Guide

## Prerequisites
1. Docker Hub account created
2. Jenkins configured with Docker Hub credentials

## Jenkins Credentials Setup
1. Go to Jenkins Dashboard > Manage Jenkins > Manage Credentials
2. Click "Add Credentials"
3. Select "Username with password" kind
4. Enter:
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password or access token
   - **ID**: `dockerhub-credentials`
   - **Description**: `Docker Hub Registry Credentials`

## Environment Variables
Update these in your Jenkinsfile:
- `DOCKER_REGISTRY`: Set to your Docker Hub username
- `IMAGE_NAME`: Set to your desired image name (e.g., `aceest-app`)

## Verification Commands
After pipeline runs, verify with these commands:

```bash
# Pull the pushed image
docker pull your-dockerhub-username/aceest-app:latest

# Run the image
docker run -p 5000:5000 your-dockerhub-username/aceest-app:latest

# Test the application
curl http://localhost:5000/programs
```

## Image Versioning Strategy
- **Build Number**: `your-dockerhub-username/aceest-app:123`
- **Latest Tag**: `your-dockerhub-username/aceest-app:latest`
- **Rollback**: Use specific build numbers for rollback

## Expected Pipeline Output
```
Images pushed to Docker Hub:
- your-dockerhub-username/aceest-app:123
- your-dockerhub-username/aceest-app:latest
```
