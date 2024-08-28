// Import necessary modules
const kue = require('kue');

// Create the queue
const queue = kue.createQueue();

// Blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
    // Track job progress to 0%
    job.progress(0, 100);

    // Check if phoneNumber is blacklisted
    if (blacklistedNumbers.includes(phoneNumber)) {
        return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    }

    // Track job progress to 50%
    job.progress(50, 100);

    // Log the notification sending process
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

    // Job is completed
    done();
}

// Process the queue with 2 jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
    const { phoneNumber, message } = job.data;
    sendNotification(phoneNumber, message, job, done);
});
