const client = new Client()

class LoadedGames {
  constructor() {
    self.gamesList = []
  }

  mostRecentSort(a, b) {
    if (new Date(a.created_at) < new Date(b.created_at)) {
      return 1
    } else {
      return -1
    }
  }

  updateGamesListView(sortFunc) {
    sortFunc = sortFunc !== undefined ? sortFunc : this.mostRecentSort
    const gamesSection = document.querySelector('#games')
    gamesSection.innerHTML = ''
    const fragment = document.createDocumentFragment()
    this.gamesList.sort(sortFunc).forEach((game, index) => {
      let row = document.createElement('div')

      const gameTitle = document.createElement('span')
      gameTitle.style.fontWeight = 'bold'
      gameTitle.style.fontSize = 'large'
      gameTitle.textContent = `Game ${game.id}`

      let type = 'span'
      let gameHref = null
      let className = 'disabled'
      if (!game.played) {
        type = 'a'
        gameHref = `game.html?gameId=${game.id}`
        className = null
      }
      const gameLink = document.createElement(type)
      gameLink.href = gameHref
      gameLink.className = className
      gameLink.textContent = 'Play'

      const resultsLink = document.createElement('a')
      resultsLink.href = `results.html?gameId=${game.id}`
      resultsLink.textContent = 'Results'

      const header = document.createElement('div')
      header.appendChild(gameTitle)
      header.innerHTML += ' - '
      header.appendChild(gameLink)
      header.innerHTML += ' - '
      header.appendChild(resultsLink)

      row.appendChild(header)

      const gameDate = document.createElement('div')
      gameDate.className = 'game-date'
      const createdAt = new Date(game.created_at)
      gameDate.textContent = createdAt.toISOString().substring(0, 10)

      row.appendChild(gameDate)

      const players = document.createElement('ul')
      game.players.forEach((player) => {
        const playerName = document.createElement('li')
        playerName.className = player.played ? null : 'disabled'
        playerName.textContent = player.username
        players.appendChild(playerName)
      })
      row.appendChild(players)

      const challengeInput = document.createElement('input')
      challengeInput.type = 'text'
      challengeInput.id = `challenge-input-${index}`

      const challengeButton = document.createElement('button')
      challengeButton.id = `challenge-button-${index}`
      challengeButton.setAttribute('onclick', `challengeButton(${game.id}, ${index})`)
      challengeButton.textContent = 'Challenge'

      const challengeDiv = document.createElement('div')
      challengeDiv.appendChild(challengeInput)
      challengeDiv.appendChild(challengeButton)
      row.appendChild(challengeDiv)

      row.style.padding = '1em 0em'

      fragment.appendChild(row)
    })
    gamesSection.appendChild(fragment)
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
