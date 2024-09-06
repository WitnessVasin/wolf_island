import random

# Базовый класс для всех существ
class Entity:
    def __init__(self, x, y, island):
        self.x = x
        self.y = y
        self.island = island

    def move(self):
        # Существа перемещаются в случайном направлении
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        new_x = (self.x + dx) % self.island.size
        new_y = (self.y + dy) % self.island.size

        if self.island.grid[new_x][new_y] is None:
            self.island.grid[self.x][self.y] = None
            self.x, self.y = new_x, new_y
            self.island.grid[self.x][self.y] = self

# Класс для волков
class Wolf(Entity):
    def __init__(self, x, y, island):
        super().__init__(x, y, island)
        self.hunger = 5  # Волк умирает, если не поест 5 ходов

    def eat(self):
        # Волк ест зайца, если он рядом
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = (self.x + dx) % self.island.size, (self.y + dy) % self.island.size
            if isinstance(self.island.grid[nx][ny], Rabbit):
                self.island.grid[nx][ny] = None
                self.hunger = 5  # Сбрасывает голод после еды
                return

    def update(self):
        self.hunger -= 1
        if self.hunger <= 0:
            self.island.grid[self.x][self.y] = None  # Волк умирает от голода
        else:
            self.eat()
            self.move()

# Класс для волчиц
class FemaleWolf(Wolf):
    def reproduce(self):
        # Размножение, если рядом есть волк
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = (self.x + dx) % self.island.size, (self.y + dy) % self.island.size
            if isinstance(self.island.grid[nx][ny], Wolf):
                empty_spots = [(self.x + ex, self.y + ey) for ex, ey in directions
                               if 0 <= self.x + ex < self.island.size and 0 <= self.y + ey < self.island.size
                               and self.island.grid[self.x + ex][self.y + ey] is None]
                if empty_spots:
                    spawn_x, spawn_y = random.choice(empty_spots)
                    self.island.grid[spawn_x][spawn_y] = FemaleWolf(spawn_x, spawn_y, self.island)

    def update(self):
        super().update()
        self.reproduce()

# Класс для зайцев
class Rabbit(Entity):
    def reproduce(self):
        # Размножение зайцев
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        empty_spots = [(self.x + dx, self.y + dy) for dx, dy in directions
                       if 0 <= self.x + dx < self.island.size and 0 <= self.y + dy < self.island.size
                       and self.island.grid[self.x + dx][self.y + dy] is None]
        if empty_spots:
            spawn_x, spawn_y = random.choice(empty_spots)
            self.island.grid[spawn_x][spawn_y] = Rabbit(spawn_x, spawn_y, self.island)

    def update(self):
        self.reproduce()
        self.move()

# Класс острова
class Island:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def add_entity(self, entity):
        self.grid[entity.x][entity.y] = entity

    def update(self):
        # Обновляем все существа на острове
        entities = [entity for row in self.grid for entity in row if entity is not None]
        for entity in entities:
            entity.update()

    def display(self):
        # Печать состояния острова
        for row in self.grid:
            print("".join(["W" if isinstance(e, Wolf) else 
                           "F" if isinstance(e, FemaleWolf) else 
                           "R" if isinstance(e, Rabbit) else "." 
                           for e in row]))
        print("\n")

# Инициализация острова
island = Island(20)

# Добавляем волков волчиц и зайцев на поле.
# Тест
for _ in range(10):
    x, y = random.randint(0, 19), random.randint(0, 19)
    island.add_entity(Wolf(x, y, island))

for _ in range(5):
    x, y = random.randint(0, 19), random.randint(0, 19)
    island.add_entity(FemaleWolf(x, y, island))

for _ in range(20):
    x, y = random.randint(0, 19), random.randint(0, 19)
    island.add_entity(Rabbit(x, y, island))

# Запуск симуляции
for _ in range(20):
    island.display()
    island.update()
    
