const e = require('express')
const express = require('express')
const app = express()
const fetch = require('node-fetch')

app
  .get('/v1/player/:player_name', (req, res) => get_player(req, res))
  .get('/v1/player/:player_name/image', (req, res) => get_player_img(req, res))


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