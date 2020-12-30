if (!Array.prototype.last) {
  Array.prototype.last = function() {
    return this[this.length - 1]
  }
}

if (!Array.prototype.any) {
  Array.prototype.any = function(func) {
    for (let i = 0; i < this.length; i++) {
      if (func(this[i], i)) {
        return true
      }
    }
    return false
  }
}

if (!Array.prototype.all) {
  Array.prototype.all = function(func) {
    return !this.any((x, i) => !func(x, i))
  }
}

if (!Array.prototype.equals) {
  Array.prototype.equals = function(array) {
    return array.length == this.length && array.all(
      (x, i) => x === this[i]
    )
  }
}

class Game {

  constructor(endCallback) {
    this.duration = 3 * 60 * 1000
    const grid = Array(4).fill(0).map(() => Array(4).fill('A'))
    this.board = new Board(grid)
    this.words = []
    this.active = true
    this.endCallback = endCallback ? endCallback : () => {}
    setTimeout(() => {
      this.endCallback()
      this.active = false
    }, this.duration)
  }

  submitWord(word) {
    const valid = this.active
      && this.board.validate(word)
      && this.words.indexOf(word) < 0
    if (valid) { this.words.push(word) }
    return valid
  }

  render() {
    return '<div class="row">'
      + this.board.grid.map(
        (row) => row.map(
          (letter) => (
            '<div class="die">'
            + (letter === 'Q' ? 'Qu' : letter)
            + '</div>'
          )
        ).join('')
      ).join('</div><div class="row">')
      + '</div>'
  }
}


class Board {
  constructor(grid) {
    this.grid = grid
    this.height = grid.length
    this.width = grid[0].length
  }

  validate(word) {
    const qword = word.toUpperCase().replaceAll('QU', 'Q')
    const paths = qword.split('').reduce(
      (ps, c) => this.extendPaths(
        ps.filter(
          (p) => this.getTile(...p.last()) == c
        )
      ),
      this.initialPaths()
    )
    return paths.length > 0
  }

  initialPaths() {
    return Array(this.height).fill().map((e, y) =>
      Array(this.width).fill().map((e, x) => [[y, x]])
    ).reduce((a, b) => a.concat(b))
  }

  extendPaths(paths) {
    return paths.map(
      (p) => this.extendPath(p)
    ).reduce((a, b) => a.concat(b), [])
  }

  extendPath(path) {
    const nextTiles = this
      .getNeighbors(...path.last())
      .filter(
        (t) => path.all((p) => !t.equals(p))
      )
    return nextTiles.length > 0
      ? nextTiles.map((t) => [...path, t])
      : [[...path, [-1, -1]]]
  }

  getNeighbors(y, x) {
    if (y === null && x === null) {
      return this.initialPaths()
    }
    const vectors = [
      [-1, -1], [-1, 0], [-1, 1],
      [0, -1], [0, 1],
      [1, -1], [1, 0], [1, 1]
    ]
    return vectors.map(
      (v) => [y + v[0], x + v[1]]
    ).filter(
      (t) => this.getTile(...t) !== null
    )
  }

  getTile(y, x) {
    if (y >= 0 && y < this.height && x >= 0 && x < this.width) {
      return this.grid[y][x]
    } else {
      return null
    }
  }
}
