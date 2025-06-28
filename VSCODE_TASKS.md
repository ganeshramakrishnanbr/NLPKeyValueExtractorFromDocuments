# NLP Key-Value Extractor

## Using VS Code Tasks

This project includes VS Code tasks that simplify running and testing the application. To use them:

1. Open the Command Palette (`Ctrl+Shift+P`)
2. Type "Tasks: Run Task" and select it
3. Choose one of the following tasks:

### Application Tasks

- **Launch NLP Key-Value Extractor**: Launches both backend and frontend in separate windows
- **Launch Backend Only**: Starts only the FastAPI backend
- **Launch Frontend Only**: Starts only the Django frontend

### Testing & Diagnostics

- **Run Network Diagnostics**: Checks port availability and network connectivity
- **Run Standalone Extractor**: Processes a document of your choice with the extractor
- **Process Markdown with Extractor**: Extracts data from the sample markdown file

## Debugging

You can also debug the application using VS Code's built-in debugger:

1. Open the Run and Debug panel (`Ctrl+Shift+D`)
2. Select one of the debug configurations:
   - **Debug Backend (FastAPI)**: Debug the FastAPI backend
   - **Debug Frontend (Django)**: Debug the Django frontend
   - **Debug Backend & Frontend**: Debug both components together
   - **Debug Standalone Extractor**: Debug the standalone extraction tool
   - **Debug Network Diagnostics**: Debug the network diagnostics tool

## Troubleshooting

If you encounter issues with the application starting:

1. Try running the **Run Network Diagnostics** task to check port availability
2. Check that all Python dependencies are installed
3. Try running each component separately
4. If server components fail, use the standalone extractor for document processing

## File Processing

The application supports various file types:

- **Text Files (.txt)**: Basic text documents
- **Markdown Files (.md)**: Documents in Markdown format
- **PDF Documents**: Coming soon with LayoutLM

## Developer Notes

- The main application components are in the `frontend` and `backend` directories
- The `standalone_extractor.py` provides functionality without requiring servers
- LayoutLM integration is available for advanced document understanding with layout awareness
