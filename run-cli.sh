#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

IMAGE_NAME="cgpa-cli-scraper"

echo "======================================================================="
echo "🔨 Building Standalone CLI Scraper Docker Image..."
echo "======================================================================="
docker build --no-cache -t $IMAGE_NAME .

echo ""
echo "======================================================================="
echo "🚀 Running Interactive CLI Scraper inside Docker..."
echo "======================================================================="
echo "💡 You can pass command-line arguments to this script (e.g. ./run-cli.sh --roll 20A91A1201)"
echo ""

# Cleanup function to destroy all packages/images
function cleanup {
    echo ""
    echo "======================================================================="
    echo "🧹 Cleaning up Docker packages, images, and build layers..."
    echo "======================================================================="
    
    # Remove the built image to leave zero footprint
    if docker image inspect $IMAGE_NAME >/dev/null 2>&1; then
        echo "🗑️ Removing docker image: $IMAGE_NAME"
        docker rmi -f $IMAGE_NAME
    fi
    
    # Prune docker builder cache to reclaim space completely
    echo "🧹 Pruning docker builder/build cache..."
    docker builder prune -f --filter type=exec
    
    echo "✅ Standalone run finished and all Docker footprints have been successfully cleaned up!"
}

# Register the cleanup function to run when the script exits (normally or via interrupt)
trap cleanup EXIT

# Run container and pass all arguments ($@ forwards roll/reg/start/end if provided)
docker run -it --rm $IMAGE_NAME "$@"
