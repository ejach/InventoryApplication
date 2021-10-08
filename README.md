# InventoryApplication

[![PyPI](https://img.shields.io/pypi/v/flask?logo=python&label=flask&style=flat-square&color=FFD43B)](https://pypi.org/project/flask/)
[![PyPI](https://img.shields.io/pypi/v/gunicorn?logo=python&label=gunicorn&style=flat-square&color=FFD43B)](https://pypi.org/project/gunicorn/)

### Project Details
There is a need to have a system in place that allows for part inventory to be tracked over each of the company vans that SOS Irrigation utilizes. Each technician has an iPad or a personal device to use on the van, so by developing a web application to sync across all devices helps keep track of all inventory in each van. A database of each part SOS Irrigation uses is necessary to keep track of all inventory in the system. The database will have the ability to add or remove parts in inventory. A count of each available part on a given van will be visible to the user. The ability to see what parts are low in stock or missing is important to know what parts to order. It will export data from the system to generate a list of all the parts the company has in inventory.

## [Installation](https://github.com/ejach/InventoryApplication/wiki/Installation)

### Manual

#### Prerequisites

Make sure you have a MySQL database running (use [this](https://gist.github.com/ejach/d84a303fd791dc386d0570dba3c54e43) to set it up via Docker) with the [correct database schema](https://github.com/ejach/InventoryApplication/blob/main/database.sql)

1. Clone the repo by running `$ git clone https://github.com/ejach/InventoryApplication.git`
2. `cd` into the cloned directory `$ cd InventoryApplication`
3. Change the environment variables to your liking by [exporting them](https://bash.cyberciti.biz/guide/Export_Variables) shown in `example.env`
```bash
# Host for the MySQL database and the WebUI (default is localhost)
host=localhost
# Host for the WebUI
webui_host=localhost
# Port for the WebUI using a WSGI server (default is 5000 for development, 8000 for production)
webui_port=5000
# Username for the MySQL database (default is root)
username=root
# Password for the MySQL database (default is root)
password=root
# Port for the MySQL database (default is 3306)
db_port=3306
# Database schema name in the MySQL database (default is parts)
db_schema=parts
# Database table in the MySQL database (default is parts)
db=parts
```
5. Install the requirements `$ pip install -r requirements.txt`

    _Make sure that your user has read/write permissions in the database/table that has been created or else it will not work._

6. Run the program using `python wsgi.py`

### Docker Run
`$ docker run -it -e host=<host> -e port=<port> -e webui_host=<webui_host> -e webui_port=<webui_port> -e db_port=<db_port> -e db=<db> ghcr.io/ejach/inventoryapplication:latest`

_Change the corresponding environment variables as needed_

### Docker-Compose

1. Run `$ docker volume create --name db-data` to create the volume used by the MySQL database
2. Use the [docker-compose](https://github.com/ejach/InventoryApplication/blob/main/docker-compose.yml) file and edit the `environment` variables as needed:

```yaml
version: '3.8'
services:
  db:
    image: mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: parts
    volumes:
      - db-data:/var/lib/mysql
    ports:
      - "3308:3306"
  phpmyadmin:
    image: phpmyadmin/phpmyadmin:latest
    restart: always
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: root
    ports:
      - "8080:80"
  invapplication:
    image: ghcr.io/ejach/inventoryapplication:latest
    restart: always
    environment:
      host: db
      webui_host: localhost
      webui_port: 5000
      username: root
      password: root
      db_port: 3306
      db: parts
    ports:
      - "5000:8000"
volumes:
  db-data:
    external: true
```
2. Run `$ docker-compose -f docker-compose.yml up -d`

### Docker Build
1. Make sure you have a MySQL database running with the [correct database schema](https://github.com/ejach/InventoryApplication/blob/main/database.sql)
2. Change the environment variables to your liking by [exporting them](https://bash.cyberciti.biz/guide/Export_Variables) shown in `example.env`
3. Build the image using the existing `Dockerfile` by running `$ docker build -t inventoryapplication .`
4. Run the newly created image using `$ docker run inventoryapplication`
