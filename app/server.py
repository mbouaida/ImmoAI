from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Initialize the FastAPI application
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your data into a pandas DataFrame
df = pd.read_csv('../data/data.csv')


# Define a route for getting data for a specific town
@app.get('/api/town/{town_name}')
async def get_town(town_name: str):
    # Filter the DataFrame to only the town we're interested in
    town_data = df[df['town'] == town_name]

    # If there's no data for this town, return a 404 (Not Found)
    if town_data.empty:
        raise HTTPException(status_code=404, detail="Town not found")

    # Convert the town data into a dictionary and return it
    return town_data.to_dict(orient='records')


# Define a route for searching for towns
@app.get('/api/search')
async def search_towns(q: str):
    # Filter the DataFrame to only towns that contain the query string
    search_results = df[df['town'].str.contains(q, na=False)]

    # Convert the search results into a dictionary and return it
    return search_results.to_dict(orient='records')
