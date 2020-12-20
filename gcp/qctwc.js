// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery')

queryCtwcCloud = async (match_id) => {
  // Create a client
  const bigqueryClient = new BigQuery()

  // The SQL query to run
  const sqlQuery = `SELECT
    Game_Id, Match_Id, Series, Event, Round, Video_Id, Player_1, Player_2, Timestamp, Time_Seconds,
    Player_1_Score, Player_2_Score, Match_Winner, Match_Score
    FROM \`ctwc-cloud.ctwc_dataset.ctwc\`
    WHERE Match_Id=@match_id
    LIMIT 10`

  const options = {
    query: sqlQuery,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
    params: {match_id: `${match_id}`}
  }

  // Run the query
  const [match] = await bigqueryClient.query(options)

  console.log(`Query Results for Match: ${match_id}`)

//   console.log(games)

    match.forEach(game => {
        game.Video_Url = `https://youtu.be/${game.Video_Id}?t=${game.Time_Seconds}`
        delete game.Video_Id
        delete game.Time_Seconds
    })

    console.log(match)

    return match
}

// Main Starts Here
console.log("************==****************\n")

let match = queryCtwcCloud('ctwc_2017_r1-01')