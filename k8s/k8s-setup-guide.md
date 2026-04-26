# Kubernetes Deployment Setup Guide

## Prerequisites
- Minikube installed and running
- kubectl configured
- Docker Hub image available

## Quick Start Commands

```bash
# Start Minikube
minikube start

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Create namespace
kubectl apply -f namespace.yaml

# Deploy all strategies
kubectl apply -f rolling-update-deployment.yaml
kubectl apply -f blue-green-deployment.yaml
kubectl apply -f canary-deployment.yaml
kubectl apply -f shadow-deployment.yaml
kubectl apply -f ab-testing-deployment.yaml
kubectl apply -f deployment-scripts.yaml
```

## Deployment Strategies Overview

### 1. Rolling Update (Default)
```bash
# Deploy
kubectl apply -f rolling-update-deployment.yaml

# Update with new image
kubectl set image deployment/aceest-app-rolling aceest-app=tdeepakreddy/aceest-app:new-version -n aceest-fitness

# Monitor rollout
kubectl rollout status deployment/aceest-app-rolling -n aceest-fitness

# Rollback
kubectl rollout undo deployment/aceest-app-rolling -n aceest-fitness
```

### 2. Blue-Green Deployment
```bash
# Deploy both environments
kubectl apply -f blue-green-deployment.yaml

# Switch from blue to green
kubectl patch service aceest-app-main-service -p '{"spec":{"selector":{"version":"green"}}}' -n aceest-fitness

# Switch back to blue
kubectl patch service aceest-app-main-service -p '{"spec":{"selector":{"version":"blue"}}}' -n aceest-fitness
```

### 3. Canary Release
```bash
# Deploy stable and canary
kubectl apply -f canary-deployment.yaml

# Update canary with new version
kubectl set image deployment/aceest-app-canary aceest-app=tdeepakreddy/aceest-app:new-version -n aceest-fitness

# Increase canary traffic (scale up)
kubectl scale deployment aceest-app-canary --replicas=2 -n aceest-fitness
```

### 4. Shadow Deployment
```bash
# Deploy production and shadow
kubectl apply -f shadow-deployment.yaml

# Update shadow with new version
kubectl set image deployment/aceest-app-shadow aceest-app=tdeepakreddy/aceest-app:new-version -n aceest-fitness

# Monitor shadow logs
kubectl logs -f deployment/aceest-app-shadow -n aceest-fitness
```

### 5. A/B Testing
```bash
# Deploy both versions
kubectl apply -f ab-testing-deployment.yaml

# Update version B
kubectl set image deployment/aceest-app-version-b aceest-app=tdeepakreddy/aceest-app:new-version -n aceest-fitness

# Adjust traffic split (via Ingress annotation)
kubectl annotate ingress aceest-app-ab-testing nginx.ingress.kubernetes.io/canary-weight="30" -n aceest-fitness
```

## Monitoring and Verification

```bash
# Check all deployments
kubectl get deployments -n aceest-fitness

# Check services
kubectl get services -n aceest-fitness

# Check pods
kubectl get pods -n aceest-fitness

# Get service URLs
minikube service aceest-app-rolling-service -n aceest-fitness --url

# Port forward for local testing
kubectl port-forward service/aceest-app-rolling-service 8080:80 -n aceest-fitness
```

## Cleanup

```bash
# Delete all resources
kubectl delete namespace aceest-fitness

# Stop Minikube
minikube stop
```
