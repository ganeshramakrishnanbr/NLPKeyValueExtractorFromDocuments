#!/bin/bash

# Quick commit script - shorter version
# Usage: ./quick-commit.sh "message" or qc "message" (after alias setup)

if [ -z "$1" ]; then
    echo "Usage: ./quick-commit.sh \"Your commit message\""
    exit 1
fi

git add . && git commit -m "$1" && git push

if [ $? -eq 0 ]; then
    echo "✅ Successfully committed and pushed: $1"
else
    echo "❌ Commit/push failed"
fi