class Client {
  newGame(callback) {
    const method = 'POST'
    const url = '/games'
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.send()
  }

  getGames(callback) {
    const method = 'GET'
    const url = '/games'
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.send()
  }

  getSingleGame(gameId, callback) {
    const method = 'GET'
    const url = `/games/${gameId}`
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.send()
  }

  joinGame(gameId, callback) {
    const method = 'POST'
    const url = `/games/${gameId}`
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.send()
  }

  challenge(gameId, username, callback) {
    const method = 'POST'
    const url = `/games/${gameId}/players`
    const data = JSON.stringify({username})
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.setRequestHeader('Content-type', 'application/json')
    request.send(data)
  }

  login(username, callback) {
    const method = 'POST'
    const url = '/login'
    const data = JSON.stringify({username})
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.setRequestHeader('Content-type', 'application/json')
    request.send(data)
  }

  submitWords(gameId, words, callback) {
    const method = 'POST'
    const url = `/games/${gameId}/words`
    const data = JSON.stringify({words})
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.setRequestHeader('Content-type', 'application/json')
    request.send(data)
  }

  getWords(gameId, callback) {
    const method = 'GET'
    const url = `/games/${gameId}/words`
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.send()
  }

  getPlayers(gameId, callback) {
    const method = 'GET'
    const url = `/games/${gameId}/players`
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.send()
  }

  vetoWord(gameId, word, callback) {
    const method = 'POST'
    const url = `/games/${gameId}/vetoes`
    const data = JSON.stringify({word})
    let request = new XMLHttpRequest()
    request.onreadystatechange = (x) => {
      if (request.readyState === 4) {
        callback(JSON.parse(request.response))
      }
    }
    request.open(method, url)
    request.setRequestHeader('Content-type', 'application/json')
    request.send(data)
  }
}
