// Import the Kue module
const kue = require('kue');

/**
 * Function to create push notification jobs.
 * @param {Array} jobs - Array of job objects to process.
 * @param {Object} queue - Kue queue object.
 */
function createPushNotificationsJobs(jobs, queue) {
    // Check if jobs is an array
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    // Iterate through each job in the jobs array
    jobs.forEach((jobData) => {
        // Create a job in the push_notification_code_3 queue
        const job = queue.create('push_notification_code_3', jobData);

        // Log when the job is created
        job.on('enqueue', () => {
            console.log(`Notification job created: ${job.id}`);
        });

        // Log when the job is complete
        job.on('complete', () => {
            console.log(`Notification job ${job.id} completed`);
        });

        // Log when the job fails
        job.on('failed', (err) => {
            console.log(`Notification job ${job.id} failed: ${err}`);
        });

        // Log job progress
        job.on('progress', (progress) => {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });

        // Save the job to the queue
        job.save();
    });
}

module.exports = createPushNotificationsJobs;
