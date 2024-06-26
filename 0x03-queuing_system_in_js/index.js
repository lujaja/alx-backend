const redis = require('redis');
const client = redis.createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');

    client.set('mykey', 'Hello, Redis!', (err, reply) => {
        console.log(reply);

        client.get('mykey', (err, reply) => {
            console.log(reply);

            client.hset('myhash', 'field1', 'value1', (err, reply) => {
                console.log(reply);

                client.hgetall('myhash', (err, reply) => {
                    console.log(reply);
                    client.quit();
                });
            });
        });
    });
})