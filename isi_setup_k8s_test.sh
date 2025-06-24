#!/bin/bash

# This script automates the entire setup and testing process.
# It will:
# 1. Clean up old environments.
# 2. Start a fresh Minikube cluster and MongoDB container.
# 3. Configure Kubernetes with the necessary resources (namespace, service account, labels).

# Exit immediately if any command fails
set -e

# --- Color Definitions for pretty printing ---
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Helper function to check for required commands ---
check_command() {
    if ! command -v $1 &> /dev/null
    then
        echo -e "${RED}ERROR: Command '$1' could not be found. Please install it before running this script.${NC}"
        exit 1
    fi
}

echo -e "${BLUE}### STEP 0: Checking for required tools... ###${NC}"
check_command minikube
check_command docker
check_command kubectl
check_command pytest
echo -e "${GREEN}All tools found.${NC}"

echo -e "\n${BLUE}### STEP 1: Cleaning up previous environments... ###${NC}"
echo "--> Deleting existing Minikube cluster (if any)..."
minikube delete || true
echo "--> Stopping and removing old MongoDB container (if any)..."
docker stop mongopiedge &> /dev/null || true
docker rm mongopiedge &> /dev/null || true
echo "--> Cleaning up pytest cache..."
rm -rf .pytest_cache
echo -e "${GREEN}Cleanup complete.${NC}"

echo -e "\n${BLUE}### STEP 2: Setting up new infrastructure... ###${NC}"
echo "--> Starting a new 3-node Minikube cluster..."
minikube start --nodes 3 --driver=docker
echo "--> Starting new MongoDB container..."
docker run --name mongopiedge -d -p 27017:27017 mongo
echo -e "${GREEN}Infrastructure is up.${NC}"

echo -e "\n${BLUE}### STEP 3: Configuring Kubernetes... ###${NC}"
echo "--> Creating 'sunrise6g' namespace..."
kubectl create namespace sunrise6g
echo "--> Creating 'sdk-user' service account..."
kubectl create serviceaccount sdk-user -n sunrise6g
echo "--> Binding 'sdk-user' to cluster-admin role..."
kubectl delete clusterrolebinding sdk-user-admin-binding &> /dev/null || true
kubectl create clusterrolebinding sdk-user-admin-binding --clusterrole=cluster-admin --serviceaccount=sunrise6g:sdk-user
echo "--> Labeling Minikube nodes..."
kubectl label node minikube location=my-local-zone node_type=edge-node --overwrite
kubectl label node minikube-m02 location=ATHENS node_type=edge-node --overwrite
kubectl label node minikube-m03 location=PATRAS node_type=edge-node --overwrite
kubectl create clusterrolebinding sdk-user-cluster-admin --clusterrole=cluster-admin --serviceaccount=sunrise6g:sdk-user
export NEW_TOKEN=$(kubectl create token sdk-user -n sunrise6g)
echo -e "${GREEN}Kubernetes configuration complete.${NC}"

echo "--> Running tests..."
pytest -v -s tests/edgecloud/test_k8s_client.py
