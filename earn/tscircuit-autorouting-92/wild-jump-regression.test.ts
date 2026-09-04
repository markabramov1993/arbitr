import { test, expect } from "bun:test"
import { MultilayerIjump } from "../../../algos/multi-layer-ijump/MultilayerIjump"
import { ObstacleList3d } from "../../../algos/multi-layer-ijump/ObstacleList3d"

test("multilayer ijump does not create an infinite-corridor jump away from the goal", () => {
  const obstacle = {
    type: "rect",
    center: { x: 0, y: 0 },
    width: 2,
    height: 2,
    layers: ["top"],
    connectedTo: [],
  } as any

  const input = {
    layerCount: 2,
    minTraceWidth: 0.1,
    obstacles: [obstacle],
    connections: [],
  } as any

  const autorouter = new MultilayerIjump({
    input,
    OBSTACLE_MARGIN: 0.15,
    startNode: { x: -5, y: 0 } as any,
    goalPoint: { x: 5, y: 10 } as any,
  })

  autorouter.obstacles = new ObstacleList3d(2, [obstacle])
  autorouter.startNode = {
    x: -5,
    y: 0,
    l: 0,
    g: 0,
    h: 0,
    f: 0,
    nodesInPath: 0,
    manDistFromParent: 0,
    parent: null,
  } as any
  autorouter.goalPoint = { x: 5, y: 10, l: 0 } as any

  // This node represents the normal iJump state immediately after the
  // forward ray hit the obstacle. The next step should only travel far enough
  // up/down to clear the obstacle. The old multilayer implementation also
  // generated a second point at |goal.y-node.y| in *both* perpendicular
  // directions. Because distAlongDir is unsigned, that produced y=-10 even
  // though the goal is at y=+10.
  const obstacleHit = autorouter.obstacles.obstacles[0]
  const node = {
    x: -1.15,
    y: 0,
    l: 0,
    g: 3.85,
    h: 0,
    f: 0,
    nodesInPath: 1,
    manDistFromParent: 3.85,
    parent: autorouter.startNode,
    obstacleHit,
  } as any

  const neighbors = autorouter.getNeighbors(node)

  // Moving downward just far enough to clear a 2mm obstacle plus margin is
  // valid (about -1.15/-2 depending on the margin tier). A jump all the way
  // to -10 is not: it is the absolute goal projection applied in the wrong
  // direction.
  expect(neighbors.some((p) => p.y < -2.01)).toBe(false)
  expect(neighbors.some((p) => p.y === -10)).toBe(false)
})
