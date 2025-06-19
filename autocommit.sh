#!/bin/bash

# NLP Key Value Extractor - Git Auto Commit Script
# Usage: ./autocommit.sh "Your commit message"
# Usage: ./autocommit.sh (uses default timestamp message)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Starting auto-commit process...${NC}"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Check if there are any changes
if git diff --quiet && git diff --staged --quiet; then
    echo -e "${BLUE}ℹ️  No changes to commit${NC}"
    exit 0
fi

# Add all changes
echo -e "${BLUE}📁 Adding all changes...${NC}"
git add .

# Determine commit message
if [ -z "$1" ]; then
    # Default message with timestamp
    COMMIT_MSG="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
else
    # Use provided message
    COMMIT_MSG="$1"
fi

# Commit changes
echo -e "${BLUE}💾 Committing with message: ${GREEN}$COMMIT_MSG${NC}"
if git commit -m "$COMMIT_MSG"; then
    echo -e "${GREEN}✅ Commit successful${NC}"
else
    echo -e "${RED}❌ Commit failed${NC}"
    exit 1
fi

# Push to remote
echo -e "${BLUE}🚀 Pushing to remote repository...${NC}"
if git push; then
    echo -e "${GREEN}✅ Push successful${NC}"
    echo -e "${GREEN}🎉 Auto-commit completed successfully!${NC}"
else
    echo -e "${RED}❌ Push failed${NC}"
    echo -e "${BLUE}ℹ️  Changes are committed locally but not pushed to remote${NC}"
    exit 1
fi

# Show git status
echo -e "\n${BLUE}📊 Current git status:${NC}"
git status --short