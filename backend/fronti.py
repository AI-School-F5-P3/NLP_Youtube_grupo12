import os
import shutil

# Define the root directory for the project
project_root = "c:/Users/busin/Desktop/new_you_db/frontend_project"

# Ensure the root directory is clean
if os.path.exists(project_root):
    shutil.rmtree(project_root)
os.makedirs(project_root)

# Define the structure
structure = {
    "public": ["favicon.ico", "index.html"],
    "src": {
        "components": ["Sidebar.tsx", "Footer.tsx", "Header.tsx", "Carousel.tsx", "RealTimeTracker.tsx"],
        "pages": ["HomePage.tsx", "VideoAnalyzer.tsx", "AnalyticsPage.tsx"],
        "services": ["apiService.ts", "websocketService.ts"],
        "styles": ["index.css"],
        "App.tsx": "",
        "index.tsx": "",
    },
    "root_files": ["package.json", "tsconfig.json", "tailwind.config.js"],
}

# Populate the structure
for folder, contents in structure.items():
    if folder == "root_files":
        # Create files in the root directory
        for file in contents:
            with open(os.path.join(project_root, file), "w") as f:
                f.write(f"// {file} placeholder")
    else:
        folder_path = os.path.join(project_root, folder)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(contents, dict):
            # Nested structure
            for subfolder, subcontents in contents.items():
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                for file in subcontents:
                    with open(os.path.join(subfolder_path, file), "w") as f:
                        f.write(f"// {file} placeholder")
        else:
            # Files in the folder
            for file in contents:
                with open(os.path.join(folder_path, file), "w") as f:
                    f.write(f"// {file} placeholder")

# Provide the user with the path to download or verify the structure
project_root
