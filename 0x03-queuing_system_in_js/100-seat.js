const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

// Redis client setup
const redisClient = redis.createClient();
const asyncGet = promisify(redisClient.get).bind(redisClient);
const asyncSet = promisify(redisClient.set).bind(redisClient);

// Redis functions for seat management
async function reserveSeat(number) {
    await asyncSet('available_seats', number.toString());
}

async function getCurrentAvailableSeats() {
    const seats = await asyncGet('available_seats');
    return parseInt(seats) || 0;
}

// Initialize available seats
reserveSeat(50); // Start with 50 seats available

// Express setup
const app = express();
const PORT = 1245;

// Kue setup
const queue = kue.createQueue();

// Middleware to parse JSON
app.use(express.json());

// Route to get number of available seats
app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
    const reservationEnabled = true; // Adjust as per your logic
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat').save(err => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        res.json({ status: 'Reservation in process' });
    });
});

// Route to process the seat reservation queue
app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        const currentAvailableSeats = await getCurrentAvailableSeats();
        if (currentAvailableSeats === 0) {
            // No seats available
            done(new Error('Not enough seats available'));
            return;
        }

        await reserveSeat(currentAvailableSeats - 1);
        if (currentAvailableSeats - 1 === 0) {
            // Update reservationEnabled status
            // reservationEnabled = false;
        }

        console.log(`Seat reservation job ${job.id} completed`);
        done();
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
