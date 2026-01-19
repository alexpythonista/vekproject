## Recommendation API Service
A microservice for providing personalized product recommendations based on user interaction history.
## Description
This REST API provides personalized product recommendations:
- For existing users: top-5 products they were most interested in (excluding purchased items)
- For new users: top-5 most popular products across all data
- Constraint: no more than 2 products from the same brand in recommendations
## Features
- Personalized recommendations based on user history
- Fallback to popular items for new users
- Brand diversity constraint (max 2 per brand)
- Docker support
## Recommendation Algorithm
### For Existing Users:
1.	Filter data by user_id
2.	Exclude products that were purchased
3.	Group by brand, keeping max 2 products per brand
4.	Sort by interaction weight: purchases → cart additions → clicks
5.	Return top-5 products
### For New Users:
1.	Use all available data
2.	Group by brand, keeping max 2 products per brand
3.	Sort by popularity: purchases → cart additions → clicks
4.	Return top-5 products
## Project Structure
```
vekproject/
├── data/
│   └── test.csv            # Sample data file
├── constants.py            # Constants and enums
├── services.py             # Business logic and data processing
├── main.py                 # FastAPI application
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
└── .gitignore              # Git ignore rules
```
### Path to test data
Path to test CSV and its name can be changed [HERE](https://github.com/alexpythonista/vekproject/blob/f7a1000a4e4acc005570cff771df41bb5989f038/services.py#L7)
- CSV-data file was intentionally not added to the repo.
## Technology Stack
- Python 3.14
- FastAPI
- Pandas
- Docker
## Getting Started
Prerequisites
- Python 3.14+ or Docker
## Run the project
### Either Docker
```
docker build -t fastapi-app .
```
```
docker run -p 8000:8000 fastapi-app
```
### Or main.py
Enable by uncommenting [HERE](https://github.com/alexpythonista/vekproject/blob/f7a1000a4e4acc005570cff771df41bb5989f038/main.py#L22-L24)
## API Documentation
Once running, access:
- API: ```http://localhost:8000```
- Interactive Docs: ```http://localhost:8000/docs```
### API Endpoint
```GET /recommendations/{user_id}```
### Parameters
```user_id (integer, required)```: User ID to get recommendations for
### Response
```
{
  "uid": 173,
  "products": [10875, 11952, 11510, 10873, 10370]
}
```
# ANSWERS
## 1. Why This Solution Structure
### Architecture decisions:
- FastAPI for high performance, async capabilities, automatic OpenAPI docs, and built-in validation
- Layered separation: ```constants``` (config), ```services``` (business logic), ```main``` (API layer) - clean separation of concerns
- Pandas for CSV processing: Optimal for prototyping with vectorized operations and easy grouping/sorting
- Dockerization: For reproducibility and easy deployment
### Algorithmic choices:
- Weighted interaction scoring: ```purchase``` > ```add_to_cart``` > ```click``` logical hierarchy
- Brand diversity via ```nlargest(2)```: Elegant Pandas solution to limit brand representation
## 2. Solution Limitations
### Performance bottlenecks:
- Entire CSV loaded in memory per request - unsustainable with large datasets
- No caching - repeated requests for same user recompute everything
- ```O(n log n)``` complexity from sorting - scales poorly with data growth
### Functional constraints:
- Static equal weights - cannot weight purchases 10x more valuable than clicks
### Architectural issues:
- CSV-based storage - not production-ready, no concurrent access
- Blocking operations - no async data processing
- No real-time updates - static file requires manual updates
## 3. Improvements for User Base Growth
- Add Redis caching with TTL for recommendations
- Implement background job to pre-compute popular items
- Use ```async``` FastAPI endpoints
- Implement chunked processing for large datasets
- Replace sorting with scoring function with configurable weights
- Microservices architecture: separate API, recommendation engine, and data layers
- Implement vector embeddings and ML models (```Word2Vec```, ```collaborative filtering```)
- Add real-time streaming pipeline (```Kafka```) for immediate recommendation updates
- Implement online learning for continuous model improvement
