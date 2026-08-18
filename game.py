"""
MM7-style RPG Game with HoMM3 atmosphere.
3D world with sprite-based objects and 4-hero party.
Built with Ursina engine.
"""

from ursina import *
from PIL import Image, ImageDraw, ImageFont
import os
import math
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


class HeroClass(Enum):
    """Hero classes in HoMM3 style."""
    KNIGHT = "Knight"
    CLERIC = "Cleric"
    RANGER = "Ranger"
    SORCERER = "Sorcerer"


@dataclass
class Hero:
    """Hero character data."""
    name: str
    hero_class: HeroClass
    level: int = 1
    hp: int = 50
    max_hp: int = 50
    mp: int = 20
    max_mp: int = 20
    attack: int = 10
    defense: int = 8
    spell_power: int = 5
    
    def __str__(self) -> str:
        return f"{self.name} ({self.hero_class.value}) Lvl {self.level}"


def create_hero_sprite(hero_class: HeroClass, color: tuple) -> str:
    """Create a sprite texture for a hero class."""
    size = (64, 64)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw body
    body_color = color
    draw.rectangle([20, 25, 44, 55], fill=body_color)
    
    # Draw head
    draw.ellipse([22, 10, 42, 30], fill=(255, 200, 150, 255))
    
    # Draw class-specific details
    if hero_class == HeroClass.KNIGHT:
        # Helmet
        draw.arc([22, 8, 42, 28], 0, 180, fill=(200, 200, 200, 255), width=3)
        # Shield
        draw.rectangle([15, 30, 22, 50], fill=(100, 100, 200, 255))
    elif hero_class == HeroClass.CLERIC:
        # Robe
        draw.polygon([(20, 55), (44, 55), (32, 25)], fill=(255, 255, 200, 255))
        # Holy symbol
        draw.rectangle([30, 35, 34, 45], fill=(255, 215, 0, 255))
    elif hero_class == HeroClass.RANGER:
        # Bow
        draw.arc([10, 30, 25, 50], 270, 90, fill=(139, 69, 19, 255), width=2)
        # Green hood
        draw.arc([22, 8, 42, 28], 0, 180, fill=(34, 139, 34, 255), width=3)
    elif hero_class == HeroClass.SORCERER:
        # Staff
        draw.rectangle([45, 25, 48, 55], fill=(139, 69, 19, 255))
        # Blue robe
        draw.polygon([(20, 55), (44, 55), (32, 25)], fill=(100, 149, 237, 255))
    
    # Save texture
    filepath = f"assets/sprites/{hero_class.value.lower()}.png"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    return filepath


def create_tree_sprite() -> str:
    """Create a tree sprite."""
    size = (128, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Trunk
    draw.rectangle([50, 180, 78, 256], fill=(101, 67, 33, 255))
    
    # Foliage (multiple layers for depth)
    foliage_color = (34, 139, 34, 255)
    dark_foliage = (20, 100, 20, 255)
    
    # Bottom layer
    draw.ellipse([20, 140, 108, 200], fill=dark_foliage)
    # Middle layer
    draw.ellipse([15, 100, 113, 170], fill=foliage_color)
    # Top layer
    draw.ellipse([30, 60, 98, 130], fill=foliage_color)
    # Top point
    draw.polygon([(64, 30), (40, 80), (88, 80)], fill=foliage_color)
    
    filepath = "assets/sprites/tree.png"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    return filepath


def create_building_sprite() -> str:
    """Create a medieval building sprite."""
    size = (200, 200)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main building
    draw.rectangle([40, 80, 160, 200], fill=(139, 137, 137, 255))
    
    # Roof
    draw.polygon([(30, 80), (100, 30), (170, 80)], fill=(101, 67, 33, 255))
    
    # Door
    draw.rectangle([85, 140, 115, 200], fill=(101, 67, 33, 255))
    
    # Windows
    draw.rectangle([50, 100, 70, 130], fill=(255, 255, 200, 200))
    draw.rectangle([130, 100, 150, 130], fill=(255, 255, 200, 200))
    
    filepath = "assets/sprites/building.png"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    return filepath


def create_ground_texture() -> str:
    """Create a grass ground texture."""
    size = (256, 256)
    img = Image.new('RGB', size, (34, 139, 34))
    draw = ImageDraw.Draw(img)
    
    # Add some variation
    import random
    random.seed(42)
    for _ in range(500):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        shade = random.randint(-20, 20)
        r = max(0, min(255, 34 + shade))
        g = max(0, min(255, 139 + shade))
        b = max(0, min(255, 34 + shade))
        draw.point((x, y), fill=(r, g, b))
    
    filepath = "assets/textures/ground.png"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    return filepath


class Party:
    """Manages the party of 4 heroes."""
    
    def __init__(self):
        self.heroes: List[Hero] = []
        self.position = Vec3(0, 0, 0)
        self.rotation_y = 0
        self.selected_index = 0
        
    def add_hero(self, hero: Hero):
        """Add a hero to the party."""
        if len(self.heroes) < 4:
            self.heroes.append(hero)
            
    def get_selected_hero(self) -> Optional[Hero]:
        """Get the currently selected hero."""
        if self.heroes and 0 <= self.selected_index < len(self.heroes):
            return self.heroes[self.selected_index]
        return None


class GameObject(Entity):
    """Base game object with sprite support."""
    
    def __init__(self, sprite_path: str, position: Vec3 = Vec3(0, 0, 0), **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.sprite_path = sprite_path
        
        # Create billboard sprite (always faces camera)
        self.billboard = Billboard(parent=self, texture=sprite_path, scale=(2, 2, 2))
        
        # Collision box
        self.collider = BoxCollider(self, center=Vec3(0, 1, 0), size=Vec3(1, 2, 1))


class MM7Game:
    """Main game class - MM7 style with HoMM3 atmosphere."""
    
    def __init__(self):
        self.app = Ursina()
        self.title = "MM7 Clone - HoMM3 Style"
        self.window.borderless = False
        self.window.fullscreen = False
        self.window.resolution = (1280, 720)
        
        # Generate assets
        print("Generating assets...")
        self.ground_texture = create_ground_texture()
        self.tree_sprite = create_tree_sprite()
        self.building_sprite = create_building_sprite()
        
        # Create hero sprites
        self.hero_sprites = {}
        hero_colors = [
            (200, 50, 50),   # Knight - Red
            (255, 255, 255), # Cleric - White
            (50, 150, 50),   # Ranger - Green
            (100, 100, 255), # Sorcerer - Blue
        ]
        
        for i, hero_class in enumerate(HeroClass):
            self.hero_sprites[hero_class] = create_hero_sprite(
                hero_class, hero_colors[i]
            )
        
        # Initialize party
        self.party = Party()
        self.create_initial_party()
        
        # Setup scene
        self.setup_scene()
        
        # UI elements
        self.ui_visible = True
        self.setup_ui()
        
        # Movement
        self.movement_speed = 10
        self.rotation_speed = 100
        
        # Camera settings (first person view like MM7)
        camera.position = Vec3(0, 2, 0)
        camera.rotation_x = 0
        
        # Skybox
        Sky(texture='sky_sunset')
        
        # Fog for atmosphere
        scene.fog_density = (10, 50)
        scene.fog_color = color.rgb(200, 180, 150)
        
        # Bind input and update methods
        self.app.input = self.input
        self.app.update = self.update
        
        print("Game initialized!")
        print(f"Party: {len(self.party.heroes)} heroes")
        for hero in self.party.heroes:
            print(f"  - {hero}")
    
    def run(self):
        """Run the game loop."""
        self.app.run()
    
    def create_initial_party(self):
        """Create initial party of 4 heroes."""
        heroes_data = [
            ("Sir Roland", HeroClass.KNIGHT),
            ("Brother Marcus", HeroClass.CLERIC),
            ("Elara Windrunner", HeroClass.RANGER),
            ("Morwyn Shadowfire", HeroClass.SORCERER),
        ]
        
        for name, hero_class in heroes_data:
            hero = Hero(name=name, hero_class=hero_class)
            self.party.add_hero(hero)
    
    def setup_scene(self):
        """Setup the 3D scene."""
        # Ground plane
        self.ground = Entity(
            model='plane',
            texture=self.ground_texture,
            scale=(100, 100, 100),
            texture_scale=(20, 20),
            collider='box'
        )
        
        # Add trees
        self.trees = []
        tree_positions = [
            Vec3(10, 0, 10),
            Vec3(-15, 0, 20),
            Vec3(25, 0, -10),
            Vec3(-20, 0, -25),
            Vec3(30, 0, 30),
        ]
        
        for pos in tree_positions:
            tree = GameObject(self.tree_sprite, position=pos)
            self.trees.append(tree)
        
        # Add buildings
        self.buildings = []
        building_positions = [
            Vec3(0, 0, -40),
            Vec3(-30, 0, -30),
        ]
        
        for pos in building_positions:
            building = GameObject(
                self.building_sprite,
                position=pos,
                scale=Vec3(3, 3, 3)
            )
            self.buildings.append(building)
        
        # Add lighting
        AmbientLight(color=color.rgba(100, 100, 100, 100))
        DirectionalLight(color=color.rgba(255, 255, 200, 150), direction=Vec3(1, -1, -1))
    
    def setup_ui(self):
        """Setup user interface."""
        # Party panel at bottom
        self.party_panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(0, 0, 0, 150),
            scale=(0.9, 0.25),
            position=(0, -0.4)
        )
        
        # Hero portraits and stats
        self.hero_frames = []
        self.hero_texts = []
        
        for i in range(4):
            frame_x = -0.35 + (i * 0.23)
            
            # Frame border
            frame = Entity(
                parent=camera.ui,
                model='quad',
                color=color.rgba(100, 80, 60, 200),
                scale=(0.2, 0.22),
                position=(frame_x, -0.4)
            )
            self.hero_frames.append(frame)
            
            # Hero info text
            if i < len(self.party.heroes):
                hero = self.party.heroes[i]
                text_str = f"{hero.name}\n{hero.hero_class.value}\nHP: {hero.hp}/{hero.max_hp}\nMP: {hero.mp}/{hero.max_mp}"
                text = Text(
                    text=text_str,
                    position=(frame_x - 0.09, -0.45),
                    scale=0.6,
                    color=color.white
                )
                self.hero_texts.append(text)
            else:
                self.hero_texts.append(None)
        
        # Compass / Minimap indicator
        self.compass_text = Text(
            text="N",
            position=(0.45, 0.45),
            scale=1.5,
            color=color.yellow
        )
        
        # Instructions
        self.instructions = Text(
            text="WASD: Move | Mouse: Look | 1-4: Select Hero | Space: Rest",
            position=(-0.9, 0.45),
            scale=0.7,
            color=color.white
        )
        
        self.update_ui()
    
    def update_ui(self):
        """Update UI elements."""
        # Highlight selected hero
        for i, frame in enumerate(self.hero_frames):
            if i == self.party.selected_index:
                frame.color = color.rgba(200, 150, 50, 255)
            else:
                frame.color = color.rgba(100, 80, 60, 200)
        
        # Update compass based on rotation
        angles = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = int((camera.rotation_y % 360) / 45) % 8
        self.compass_text.text = angles[index]
    
    def input(self, key):
        """Handle input."""
        # Hero selection
        if key in ['1', '2', '3', '4']:
            idx = int(key) - 1
            if idx < len(self.party.heroes):
                self.party.selected_index = idx
                self.update_ui()
        
        # Rest action
        if key == 'space':
            selected = self.party.get_selected_hero()
            if selected:
                selected.hp = selected.max_hp
                selected.mp = selected.max_mp
                print(f"{selected.name} rested and recovered!")
                self.update_ui()
        
        # Toggle UI
        if key == 'tab':
            self.ui_visible = not self.ui_visible
            self.party_panel.visible = self.ui_visible
            for frame in self.hero_frames:
                frame.visible = self.ui_visible
            for text in self.hero_texts:
                if text:
                    text.visible = self.ui_visible
            self.compass_text.visible = self.ui_visible
            self.instructions.visible = self.ui_visible
    
    def update(self, dt):
        """Update game logic."""
        # First person movement (MM7 style)
        if held_keys['w']:
            camera.position += camera.forward * self.movement_speed * dt
        if held_keys['s']:
            camera.position -= camera.forward * self.movement_speed * dt
        if held_keys['a']:
            camera.position -= camera.right * self.movement_speed * dt
        if held_keys['d']:
            camera.position += camera.right * self.movement_speed * dt
        
        # Mouse look
        if mouse.velocity != Vec3(0, 0, 0):
            camera.rotation_y -= mouse.velocity[0] * self.rotation_speed * dt
        
        # Keep camera at proper height
        camera.y = 2
        
        # Update party position
        self.party.position = camera.position
        self.party.rotation_y = camera.rotation_y
        
        # Boundary check
        if abs(camera.x) > 50:
            camera.x = 50 if camera.x > 0 else -50
        if abs(camera.z) > 50:
            camera.z = 50 if camera.z > 0 else -50
        
        self.update_ui()


def main():
    """Main entry point."""
    print("=" * 50)
    print("MM7 Clone - HoMM3 Style")
    print("=" * 50)
    print("\nStarting game...")
    
    game = MM7Game()
    game.run()


if __name__ == "__main__":
    main()
