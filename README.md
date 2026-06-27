# EVOLVING LIFE - FBLA Intro to Programming 2025-2026

**Author:** Prayag Patel  
**Event:** Georgia FBLA Introduction to Programming
**Date:** January 2026

## Project Overview

Evolving Life is a console-based virtual pet simulator that demonstrates object-oriented programming, data persistence modular game design, and realistic pet ownership economics.
Players manage their pet's needs (hunger, thirst, hygiene, happiness, health) while budgeting limited in-game currency ("sparks") to cover ongoing care costs.

**Core Learning Objectives Demonstrated:**
- OOP with classes (Pet, Player)
- JSON file I/O for persistent save states
- Modular function design for game systems
- Input validation and menu-driven interfaces
- Data structures (dictionaries, lists) for game state

Table of Contents

1. Game Features
2. Pet Stats & Mechanics
3. Economy System
4. Save System
5. Credits & Attribution

--------- Game Features ---------

Pet Care System

Feed - Uses 1 Food, lowers Hunger, +5 Happiness
Water - Uses 1 Water, lowers Thirst
Clean - Uses 1 Soap, +30 Hygiene, +5 Happiness
Play - +10 Happiness, -10 Energy, +5 Hunger

Daily Progression

- Day Cycle: Next Day advances time, triggers random events, applies stat decay
- Weekly Allowance: +20 sparks every 7 days
- End-of-Day Summary: Shows sparks balance and total expenses
- Game Over: Pet runs away or dies

Skill Development

Skills: Agility, Intelligence, Strength, Charm
Cost: (Current Level + 1) skill points per upgrade
Earned daily based on pet happiness

What Each Skill Does:

Agility| Reduces daily happiness decay and prevents damage from "tripped while playing" events
Intelligence | Bonus energy recovery (+3 per 9 levels) and Extra happiness from learning events
Strength | Reduces daily hunger/thirst growth and Resists illness during vet checkups
Charm | Reduces hygiene decay and Boosts happiness from positive events

Examples: A Strength 5 pet gains 5 less hunger/thirst daily. An Agility 5 pet turns trip events into neutral outcomes.

--------- Pet Stats & Mechanics ---------

- Hunger: 0-100 (damages health when >70)
- Thirst: 0-100 (damages health when >70)
- Energy: 0-100 (affects play/rest balance)
- Hygiene: 0-100 (damages health when <30)
- Happiness: 0-100 (determines mood & skill gains)
- Health: 0-100 (0 = game over)

**Mood System:**
≤10: "Ran Away" → Game Over
11-30: "Sad"
31-40: "Okay"
41-60: "Happy"
61+: "Energetic"

--------- Economy System ---------

Starting Sparks: 100

Vet: 25 sparks (+40 Health, +5 Happiness)

Income: 20 sparks weekly
Tracks: Current sparks, total expenses, total income

--------- Save System ---------

- 4 Save Slots (slot1-slot4) stored in saves.json
- Auto-save after every day when slot assigned
- Manual Save/Load via menu option 8
- Clear Slot option with confirmation prompt
- Load shows: Pet name + current day

--------- Credits & Attribution ---------

Pygame Saving and Loading Tutorial: Creating Customizable Controls by CDcodes (https://www.youtube.com/watch?v=1UCaiX8ESsQ)
- used for basic format for saving system
