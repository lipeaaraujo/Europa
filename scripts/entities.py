import pygame

class PhysicsEntity:
  def __init__(self, game, e_type, pos, size):
    self.game = game
    self.type = e_type
    self.pos = list(pos)
    self.size = size
    self.velocity = [0, 0]
    self.collisions = {'left': False, 'right': False, 'top': False, 'bottom': False}
    
  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
  def update(self, tilemap, movement=(0, 0)):
    self.collisions = {'left': False, 'right': False, 'top': False, 'bottom': False}
    
    frame_movement = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
    
    # x axis movement.    
    self.pos[0] += frame_movement[0]
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[0] > 0:
          entity_rect.right = rect.left
          self.collisions['right'] = True
        if frame_movement[0] < 0:
          entity_rect.left = rect.right
          self.collisions['left'] = True
      self.pos[0] = entity_rect.x
    
    # y axis movement.
    self.pos[1] += frame_movement[1]
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if frame_movement[1] > 0:
          entity_rect.bottom = rect.top
          self.collisions['bottom'] = True
        if frame_movement[1] < 0:
          entity_rect.top = rect.bottom
          self.collisions['top'] = True
      self.pos[1] = entity_rect.y    
    
    # gravity.
    self.velocity[1] = min(5, self.velocity[1] + 0.1);
    
    if self.collisions['bottom'] or self.collisions['top']:
      self.velocity[1] = 0
    
  def render(self, surf, offset=(0, 0)):
    surf.blit(self.game.assets['player'], 
              tuple(map(lambda axis, offset: axis - offset, self.pos, offset)))
    