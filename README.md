# InventoryApplication

### Project Details
There is a need to have a system in place that allows for part inventory to be tracked over each of the company vans that SOS Irrigation utilizes. Each technician has an iPad or a personal device to use on the van, so by developing a web application to sync across all devices helps keep track of all inventory in each van. A database of each part SOS Irrigation uses is necessary to keep track of all inventory in the system. The database will have the ability to add or remove parts in inventory. A count of each available part on a given van will be visible to the user. The ability to see what parts are low in stock or missing is important to know what parts to order. It will export data from the system to generate a list of all the parts the company has in inventory.

## [Installation](https://github.com/ejach/InventoryApplication/wiki/Installation)

### Manual

1. Clone the repo by running `$ git clone https://github.com/ejach/InventoryApplication.git`
2. `cd` into the cloned directory `$ cd InventoryApplication`
3. Install the requirements `$ pip install -r requirements.txt`

### Docker

_As of right now there is no image uploaded to a container repository because it is in its early stages. Once it is uploaded to a container repository (most likely on GitHub) these instructions will change._

1. Change the environment variables to your liking in `.env`:
```bash
host=localhost
port=8000
db_file=database.db
db=parts
```
2. Build the image using the existing `Dockerfile` by running `$ docker build -t inventoryapplication .`
3. Run the newly created image using `$ docker run inventoryapplication`
