# density
Deployed on serverlessly on AWS Lambda.  Uses DynamoDB as it's data layer to consume heartbeats from sensors.  Backend is Django & Frontend is Angular

# Heartbeat Emulation
| Variable         | Type      | Value                                                                                                                     |
|------------------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| -s               | String    | sensor id                                                                                                                 |
| -u               | String    | domain/url to the api                                                                                                     |
| -c               | String    | Number of seconds you want to beat                                                                                        |
| --offline        | String    | (OPTIONAL) Sends sensor status offline                                                                                               |


- Run the script `heartbeat.py` under `scripts`
    - `cd scripts`    
    - ex:
        - `python heartbeat.py -s ec76f3a15afe49ac8808e7181957f5c8 -u http://localhost:8000 -c 10 `
        - `python heartbeat.py -s ec76f3a15afe49ac8808e7181957f5c8 -u http://localhost:8000 -c 10 --offline`
        - `python heartbeat.py -s sensor1 -u https://yk1tae0nwe.execute-api.us-east-1.amazonaws.com/dev -c 10`

# Application - Local
### DynamoDB 
- `cd backend`
- `sls deploy -s dev`

### Backend
- `cd backend`
- `pip install -r requirments.txt`
- `python manage.py runserver --service.settings.dev`

### Frontend
- `cd frontend`
- `npm i`
- `npm start`


# Application - Deployment
### DynamoDB 
- `cd backend`
- `sls deploy -s dev`

### Backend
- `cd backend`
-  Build virtual env & activate
- `pip -r install requirements.txt`
- `cd service`
- `zappa init`
- Under `zappa_settings.json`
    - Set environment variables `dynamoSensorsTable` & `dynamoHeartbeatsTable` based on the Tables generated.
    - Set `cors` to `true` 
-  `zappa deploy`
-  Go into API gateway and get the URL for the backend for the frontend

### Frontend
-  Make sure the backend URL is set in the settings via a script or manually
- `npm build`
- Upload to amazon S3 bucket - static site hosting


### TODO
- Use Websockets instead of polling on the frontend
    - Also good for alerting users when a sensor hasn't beat in a while.  Could also just hack it out on the FE
- Add better UI w/ filtering sorting 
- Add DyanmoDB hooks to add data to an Elasticsearch node to allow search capabilities on the unstructured metadata
