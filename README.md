# Medical QA System

An interactive medical question answering system with self-consistency and abstention capabilities.

## Installation

1. Clone the repository or navigate to the `medical-qa-system` directory.

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Setup

1. Set up MongoDB:
   - Ensure MongoDB is running locally or provide a connection URI.

2. Create a `.env` file in the root directory with the following variables:
   ```
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=medical_qa
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Replace `your_gemini_api_key_here` with your actual Google Gemini API key.

## Running the Application

1. Ensure the virtual environment is activated.

2. Run the application:
   ```
   python -m app.main
   ```

   The API will be available at `http://localhost:8000`.

3. To access the API documentation, visit `http://localhost:8000/docs` in your browser.