import express from 'express';
import { promisify } from 'util';
import kue from 'kue';
import redis from 'redis';

// Create Redis client
const client = redis.createClient();
const reserveSeat = promisify(client.set).bind(client);
const getCurrentAvailableSeats = promisify(client.get).bind(client);

// Set the initial number of available seats
reserveSeat('available_seats', 50);

// Initialize reservation control variable
let reservationEnabled = true;

// Create Kue queue
const queue = kue.createQueue();

// Create Express server
const app = express();
const port = 1245;

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats('available_seats');
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservations are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

// Route to process the queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats('available_seats');
    let availableSeats = parseInt(currentSeats, 10);

    if (availableSeats <= 0) {
      done(new Error('Not enough seats available'));
      return;
    }

    availableSeats -= 1;
    await reserveSeat('available_seats', availableSeats);

    if (availableSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
