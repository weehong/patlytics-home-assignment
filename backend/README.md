# Patlytics API
This API provides services to analyze the risk based on patent data and company information, offering both full analysis and suggestions for similar matches. 

It supports optional fuzzy matching to find close matches for patent IDs and company names.


## How To Use
Clone the repository the repository
```
git@github.com:weehong/patlytics-home-assignment.git
```

Change directory
```
cd backend
```

Copy the `.env.example` to `.env`
```
PORT=8000

LLM_API_KEY=

FUZZY_MATCH_THRESHOLD=80
```

Install the dependencies using PIP
```bash
pip install -r requirements.txt
```

Start the application
```
python src/run.py
```

---

## Endpoints

### 1. Analyze Patent and Company Data

**POST /api/v1/patent**

This endpoint analyzes patent and company data, using the patent ID and company name provided in the request. It can also leverage an optional fuzzy matching threshold to enhance the matching process.

#### Request

- **Body** (JSON):
    ```json
    {
        "patent_id": "string",
        "company_name": "string"
    }
    ```

- **Parameters**:
  - `patent_id` (string): The unique ID of the patent.
  - `company_name` (string): The name of the company.

#### Response

- **200 OK**:
    ```json
    {
        "message": "string",
        "data": {},
        "status": true
    }
    ```

  - `message`: A description of the analysis result.
  - `data`: The detailed result of the analysis.
  - `status`: A boolean indicating whether the analysis was successful.

- **400 Bad Request**: 
    If either `patent_id` or `company_name` is missing.
  
    ```json
    {
        "detail": "Both patent_id and company_name are required"
    }
    ```

- **500 Internal Server Error**:
    In case of an error during the analysis.
  
    ```json
    {
        "detail": "Error during analysis: <error_message>"
    }
    ```

---