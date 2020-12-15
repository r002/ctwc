const express = require('express')
const app = express()
const fetch = require('node-fetch')

app.get('/player/image/:player_name', (req, res) => get_player_img(req, res))

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