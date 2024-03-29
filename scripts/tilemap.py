import pygame

NEIGHBOR_OFFSETS = [(-1, -1), (0, -1), (1, -1), (2, -1),
                    (-1, 0), (0, 0), (1, 0), (2, 0),
                    (-1, 1), (0, 1), (1, 1), (2, 1),
                    (-1, 2), (0, 2), (1, 2), (2, 2),]

PHYSICS_TILES = {'grass', 'bricks'}

class Tilemap:
  def __init__(self, game, tile_size=8):
    self.game = game
    self.tile_size = tile_size
    self.tilemap = {}
    self.offgrid_tiles = []
    
    for i in range(25):
      self.tilemap[f'{i};10'] = {'type':'grass', 'variant': 7, 'pos': (i, 10)}
      
    for i in range(25):
      self.tilemap[f'25;{i}'] = {'type':'bricks', 'variant': 8, 'pos': (25, i)}

  def tiles_around(self, pos):
    tiles = []
    grid_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
    for offset in NEIGHBOR_OFFSETS:
      neighbor_loc = f'{grid_pos[0] + offset[0]};{grid_pos[1] + offset[1]}'
      if neighbor_loc in self.tilemap:
        tiles.append(self.tilemap[neighbor_loc])
    return tiles

  def physics_rects_around(self, pos):
    rects = []
    for tile in self.tiles_around(pos):
      if(tile['type'] in PHYSICS_TILES):
        rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size,
                                 self.tile_size, self.tile_size))
    return rects
  
  def render(self, surf, offset=(0, 0)):
    # offgrid tiles.
    for tile in self.offgrid_tiles:
      surf.blit(self.game.assets[tile['type']][tile['variant']], 
                tuple(map(lambda axis, offset: axis - offset, tile['pos'], offset)))
      
    # render only the tiles on the screen for optimization.
    for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
      for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
        loc = f'{x};{y}'
        if loc in self.tilemap:
          tile = self.tilemap[loc]
          surf.blit(self.game.assets[tile['type']][tile['variant']], 
                    tuple(map(lambda axis, offset: self.tile_size * axis - offset, tile['pos'], offset)))
              
    # for loc in self.tilemap:
    #   tile = self.tilemap[loc]
    #   surf.blit(self.game.assets[tile['type']][tile['variant']], 
    #             tuple(map(lambda axis, offset: self.tile_size * axis - offset, tile['pos'], offset)))
      
