#!/bin/bash

rm -rf packages/overlays/Lineage/icons/IconPack* packages/overlays/Lineage/fonts/etc/

clear

read -p "Do you want to sync with lineage? (y/n): " answer
if [ "$answer" = "y" ]; then
    export SYNC_WITH_LINEAGE=true
    echo "SYNC_WITH_LINEAGE is set to true"
else
    echo "SYNC_WITH_LINEAGE not set"
fi


# Check for root
if [ "$(id -u)" -eq "0" ]; then
    echo "Do not run this script as root. Please run as a regular user."
    exit 1
fi

if [ "$SYNC_WITH_LINEAGE" == "true" ]; then
    echo "Syncing with LineageOS source"

    # Repo initialization
    repo init -u https://github.com/lineage-vayu/android.git -b lineage-22.2 --git-lfs --depth=1
    if [ $? -ne 0 ]; then
        echo "Repo init failed, but continuing with the build process"
    fi

    # Sync the repo
    repo sync -j16 --force-sync
    if [ $? -ne 0 ]; then
        echo "Repo sync failed, but continuing with the build process"
    fi
else
    echo "SYNC_WITH_LINEAGE is not set to true, skipping repo init and sync. Continuing with the build process"
fi

# Define the device
DEVICE="vayu"
WORK_DIR=$(pwd)

if [ "$BUILDING_FROM_SCRATCH" = true ]; then
    WORK_DIR=$HOME/lineage
    mkdir -p "$WORK_DIR"
    cd "$WORK_DIR"
fi

export KBUILD_BUILD_USER=grepfox 
export KBUILD_BUILD_HOST=home
export BUILD_USERNAME=grepfox
export BUILD_HOSTNAME=home


#  Set up ccache
echo "Setting up ccache."
export USE_CCACHE=1
export CCACHE_DIR="$WORK_DIR/.ccache"
export CCACHE_MAXSIZE=20G
ccache -M 20G

# Set up the environment for the build
echo "Setting up the environment"
source build/envsetup.sh

# Choose the build target for LineageOS
read -p "Do you want to build the ROM? (y/n) (yes for rom / n for kernel): " build_reponse
if [ "$build_reponse" = "y" ]; then
    echo "Building the LineageOS ROM using brunch for $DEVICE"
    brunch "$DEVICE"
    bash sign.sh
else
    echo "Building Kernel"
    breakfast "$DEVICE"
    m bootimage dtboimage
fi

