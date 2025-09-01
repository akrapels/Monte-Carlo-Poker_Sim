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
