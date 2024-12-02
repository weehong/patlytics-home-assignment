# Patlytics - Patent Infringement Checker

Patlytics is a web application designed to analyze the relevance and potential for patent infringement based on provided datasets. It leverages Large Language Models (LLM) to evaluate patents and company data, making it easier for users to identify possible patent infringements.

Users can access the application via [Patlytics Web App](https://patlytics.thedecoder.net), where they can input the **patent ID** and **company name** to receive a detailed analysis. After the analysis is done, users can download the results in PDF format for later use.

## Reference

This project references the GitHub project by [Ylieo816](https://github.com/Ylieo816?tab=repositories) for the LLM portion of the application.

## Features

- **Patent Infringement Analysis**: Evaluate the relevance and potential of patent infringement based on patent IDs and company names.
- **PDF Reports**: Generate downloadable PDF reports of the analysis for later reference.
- **Fast Development and Build**: Powered by **Vite** for fast build and development workflows.
- **Responsive UI**: Built with **React** and styled using **Tailwind CSS** for a seamless and modern user experience.
- **LLM-powered Insights**: Large Language Models (LLM) are used to provide deep insights into patent data.

---

## How to Use

### 1. Clone the Repository

Start by cloning the project repository to your local machine.

```bash
git clone git@github.com:weehong/patlytics-home-assignment.git
```

### 2. Set Up Environment Variables

Copy the `.env.example` file to `.env` and set the appropriate environment variables.

```bash
cp .env.example .env
```

Edit the `.env` file with the following configurations:

```env
FRONTEND_API_URL=http://localhost
FRONTEND_PORT=5173

BACKEND_URL=http://localhost
BACKEND_PORT=8000

LLM_API_KEY=your_llm_api_key_here
```

- `FRONTEND_API_URL`: URL for the frontend (defaults to `http://localhost`).
- `FRONTEND_PORT`: Port for the frontend (defaults to `5173`).
- `BACKEND_URL`: URL for the backend (defaults to `http://localhost`).
- `BACKEND_PORT`: Port for the backend (defaults to `8000`).
- `LLM_API_KEY`: API key for accessing the Large Language Model service.

### 3. Start the Services with Docker

To set up the backend and other services, run the following Docker command:

```bash
docker compose up -d
```

This will start the backend services, including the application server and any required databases.

### 4. Run the Frontend Locally

Once the services are up and running, you can access the frontend at `http://localhost:5173`.

### 5. Access the Backend Locally

The backend is hosted on `http://localhost:8000`. You can interact with the backend directly or use the frontend interface to send requests to the backend.

---

## User Flow

1. **Input Patent ID and Company Name**: On the homepage of the Patlytics web app, enter the **patent ID** and **company name** you want to analyze.
   
2. **Submit the Data**: Click the button to submit your data to the backend. The backend will process the request, using LLM to analyze the patent and company data.

3. **Download PDF Report**: Once the analysis is complete, a downloadable PDF report will be generated. You can save this report for later use.

---

## API Endpoints

### 1. **Analyze Patent and Company Data**

- **URL**: `POST /api/v1/patent`
- **Description**: Analyzes the provided patent ID and company name to check for potential infringements and relevance.
- **Request Body**: 
    ```json
    {
        "patent_id": "string",
        "company_name": "string"
    }
    ```

- **Response**:
    - Success:
    ```json
    {
        "message": "Analysis completed",
        "data": { "analysis_result": {...} },
        "status": true
    }
    ```

    - Error (e.g., Missing parameters):
    ```json
    {
        "detail": "Both patent_id and company_name are required"
    }
    ```

## Credits

- **React**: A JavaScript library for building user interfaces.
- **Vite**: A fast and modern build tool.
- **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
- **React Hook Form**: A library for easy form handling in React.
- **React PDF Renderer**: A library for rendering PDF documents in React.

For more information, visit the official documentation of these libraries.

---