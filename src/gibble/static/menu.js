const client = new Client()

class LoadedGames {
  constructor() {
    self.gamesList = []
  }

  updateGamesListView() {
    const gamesSection = document.querySelector('#games')
    gamesSection.innerHTML = ''
    this.gamesList.map((game, index) => {
      let row = document.createElement('div')

      const gameTitle = document.createElement('span')
      gameTitle.style.fontWeight = 'bold'
      gameTitle.textContent = `Game ${game.id}`

      const gameLink = document.createElement('a')
      if (!game.played) gameLink.href = `game.html?gameId=${game.id}`
      gameLink.textContent = 'Play'

      const resultsLink = document.createElement('a')
      resultsLink.href = `results.html?gameId=${game.id}`
      resultsLink.textContent = 'Results'

      const header = document.createElement('div')
      header.appendChild(gameTitle)
      header.innerHTML += ' '
      header.appendChild(gameLink)
      header.innerHTML += ' '
      header.appendChild(resultsLink)
      header.innerHTML += ' '

      row.appendChild(header)

      const players = document.createElement('div')
      game.players.forEach((player) => {
        const playerName = document.createElement('p')
        playerName.textContent = player.username
        players.appendChild(playerName)
      })
      const challengeInput = document.createElement('input')
      challengeInput.type = 'text'
      challengeInput.id = `challenge-input-${index}`
      players.appendChild(challengeInput)
      const challengeButton = document.createElement('button')
      challengeButton.id = `challenge-button-${index}`
      challengeButton.setAttribute('onclick', `challengeButton(${game.id}, ${index})`)
      challengeButton.textContent = 'Challenge'
      players.appendChild(challengeButton)
      row.appendChild(players)

      row.style.padding = '1em 0em'

      return row
    }).forEach((ele) => gamesSection.appendChild(ele))
  }
}

const loadedGames = new LoadedGames()

const setUser = () => {
  const username = document.querySelector('#usernameInput').value
  login(username)
}

const login = (username) => {
  client.login(username, (loginResponse) => {
    const display = `${loginResponse.username} (${loginResponse.user_id})`
    document.querySelector('#usernameDisplay').innerText = display
    getGames()
  })
}

const getGames = () => {
  client.getGames((gamesResponse) => {
    loadedGames.gamesList = gamesResponse.games
    loadedGames.updateGamesListView()
  })
}

const newGame = () => {
  client.newGame((resp) => {
    getGames()
  })
}

const challengeButton = (gameId, index) => {
  const username = document.querySelector(`#challenge-input-${index}`).value
  client.challenge(gameId, username, (resp) => {
    getGames()
  })
}

window.onload = () => {
  if (document.cookie.indexOf('username') > -1) {
    const username = document.cookie.split('username=')[1].split(';')[0]
    login(username)
  }
}
