# Linux Command Manual Generator

A comprehensive Python and Bash-based automation tool for generating, verifying, and managing 20 Linux/Unix command documentation with intelligent command recommendations.

## 📋 Overview

This project automates the creation of comprehensive system manuals for Linux/Unix commands. It provides two implementations:
- **Python version** (`main.py`): Object-oriented approach with XML serialization
- **Bash version** (`finalproj_jenin.sh`): Shell scripting implementation with text-based output

Both implementations generate structured documentation including command descriptions, version history, usage examples, and related commands.

## ✨ Features

### 1. Automated Manual Generation
- Extracts command descriptions from man pages
- Retrieves version information using multiple methods
- Generates practical usage examples
- Identifies related commands automatically
- Creates structured documentation (XML for Python, formatted text for Bash)

### 2. Verification System
- Validates generated documentation accuracy
- Compares manual versions to detect changes
- Ensures consistency across documentation
- Supports selective verification (all commands or specific commands)

### 3. Command Recommendation System
- Suggests functionally related commands
- Pattern-based command discovery using `compgen`
- Context-aware recommendations based on command purpose
- Helps users discover alternative or complementary tools

### 4. Search Functionality
- Quick command lookup from generated manuals
- Browse all documented commands
- Display comprehensive command information
- Easy navigation through documentation

## 📁 Project Structure
