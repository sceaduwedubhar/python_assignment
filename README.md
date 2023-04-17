# Take-Home Assignment

- [Take-Home Assignment](#take-home-assignment)
  - [Dependencies](#dependencies)
  - [Get Started](#get-started)
    - [Create a docker container](#create-a-docker-container)
    - [Migrate database](#migrate-database)
      - [Access docker container](#access-docker-container)
      - [Create financial\_data table in database](#create-financial_data-table-in-database)
    - [Retrieve data from AlphaVantage](#retrieve-data-from-alphavantage)
      - [Access docker container](#access-docker-container-1)
      - [Retrieve data](#retrieve-data)
  - [REST API](#rest-api)
    - [Get financial\_data](#get-financial_data)
      - [Sample Request](#sample-request)
      - [Parameter](#parameter)
      - [Reponse](#reponse)
    - [Get financial\_data](#get-financial_data-1)
      - [Sample Request](#sample-request-1)
      - [Parameter](#parameter-1)
      - [Reponse](#reponse-1)
  - [API KEY of free API provider AlphaVantage](#api-key-of-free-api-provider-alphavantage)


## Dependencies
- Python >= 3.10
- fastapi
  - high performance, easy to learn, fast backend framework 
- uvicorn
  - ASGI web server
- requests
  - request data from [AlphaVantage](https://www.alphavantage.co/documentation/) API
- sqlalchemy
  - ORM library, used for communicating with database
- psycopg2-binary
  - PostgreSQL database adapter
- python-dotenv
  - read key-value pairs from a ```.env``` file 

## Get Started
### Create a docker container
```
docker compose up --build
```

### Migrate database
#### Access docker container 
```
docker exec -it <container-id> bash
```
#### Create financial_data table in database
```
python model.py
```

### Retrieve data from [AlphaVantage](https://www.alphavantage.co/documentation/)
#### Access docker container 
```
docker exec -it <container-id> bash
```
#### Retrieve data
```
python get_raw_data.py
```

## REST API

### Get financial_data

#### Sample Request

```
GET http://localhost:8000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2
```

#### Parameter

| Parameter    | Required | default |                    Description                    |
| :----------- | :------: | :-----: | :-----------------------------------------------: |
| `start_date` |   :x:    |    -    |            start date e.g. 2023-04-01             |
| `end_date`   |   :x:    |    -    |             end date e.g. 2023-04-15              |
| `symbol`     |   :x:    |    -    |          symbol of stock e.g. IBM, AAPL           |
| `limit`      |   :x:    |    5    | limit of records can be retrieved for single page |
| `page`       |   :x:    |    1    |                current page index                 |

#### Reponse

```
{
    "data": [
        {
            "symbol": "IBM",
            "date": "2023-01-05",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "62199013",
        },
        {
            "symbol": "IBM",
            "date": "2023-01-06",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "59099013"
        },
        {
            "symbol": "IBM",
            "date": "2023-01-09",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "42399013"
        }
    ],
    "pagination": {
        "count": 20,
        "page": 2,
        "limit": 3,
        "pages": 7
    },
    "info": {'error': ''}
}
```

### Get financial_data

#### Sample Request

```
GET http://localhost:8000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM
```

#### Parameter

| Parameter    |      Required      | default |          Description           |
| :----------- | :----------------: | :-----: | :----------------------------: |
| `start_date` | :heavy_check_mark: |    -    |   start date e.g. 2023-04-01   |
| `end_date`   | :heavy_check_mark: |    -    |    end date e.g. 2023-04-15    |
| `symbol`     | :heavy_check_mark: |    -    | symbol of stock e.g. IBM, AAPL |

#### Reponse

```
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "symbol": "IBM",
        "average_daily_open_price": 123.45,
        "average_daily_close_price": 234.56,
        "average_daily_volume": 1000000
    },
    "info": {'error': ''}
}
```

## API KEY of free API provider [AlphaVantage](https://www.alphavantage.co/documentation/)

API Key should be stored in ```.env``` file with key name **APIKEY**.

You can update the **APIKEY** in ```.env``` file for local development and production environment separately.

In actual practice, ```.env``` file should be excluded in version control. You may add ```.env``` to ```.gitignore``` file.