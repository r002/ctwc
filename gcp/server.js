const e = require('express')
const express = require('express')
const app = express()
const fetch = require('node-fetch')
const {BigQuery} = require('@google-cloud/bigquery')

app
  .get('/v1/player/:player_name', (req, res) => get_player(req, res))
  .get('/v1/player/:player_name/image', (req, res) => get_player_img(req, res))

  .get('/v1/match/:match_id', (req, res) => queryCtwcCloud(req, res))


queryCtwcCloud = async (req, res) => {
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
    params: {match_id: `${req.params.match_id}`}
  }

  // Run the query
  const [match] = await bigqueryClient.query(options)

  console.log(`Query Results for Match: ${req.params.match_id}`)

  match.forEach(game => {
      game.Video_Url = `https://youtu.be/${game.Video_Id}?t=${game.Time_Seconds}`
      delete game.Video_Id
      delete game.Time_Seconds
  })

  console.log(match)

  res.send(match)
}

get_player = async (req, res) => {
  // res.send(`>> Player Fetched: ${req.params.player_name}`)

  let url = "https://r002.github.io/ctwc/db/players.json"
  let settings = { method: "Get" }
  fetch(url, settings)
    .then(res => res.json())
    .then((player_list) => {
      // console.log(">> RETURNED", player_list)

      result = player_list.filter(player => {
        return player.player_code === req.params.player_name
      })

      if (result.length>0) {
        result[0].image = `https://ctwc-cloud.appspot.com/v1/player/${req.params.player_name}/image`
      } else
      {
        result = "No player with that player_code found."
      }

      res.send(result)
  })

}


get_player_img = async (req, res) => {
  const url = `https://r002.github.io/ctwc/img/player/${req.params.player_name}.png`
  console.log(">> Trying:", url)
  
  const response = await fetch(url, { method: 'HEAD' })
  console.log(">> CTWC RESP:", response.ok)

  if(response.ok) {
      res.redirect(url)
  } else {
      res.redirect("https://r002.github.io/ctwc/img/player/unavailable.png")
  }
}

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`)
})