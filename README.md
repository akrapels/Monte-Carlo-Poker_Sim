# Poker Simulator

A simple poker hand simulator that calculates win rates against different opponents using Monte Carlo simulation.

## What it does

- Simulates poker hands against different playing styles
- Calculates win percentages for your cards
- Gives strategic recommendations (raise, call, or fold)

## How to use

1. **Pick your cards**: Enter your 2 cards (like "As" for Ace of spades)
2. **Choose opponent**: Pick from 8 different friends with different playing styles
3. **Set iterations**: Choose how many hands to simulate (100-10,000)
4. **Get results**: See your win rate and recommendation

## Example

```
Your Hand: AH AS
vs Rishi (85% range)
Hands Played: 1,000
------------------------------
Win Rate:  84.8%
Tie Rate:  1.2%
Loss Rate: 14.0%
------------------------------
Recommendation: RAISE
```

## How the math works

The simulator uses **Monte Carlo simulation** to calculate win rates:

1. **Deal random cards**: For each simulation, it deals random opponent cards and community cards
2. **Check if opponent plays**: Only counts hands where the opponent would actually play (based on their style)
3. **Compare hands**: Evaluates both your hand and opponent's hand to see who wins
4. **Count results**: Tracks wins, ties, and losses
5. **Calculate percentage**

### How hand strength is calculated

The program calculates hand strength to decide if opponents will play:

**Pocket Pairs**:
- Strength = rank × 8
- Example: AA = 14 × 8 = 112, 22 = 2 × 8 = 16

**Non-pairs**:
- Strength = (rank1 + rank2) × 3 + bonuses
- **Bonuses**: +10 for suited, +8 for connected, +4 for semi-connected
- Example: AK suited = (14 + 13) × 3 + 10 = 81 + 10 = 91

### How opponents decide to play

Each opponent has a percentage range (like Rishi at 85%):
- The program calculates the strength of their random cards
- **Key calculation**: `percentile = (strength / max_strength) × 100`
- **Decision**: If `percentile >= (100 - range_percent)`, they play the hand

**The math**: 
- Maximum possible strength = 14 × 8 = 112 (AA)
- If opponent gets 72 offsuit: strength = 18, percentile = (18/112) × 100 = 16%
- Since 16% < 15%, Rishi folds this weak hand
- If opponent gets AK suited: strength = 91, percentile = (91/112) × 100 = 81%  
- Since 81% > 15%, Rishi plays this strong hand

## Opponents

- **Rishi (85%)**: Plays almost anything
- **Jack (70%)**: Loose-aggressive
- **Tony (75%)**: Loose player
- **Chetty (65%)**: Moderate-loose
- **Caius (60%)**: Moderate player
- **Aryan (45%)**: Tight-moderate
- **Sachin (40%)**: Tight player
- **Rowan (20%)**: Only plays premium hands

## Why I made this

I wanted to simulate poker hands against my friends' actual playing styles to see how different hands would perform. It's fun to test if that marginal hand is actually profitable against someone who plays too loose, just like my friends.

## Author

Alexander Krapels - alexandermkrapels@gmail.com

