// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');

async function queryCtwcCloud() {
  // Queries a public Stack Overflow dataset.

  // Create a client
  const bigqueryClient = new BigQuery();

  // The SQL query to run
  const sqlQuery = `SELECT
    Game_Id
    FROM \`ctwc-cloud.ctwc_dataset.ctwc\`
    LIMIT 10`;

  const options = {
    query: sqlQuery,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
  };

  // Run the query
  const [rows] = await bigqueryClient.query(options);

  console.log('Query Results:');

  rows.forEach(row => {
    console.log(row)
  });
}
queryCtwcCloud();