// Spell reference name, PixelFX source, in-game use, and effect-specific settings.
export const trees = {
  fire: [
    ["Fire Bolt", "fire/fireball", "Small right-facing projectile", { radius: 2, speed: 49 }],
    ["Warmth", "custom/warmth", "Passive mana recovery aura around the caster"],
    ["Inferno", "fire/flamethrower", "Continuous right-facing flame jet"],
    ["Blaze", "custom/blaze", "Place persistent flame trail segments at previous caster positions"],
    ["Fire Ball", "fire/fireball", "Heavy right-facing projectile", { radius: 8, speed: 129 }],
    ["Fire Wall", "custom/fire-wall", "Persistent horizontal barrier of flame"],
    ["Enchant", "fire/spirit-flame", "Flame to attach to the enchanted weapon"],
    ["Meteor", "fire/meteor", "Falling fire mass and ground impact"],
    ["Fire Mastery", "fire/fire-tornado", "Optional passive upgrade flourish"],
    ["Hydra", "custom/hydra", "Triple flame familiar turret"],
  ],
  cold: [
    ["Ice Bolt", "projectiles/magic-missile", "Small right-facing cold projectile"],
    ["Frozen Armor", "custom/frozen-armor", "Thin frost guard that keeps the caster readable"],
    ["Frost Nova", "ice/frost-nova", "Expanding ground-level wave"],
    ["Ice Blast", "ice/ice-shatter", "Burst of ice shards at the target"],
    ["Shiver Armor", "custom/shiver-armor", "Ring of raised spikes at the caster"],
    ["Glacial Spike", "ice/ice-lance", "Large right-facing spear-shaped projectile", { length: 27 }],
    ["Blizzard", "custom/blizzard", "Sustained staggered ice strikes across an area"],
    ["Chilling Armor", "scifi/force-field", "Dome used to signal projectile defense"],
    ["Frozen Orb", "arcane/arcane-orb", "Spinning cold orb shedding ice motes"],
    ["Cold Mastery", "ice/snowflake-burst", "Optional passive upgrade flourish"],
  ],
  lightning: [
    ["Charged Bolt", "custom/charged-bolt", "Three short ground arcs moving right"],
    ["Static Field", "custom/static-field", "Low expanding electric field"],
    ["Telekinesis", "custom/telekinesis", "Remote pull with a converging field at the target"],
    ["Nova", "lightning/thunderclap", "Electric area burst around the caster"],
    ["Lightning", "arcane/arcane-beam", "Sustained straight right-facing electric beam"],
    ["Chain Lightning", "lightning/chain-lightning", "Sequential links between targets"],
    ["Teleport", "arcane/blink-in", "Arrival burst at the destination"],
    ["Thunder Storm", "lightning/lightning-strike", "Vertical strike at the chosen target"],
    ["Energy Shield", "holy/divine-shield", "Sustained protection around the caster"],
    ["Lightning Mastery", "lightning/charge-up", "Optional passive upgrade flourish"],
  ],
};

// Colors are drawn from project.json. Each ramp is ordered dark to light.
export const ramps = {
  fire: ["#4F3333", "#6A4757", "#8B6755", "#D88475", "#EAB853", "#F8CFAB", "#F0FCFF"],
  cold: ["#28283F", "#354568", "#367CB0", "#589DC8", "#91C7C0", "#ADE9FF", "#F0FCFF"],
  lightning: ["#28283F", "#393B5B", "#505276", "#367CB0", "#589DC8", "#78CBF4", "#ADE9FF", "#F0FCFF"],
};
