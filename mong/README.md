# MongoDB

In this directory there is the main configuration to run MongoDB, including different APIs that connect from the stream of data and post to specific collections (No-SQL version of tables).

# Current implementation

The current implementation subscribes to Kafka topics from the tickets, passengers, and sensors API and pushes data into the MongoDB `raw` database based on the specific topic it is listening to.
In the newer version, inserts are performed directly from the generator without the need to make calls to exposed APIs. Data is then inserted in the `passengers`, `tickets`, `sensors`, `gps`, and `traffic` collections.

# Example: Accessing and Querying MongoDB

First, make sure that on your local machine you have `mongosh` installed (https://www.mongodb.com/docs/mongodb-shell/). Then you can query MongoDB from the CLI by doing the following:

1. Initiate the connection to the Database

```
mongosh mongodb://localhost:27017
```

2. Select `raw` Database

```
use raw
```

3. List all collections in Database

```
show collections
```

4. Find all documents from `sensors` collection

```
db.sensors.find()
```

5. Find specific entries in the `sensors` collection

```
db.sensors.find().sort({ "_id": -1 }).limit(1)
```

# History of development

Previous versions of this used the following approach:

- At this point in time, deduplication is also handled at this step by checking whether the `measurement_id` from sensors or the `ticket_id` from tickets are already available in MongoDB and avoiding reinsertion in that case.
