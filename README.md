# Group 71: Welcome to Grocery Express

# Note please run all scripts/commands from the project root directory

## Prerequisites:
1. Docker installed
Use `docker --version` to check whether Docker has been installed.
2. Maven installed
Use `mvn -version` to check whether Maven has been installed.

### To Install Docker go to:
```
https://docs.docker.com/get-docker/
```
### To Install Maven go to:
```
https://maven.apache.org/download.cgi
```

## Compile project
```shell script
mvn clean package
```
- This step compiles the project using Maven build system by running the command "mvn clean package". The "clean" command deletes any existing build artifacts and the "package" command compiles the project and generates a JAR package, that can be used to run the application.

## Build docker images
```shell script
sh docker_build.sh
```
- This step builds Docker images for the application using the script "docker_build.sh". The script contains instructions for building the images, including specifying the base image to use, copying the application files into the image, and setting environment variables. 

## Run database
```shell script
docker-compose up -d mysql
```
- This step runs a MySQL database instance as a Docker container. The command starts the MySQL container and runs it as a background process. 
- Please note that if you have not previously installed the Docker image for MySQL, Docker will automatically download the MySQL image from Docker Hub before running the "docker-compose up -d mysql" command. The download time of the image depends on your network speed and the size of the image to be downloaded.
## Run service
```shell script
docker-compose up -d
```
- This step runs the application as a Docker container using the command "docker-compose up -d". The command starts all the containers defined in the Docker Compose file, which means that the containers run in the background.
## Run client
```shell script
java -jar ./grocery-express-client/target/client-0.0.1-SNAPSHOT.jar http://localhost:80 
```
- The default URL for requests is http://localhost:8080, but you can specify a custom request URL by providing it as a parameter when running the client JAR.
- This is a command to run the client JAR file located at "./grocery-express-client/target/client-0.0.1-SNAPSHOT.jar" with a custom request URL specified as a parameter. The custom request URL in this case is "http://localhost:80". 

## Remove service
```shell script
docker-compose down
```
- This step stops and removes the containers created by the previous step using the command "docker-compose down". The command stops the containers and removes any networks defined in the Docker Compose file.

## Improvements
### Summary
This system adopts the "Client-Server" architecture pattern of front-end and back-end separation. The front-end is a CLI application program written in Java language, and the back-end uses the Spring Boot framework. Additionally, Maven is used for automating the build and managing the dependencies of the Java project, simplifying the development, build, and deployment process. As for the database, we use the Hibernate framework to manage the object mapping of MySQL database, which simplifies the development of data access layer and efficiently handles data operations.

### Scalability
- **Database optimization**. First, we carefully designed and improved the table structure of the database. Then, we used the Hibernate ORM framework to manage the mapping between objects and the database, further improving the efficiency of data processing. Finally, we added indexes to reduce the database load and avoid system bottlenecks, resulting in faster read and write operations. For example, we added two indexes, `customer_id` and `store_id`, to the `coupon` table, an index for `store_id` to the `fueling_station` table, and two indexes, `pilot_id` and `store_id`, to the `drone` table.

- **Load balancing architecture**. We implemented load balancing through Docker Compose and Nginx. The approach involved deploying customer and store microservices in Docker containers, adjusting the scale of Docker container instances, and using Nginx to perform traffic forwarding and load balancing. Details can be found in the `docker-compose.yml` and `nginx.conf` code.

- **Microservices architecture**. We split the backend services into two parts, customer and store, and implemented microservices through deployment in the `docker-compose.yml`. This is evident from our code structure.

### Time-Sensitive Coupons
- Time-sensitive coupons are to be instantiated with 3 key attributes: coupon id, coupons reduction which represents the dollar reductions for customer’s order, and coupon expiration date, which sets an important deadline for order delivery.
- The distribution of coupons has been set as a function within time-sensitive coupon class: once distributed, this specific coupon id will be associated with the customer.
- Coupon class has been associated with Customer class via TreeMap as an attribute for coupons received for each customer.
- Coupon class also has a relationship with Store class: Store could add attributes and functions such as distribution frequency which could be adjusted and determine the frequency of calling coupon’s distribution functions. While distributing, Store should also check customer ratings and distribute more frequently to customers with higher ratings.
- Once associated with customer class, coupons could be related to order class. When an order is purchased, the system could check if the corresponding customer has a coupon and the coupon should be applied onto order cost and customer credit deducted. Order should also have an additional attribute such as delivery time to compare with the coupon's expiry date. If the order's delivery time exceeds the coupon's expiry date, it will affect the store's revenue.
- New commands include:
```
[1] assign_coupon,storeName
Command:
assign_coupon,storeName,account,couponId,couponReduction,expiryPeriod

> assign_coupon,kroger,aapple2,1,5,3
OK:coupon_assigned
> assign_coupon,fresh_market,aapple2,1,5,3
ERROR:store_identifier_does_not_exist
> assign_coupon,kroger,aapple2,1,15,5
ERROR:coupon_identifier_already_exists
> assign_coupon,kroger,aapple3,1,5,3
ERROR:customer_identifier_does_not_exist
> assign_coupon,kroger,aapple2,2,50,3
OK:coupon_assigned


[2] display_coupon
Command:
display_coupon,storeName

> display_coupon,kroger
Coupon{id=null, store=kroger, customer=aapple2, couponId=1, couponReduction=5, expiryPeriod=3, expiryDate=Tue Apr 25 00:02:05 CST 2023, expiry=false}
Coupon{id=null, store=kroger, customer=aapple2, couponId=2, couponReduction=50, expiryPeriod=3, expiryDate=Tue Apr 25 00:04:03 CST 2023, expiry=false}
OK:display_completed
> display_coupon,fresh_market
ERROR:store_identifier_does_not_exist
```

### Fueling Station
- We have created a new FuelingStation class that includes attributes for StationID and Location. The StationId will be used to uniquely identify each fueling station, and the Location attribute will store the coordinates of the fueling station.
- The FuelingStation class has been associated with the Store class. We have modified the Store class to include a new attribute, FuelingStations, which stores all fueling stations in the system. By default, the Store class is also a fueling station.- New commands include:
```
[1] make_fueling_station
Command:
make_fueling_station,stationID,xCoordinate,yCoordinate,storeName

> make_fueling_station,1,15,15,kroger
ERROR:station_identifier_already_exists
> make_fueling_station,3,15,15,kroger
OK:change_completed
> make_fueling_station,4,15,15,fresh_market
ERROR:store_identifier_does_not_exist
> make_fueling_station,4,35,35,kroger
OK:change_completed
> make_fueling_station,5,60,60,publix
OK:change_completed


[2] delete_fueling_station
Command:
delete_fueling_station,stationID

> delete_fueling_station,5
OK:change_completed
> delete_fueling_station,10
ERROR:station_identifier_does_not_exist


[3] check_refueling_option
Command:
check_refueling_option,droneID,storeName

> check_refueling_option,1,kroger
stationID:1,location:(10,10)
stationID:3,location:(15,15)
stationID:4,location:(35,35)
OK:display_completed
> check_refueling_option,5,kroger
ERROR:drone_identifier_does_not_exist
> check_refueling_option,5,fresh_market
ERROR:store_identifier_does_not_exist


[4] refuel_drone
Command:
refuel_drone,droneID,stationID,storeName

> display_drones,kroger
droneID:1,total_cap:40,num_orders:0,remaining_cap:40,trips_left:0,flown_by:Finneas_Fig,fuel_rate:5,max_fuel_capacity:200.00,remaining_fuel:173.48,location:(20,20)
droneID:2,total_cap:20,num_orders:0,remaining_cap:20,trips_left:3,fuel_rate:8,max_fuel_capacity:240.00,remaining_fuel:240.00,location:(10,10)
droneID:4,total_cap:40,num_orders:1,remaining_cap:36,trips_left:5,fuel_rate:6,max_fuel_capacity:240.00,remaining_fuel:240.00,location:(10,10)
OK:display_completed
> refuel_drone,1,4,kroger
OK:change_completed
> display_drones,kroger
droneID:1,total_cap:40,num_orders:0,remaining_cap:40,trips_left:0,flown_by:Finneas_Fig,fuel_rate:5,max_fuel_capacity:200.00,remaining_fuel:200.00,location:(35,35)
droneID:2,total_cap:20,num_orders:0,remaining_cap:20,trips_left:3,fuel_rate:8,max_fuel_capacity:240.00,remaining_fuel:240.00,location:(10,10)
droneID:4,total_cap:40,num_orders:1,remaining_cap:36,trips_left:5,fuel_rate:6,max_fuel_capacity:240.00,remaining_fuel:240.00,location:(10,10)
OK:display_completed
> refuel_drone,6,4,kroger
ERROR:drone_identifier_does_not_exist
> refuel_drone,1,6,kroger
ERROR:station_identifier_does_not_exist
> refuel_drone,1,6,fresh_market
ERROR:store_identifier_does_not_exist
```