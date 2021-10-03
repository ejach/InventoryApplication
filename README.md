# InventoryApplication

### Project Details
There is a need to have a system in place that allows for part inventory to be tracked over each of the company vans that SOS Irrigation utilizes. Each technician has an iPad or a personal device to use on the van, so by developing a web application to sync across all devices helps keep track of all inventory in each van. A database of each part SOS Irrigation uses is necessary to keep track of all inventory in the system. The database will have the ability to add or remove parts in inventory. A count of each available part on a given van will be visible to the user. The ability to see what parts are low in stock or missing is important to know what parts to order. It will export data from the system to generate a list of all the parts the company has in inventory.

## [Installation](https://github.com/ejach/InventoryApplication/wiki/Installation)

### Manual

1. Clone the repo by running `$ git clone https://github.com/ejach/InventoryApplication.git`
2. `cd` into the cloned directory `$ cd InventoryApplication`
3. Install the requirements `$ pip install -r requirements.txt`
4. Create the database file using `database.sql` and name it `database.db` and place it in the root directory

    _Make sure that your user has read/write permissions in the database/table that has been created or else it will not work._

6. Run the program using `python wsgi.py`

### Docker (not working currently [#36](https://github.com/ejach/InventoryApplication/issues/36))
`docker run -it -e host=<host> -e port=<port> -e db_file=<db_file> -e db=<db> ghcr.io/ejach/inventoryapplication:latest`

1. Change the environment variables to your liking in `.env`:
```bash
# Host for the MySQL database and the WebUI (default is localhost)
host=localhost
# Port for the WebUI using a WSGI server (default is 5000 for development, 8000 for production)
webui_port=5000
# Username for the MySQL database (default is root)
username=root
# Password for the MySQL database (default is root)
password=root
# Port for the MySQL database (default is 3306)
db_port=3308
# Database name in the MySQL database (default is parts)
db=parts
```
2. Build the image using the existing `Dockerfile` by running `$ docker build -t inventoryapplication .`
3. Run the newly created image using `$ docker run inventoryapplication`
