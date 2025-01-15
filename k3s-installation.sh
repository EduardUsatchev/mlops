#!/bin/bash

# Function to install K3s using Multipass
install_k3s_with_multipass() {
    echo "Installing K3s using Multipass..."

    # Install Multipass if not already installed
    if ! command -v multipass &> /dev/null; then
        echo "Multipass not found. Installing it via Homebrew..."
        brew install multipass
    fi

    # Launch an Ubuntu VM with 3 GB memory and 10 GB disk
    echo "Launching Ubuntu VM with Multipass..."
    multipass launch --name k3s-vm --mem 3G --disk 10G

    # Shell into the VM and install K3s
    echo "Shelling into the VM to install K3s..."
    multipass exec k3s-vm -- bash -c "
        curl -sfL https://get.k3s.io | sh -
        echo 'K3s installed successfully.'
    "

    echo "Fetching K3s node status..."
    multipass exec k3s-vm -- kubectl get nodes
}

# Function to copy and configure kubeconfig file
configure_kubeconfig() {
    echo "Copying kubeconfig file from VM to local machine..."

    # Copy the kubeconfig file from the VM to the current directory
    multipass transfer k3s-vm:/etc/rancher/k3s/k3s.yaml ./k3s.yaml

    # Get the IP address of the Multipass VM
    VM_IP=$(multipass info k3s-vm | grep IPv4 | awk '{print $2}')
    echo "VM IP address: $VM_IP"

    # Replace localhost with the VM's IP address in the kubeconfig file
    sed -i '' "s/127.0.0.1/$VM_IP/" ./k3s.yaml
    echo "Kubeconfig file updated with VM IP address."

    # Export KUBECONFIG environment variable
    export KUBECONFIG=$(pwd)/k3s.yaml
    echo "KUBECONFIG environment variable set to $(pwd)/k3s.yaml"

    # Verify the connection to the K3s cluster
    echo "Verifying connection to K3s cluster..."
    kubectl get nodes
}

# Main script logic
echo "Starting K3s installation and configuration process..."
install_k3s_with_multipass
configure_kubeconfig
echo "K3s installation and configuration completed successfully!"
