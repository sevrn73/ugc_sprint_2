const dbName = "ugc_db";
const conn = new Mongo();
const db = conn.getDB(dbName);

const collectionSettings = [
    {
        name: "bookmarks",
        shardKey: "user_id",
        indexFields: ["film_id", "timestamp"]
    },
    {
        name: "likes",
        shardKey: "user_id",
        indexFields: ["film_id", "score", "timestamp"]
    },
    {
        name: "reviews",
        shardKey: "user_id",
        indexFields: [
            "film_id",
            "timestamp",
            "text",
        ]
    },
];

sh.enableSharding(dbName);

collectionSettings.forEach((collection) => {
    const collectionName = collection.name;
    const shardKey = collection.shardKey;
    const indexFields = collection.indexFields;

    db.createCollection(collectionName);
    if (shardKey !== undefined) {
        sh.shardCollection(`${dbName}.${collectionName}`, {[shardKey]: "hashed"});
    }
    if (indexFields !== undefined) {
        indexFields.forEach((field) => {
            db[collectionName].createIndex({[field]: -1});
        })
    }
});
