import { Board } from './game.js'

let grid = [
  ['c', 'a', 't', 'a', 'a'],
  ['a', 'a', 'a', 'a', 'a'],
  ['b', 'a', 'a', 'a', 'a'],
  ['a', 'a', 'a', 'a', 'a'],
  ['a', 'a', 'a', 'a', 'a']
]
let board = new Board(grid)

console.log(board.getNeighbors(0, 0))
console.log(board.extendPath([[0,0], [0,1]]))
console.log(board.extendPaths([
  [[0,0], [0,1]],
  [[1,1], [0,1]]
]))

console.log('any')
console.log([1, 2, 3].any((x) => x === 3))
console.log([1, 2, 3].any((x) => x === 0) == false)

console.log('all')
console.log([1, 2, 3].all((x) => x < 4))
console.log([1, 2, 3].all((x) => x === 1) === false)
console.log([1, 2, 3].all((x, i) => x === [1, 2, 3][i]))

console.log('equals')
console.log([1, 2, 3].equals([1, 2, 3]))
console.log([1, 2, 3].equals([1, 2, 4]) === false)

console.log('validate')
console.log(board.validate('abc') === false)
console.log(board.validate('cat') === true)
console.log(board.validate('cabat') == true)
console.log(board.validate('bacatac') == false)
