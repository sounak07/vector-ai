# Vector 

## To start build the images and start the server 

``` bash
docker-compose up --build --remove-orphans
```

[Open API Spec for the service](http://localhost:8080/docs)

[Flower (An analytics tool for celery)](http://localhost:5555/dashboard)

[Rabbit MQ Management](http://localhost:15672/#/)

`Note: Services will only work once you start the server!`

## Architecture

![alt text](/img//architecture.jpeg "arch")

- The application consists of Read and write APIs. Read APIs are in Sync as I felt it gives a better user experience and since I'm doing the writes async , at scale our application should be able to manage and serve requests efficiently. Write APIs are being managed via a message broker. Here I have used celery with Rabbitmq.

- All the GET APIs of our application are Sync in nature. But the writes of any kind are happening async. I have not used the event loop architecture that fast API offers since all my heavy duty writes are already being done async. Being sync should not really effect the overall performance of my APIs as fast API will be running the Sync tasks in separate threads.

- For all the writes which are async via task queue, i wanted to give a better user experience so i added all kinds of validation checks before adding it to the task queue so that the user knows before-hand what Invalidations they are doing which and would ensure that the task doesn't fail due the invalid/incorrect data.


## DB Design

We will be using Postgres as our main datastore for our application. Reason for choosing an SQL db is definetly efficient processing of queries. Data is more organised, structured and relational. I wanted to build more organised relationships between the tables since i feel it would easier to scale for this use case. Also since I'm doing the READS in sync and SQL will be able to do it more efficiently and easily. We might have the need of joining data across tables for additional features in future and SQL makes it easier to perform complex queries against structured data, including ad hoc requests.

Why PostgreSQL ?
- It easy to integrate with FastAPI.
- It has a strong reputation for reliability, feature robustness, and performance.
- It offers a lots of flexibility to users.
- It has a great track record of Data integrity, security at scale.

## Cloud Infra

### Components:

 - Postgres -> We can have a managed RDS Cluster.
 - Fast API service and worker will be hosted on AWS Auto scaling group behind an ALB. We will need to create other supporting resources like security groups, VPC, subnets etc. 
 - Rabbit MQ (Message Broker) -> We can choose a managed cluster from https://www.cloudamqp.com/ or we can have a self managed cluster for rabbitmq.

`Note: We automate the creation of the entire infra using terraform.`