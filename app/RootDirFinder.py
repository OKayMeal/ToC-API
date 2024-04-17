import os

class RootDirFinder:
    """Small util class that determines the project root dir"""
    # current file path
    currentFilePath = os.path.dirname(os.path.abspath(__file__))
    
    def find_project_root(self, currentPath):
        root_marker = '.git'
        while currentPath != os.path.dirname(currentPath):  # stop when the root of the filesystem is reached
            if root_marker in os.listdir(currentPath):
                return currentPath
            currentPath = os.path.dirname(currentPath)
        return currentPath  # fallback to current path if nothing is found

    