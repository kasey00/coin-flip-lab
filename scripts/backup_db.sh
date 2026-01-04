#!/bin/bash

# ==============================================================================
#  Docker Volume Backup Utility
#  Description: Creates a timestamped .tar.gz backup of a specific Docker volume.
#               Uses a temporary Alpine container to ensure cross-platform compatibility.
# ==============================================================================

# --- CONFIGURATION (Edit these if needed) ---
# The exact name of the volume defined in docker-compose.yml
VOLUME_NAME="coin_app_postgres_data"

# Backup directory (Default: creates a 'backups' folder in the project root)
# $(dirname "$0") gets the script's folder, .. goes up one level to project root
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/backups"

# Date format for the filename (YYYY-MM-DD)
TIMESTAMP=$(date +%F)
FILENAME="db_backup_${TIMESTAMP}.tar.gz"

# Retention: Delete files older than X days (Set to 0 to disable)
RETENTION_DAYS=7
# ==============================================================================

# 1. Setup
# Ensure the backup directory exists on the host machine
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

echo "=========================================="
echo "Starting Backup for Volume: $VOLUME_NAME"
echo "Target File: $BACKUP_DIR/$FILENAME"
echo "=========================================="

# 2. Run Backup
# We use $(pwd) logic to map the host path dynamically.
# Note: On Windows (Git Bash/WSL), standard paths usually work. 
# On pure Command Prompt, this script might need WSL or Git Bash to run.

docker run --rm \
  -v "$VOLUME_NAME":/source_data \
  -v "$BACKUP_DIR":/backup_target \
  alpine tar czf "/backup_target/$FILENAME" -C /source_data .

# 3. Validation
if [ $? -eq 0 ]; then
    echo "✅ Success! Backup created."
    
    # Check file size (Human readable)
    FILE_SIZE=$(du -h "$BACKUP_DIR/$FILENAME" | cut -f1)
    echo "   Size: $FILE_SIZE"
else
    echo "❌ Error: Backup failed. Check if Docker is running."
    exit 1
fi

# 4. Retention Policy (Cleanup)
if [ "$RETENTION_DAYS" -gt 0 ]; then
    echo "------------------------------------------"
    echo "Checking for old backups (Older than $RETENTION_DAYS days)..."
    # Find and delete
    find "$BACKUP_DIR" -name "db_backup_*.tar.gz" -mtime +$RETENTION_DAYS -print -delete
    echo "Cleanup complete."
fi

echo "=========================================="