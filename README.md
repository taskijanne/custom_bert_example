# How to run the Python + Node application

## Backend
1. Clone the repository
2. Install dependencies:

pip install fastapi uvicorn python-dotenv requests transformers torch

3. .Add .env file and "APIKEY" -variable to the file APIKEY=yourapikeyhere
(If you don't have apikey, get one from Groq)

4. Start backend app:
uvicorn main:app --reload

5. WAIT for the custom model to be loaded from Huggingface. Once you see  "INFO:     Application startup complete." -line in the console, you are good to go

## Frontend

1. Install prerequisites

Node.JS 

2. Go to "ui" folder

3. run npm install

4. run npm start

5. Open browser in localhost:3000 (if it doesn't open automatically)

# How to use the API

Endpoint: http://127.0.0.1:8000/analyze
Method: POST

Body:

* text: Text you want to translate
* model: "custom" or "llama"

Example body:

{
  "text": "I like this application a lot",
  "model": "custom"
}

# How to run notebook

1. Go to google colab: https://colab.research.google.com/
2. Import the notebook
3. Connect to local or hosted environment