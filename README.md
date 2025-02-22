# TubeChef

TubeChef is a streamlined script that automates the creation of recipes by searching YouTube for cooking videos, extracting transcripts, generating concise recipes with an LLM, and uploading them to Notion.

---

## Overview

TubeChef integrates with multiple APIs to provide a seamless workflow for food enthusiasts:
- **YouTube Integration:** Searches for cooking videos based on your desired dish.
- **Transcript Extraction:** Retrieves video transcripts for recipe analysis.
- **Recipe Generation:** Uses a Gemini LLM to extract the best, easy-to-follow recipe (under 2000 characters) focusing on minimal cooking time and simplicity.
- **Notion Upload:** Automatically creates a Notion page with the generated recipe, titled with the current date and dish name.

---

## Features

- **YouTube Video Search:** Fetches relevant cooking videos using the YouTube API.
- **Transcript Processing:** Extracts and compiles video transcripts for analysis.
- **Recipe Selection:** Compares multiple transcripts to choose the clearest, simplest recipe.
- **Automated Notion Page Creation:** Publishes the final recipe to a Notion page with a formatted title.
- **Easy Setup:** A setup script creates a virtual environment, installs dependencies, and configures environment variables.

---

## Requirements

- **Python 3.x**
- **API Keys:**
  - YouTube API Key
  - Notion API Key & Notion Page ID

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Run the Setup Script:**
   ```bash
   ./setup.sh
   ```
   This script will:
   - Create a Python virtual environment.
   - Install dependencies from `requirements.txt`.
   - Copy `.env.example` to `.env` (or create a new `.env` if not found).
   - Configure the necessary Composio tools for YouTube and Notion integrations.

---

## Configuration

Before running TubeChef, update the `.env` file with your API credentials:

```dotenv
GOOGLE_API_KEY=your_youtube_api_key
NOTION_API_KEY=your_notion_api_key
NOTION_PAGE_ID=your_notion_page_id
```

---

## Usage

1. **Activate the Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Main Script:**
   ```bash
   python script.py
   ```

3. **Follow the Prompt:**
   - Enter the name of the dish you want to cook.
   - TubeChef will search YouTube for relevant videos, extract transcripts, generate a concise recipe, and create a Notion page with the final recipe.

## Contributing

Contributions, suggestions, and bug reports are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

Happy cooking and coding with TubeChef!
