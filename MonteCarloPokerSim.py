import random
import itertools
from collections import Counter

def make_deck():

    suits = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    return deck

def card_value(rank):

    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
              '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return values[rank]

def is_straight(ranks):

    ranks = sorted(set(ranks), reverse=True)
    if len(ranks) < 5:
        return False
    
    for i in range(len(ranks) - 4):
        if ranks[i] - ranks[i+4] == 4:
            return ranks[i]
    
    if set([14, 5, 4, 3, 2]).issubset(set(ranks)):
        return 5
    
    return False

def is_flush(suits):

    suit_counts = Counter(suits)
    for suit, count in suit_counts.items():
        if count >= 5:
            return suit
    return False

def evaluate_5_card_hand(five_cards):

    ranks = [card_value(card[0]) for card in five_cards]
    suits = [card[1] for card in five_cards]
    
    rank_counts = Counter(ranks)
    rank_count_values = sorted(rank_counts.values(), reverse=True)
    
    is_flush_suit = is_flush(suits)
    straight_high = is_straight(ranks)
    
    if is_flush_suit and straight_high:
        return (8, [straight_high])
    
    if rank_count_values == [4, 1]:
        four_rank = [rank for rank, count in rank_counts.items() if count == 4][0]
        kicker = [rank for rank, count in rank_counts.items() if count == 1][0]
        return (7, [four_rank, kicker])
    
    if rank_count_values == [3, 2]:
        three_rank = [rank for rank, count in rank_counts.items() if count == 3][0]
        two_rank = [rank for rank, count in rank_counts.items() if count == 2][0]
        return (6, [three_rank, two_rank])
    
    if is_flush_suit:
        flush_ranks = sorted([rank for rank in ranks], reverse=True)
        return (5, flush_ranks)
    
    if straight_high:
        return (4, [straight_high])
    
    if rank_count_values == [3, 1, 1]:
        three_rank = [rank for rank, count in rank_counts.items() if count == 3][0]
        kickers = sorted([rank for rank, count in rank_counts.items() if count == 1], reverse=True)
        return (3, [three_rank] + kickers)
    
    if rank_count_values == [2, 2, 1]:
        pairs = sorted([rank for rank, count in rank_counts.items() if count == 2], reverse=True)
        kicker = [rank for rank, count in rank_counts.items() if count == 1][0]
        return (2, pairs + [kicker])
    
    if rank_count_values == [2, 1, 1, 1]:
        pair_rank = [rank for rank, count in rank_counts.items() if count == 2][0]
        kickers = sorted([rank for rank, count in rank_counts.items() if count == 1], reverse=True)
        return (1, [pair_rank] + kickers)
    
    return (0, sorted(ranks, reverse=True))

def evaluate_poker_hand(cards):

    if len(cards) != 7:
        return (0, [])
    
    best_hand = None
    best_rank = -1
    
    for combo in itertools.combinations(cards, 5):
        rank, tie_breakers = evaluate_5_card_hand(combo)
        if rank > best_rank or (rank == best_rank and tie_breakers > best_hand[1]):
            best_hand = (rank, tie_breakers)
            best_rank = rank
    
    return best_hand

def would_villain_play(cards, range_percent):

    rank1, suit1 = cards[0][0], cards[0][1]
    rank2, suit2 = cards[1][0], cards[1][1]
    
    val1 = card_value(rank1)
    val2 = card_value(rank2)
    
    strength = 0
    
    if rank1 == rank2:  # Pocket pair
        strength = val1 * 8
    else:  # Non-pair
        strength = (val1 + val2) * 3
        
        if suit1 == suit2:  # Suited
            strength += 10
        
        if abs(val1 - val2) <= 1:  # Connected
            strength += 8
        elif abs(val1 - val2) <= 3:  # Semi-connected
            strength += 4
    
    max_strength = 14 * 8
    percentile = (strength / max_strength) * 100
    
    return percentile >= (100 - range_percent)

def display_prompt():
    print("Format: rank + suit (e.g., As = Ace of spades, Kh = King of hearts)")

def get_card_input(prompt):

    while True:
        card = input(prompt).strip().upper()
        if len(card) == 2 and card[0] in '23456789TJQKA' and card[1] in 'SHDC':
            return card
        print("Invalid card format. Use format like 'As', 'Kh', 'Qd', 'Jc'")

def select_cards():

    print("\n" + "="*50)
    print("POKER MONTE CARLO SIMULATOR")
    print("="*50)
    
    display_prompt()    

    player_cards = []
    print(f"\nSelect your 2 hole cards:")
    
    for i in range(2):
        while True:
            card = get_card_input(f"Card {i+1}: ")
            if card in player_cards:
                print("Card already selected. Choose a different card.")
            else:
                player_cards.append(card)
                break
    
    return player_cards

def select_opponent():

    opponents = {
        "1": ("Rishi", 85),
        "2": ("Jack", 70), 
        "3": ("Tony", 75),
        "4": ("Chetty", 65),
        "5": ("Caius", 60),
        "6": ("Aryan", 45),
        "7": ("Sachin", 40),
        "8": ("Rowan", 20)
    }
    
    print("\nSelect your opponent:")
    print("-" * 30)
    for key, (name, range_val) in opponents.items():
        print(f"{key}. {name} ({range_val}% range)")
    
    while True:
        choice = input("\nEnter opponent number (1-8): ").strip()
        if choice in opponents:
            return opponents[choice]
        print("Invalid choice. Please enter 1-8.")

def get_iterations():

    while True:
        try:
            iterations = int(input("\nEnter number of simulations (100-10000): "))
            if 100 <= iterations <= 10000:
                return iterations
            print("Please enter a number between 100 and 10000.")
        except ValueError:
            print("Please enter a valid number.")

def run_simulation(player_cards, opponent_name, opponent_range, iterations):

    print(f"\nRunning {iterations:,} simulations...")
    print(f"Your hand: {player_cards[0]} {player_cards[1]}")
    print(f"Opponent: {opponent_name} ({opponent_range}% range)")
    print("-" * 50)
    
    wins = 0
    ties = 0
    hands_played = 0
    attempts = 0
    max_attempts = iterations * 20  # Allow more attempts to find valid hands
    
    while hands_played < iterations and attempts < max_attempts:
        attempts += 1
        
        deck = make_deck()
        
        # Remove player cards from deck
        for card in player_cards:
            if card in deck:
                deck.remove(card)
        
        random.shuffle(deck)
        
        # Deal opponent cards
        villain_cards = deck[:2]
        remaining_deck = deck[2:]
        
        # Check if villain would play this hand
        if not would_villain_play(villain_cards, opponent_range):
            continue
        
        # Deal board
        board = remaining_deck[:5]
        
        # Evaluate hands
        hero_hand = player_cards + board
        villain_hand = villain_cards + board
        
        hero_rank, hero_ties = evaluate_poker_hand(hero_hand)
        villain_rank, villain_ties = evaluate_poker_hand(villain_hand)
        
        # Compare hands
        if hero_rank > villain_rank:
            wins += 1
        elif hero_rank == villain_rank:
            if hero_ties > villain_ties:
                wins += 1
            elif hero_ties == villain_ties:
                ties += 1
        
        hands_played += 1
        
        # Show progress
        if hands_played % max(1, iterations // 10) == 0:
            progress = (hands_played / iterations) * 100
            print(f"Progress: {progress:.0f}% ({hands_played:,}/{iterations:,} hands)")
    
    return wins, ties, hands_played

def display_results(player_cards, opponent_name, opponent_range, wins, ties, hands_played):

    print("\n" + "="*50)
    print("SIMULATION RESULTS")
    print("="*50)
    
    print(f"Your Hand: {player_cards[0]} {player_cards[1]}")
    print(f"vs {opponent_name} ({opponent_range}% range)")
    print(f"Hands Played: {hands_played:,}")
    print("-" * 30)
    
    if hands_played > 0:
        win_rate = (wins / hands_played) * 100
        tie_rate = (ties / hands_played) * 100
        loss_rate = 100 - win_rate - tie_rate
        
        print(f"Win Rate:  {win_rate:.1f}%")
        print(f"Tie Rate:  {tie_rate:.1f}%")
        print(f"Loss Rate: {loss_rate:.1f}%")
        print("-" * 30)
        
        # Give recommendation based on win rate
        if win_rate >= 65:
            recommendation = "RAISE"
            advice = "Strong hand - play aggressively!"
        elif win_rate >= 50:
            recommendation = "CALL"
            advice = "Decent hand - proceed with caution"
        else:
            recommendation = "FOLD"
            advice = "Weak hand - consider folding"
        
        print(f"Recommendation: {recommendation}")
        print(f"Advice: {advice}")
    else:
        print("No valid hands were played in the simulation.")
        print("This might happen with very tight opponent ranges.")

def main():

    while True:
        player_cards = select_cards()
        opponent_name, opponent_range = select_opponent()
        iterations = get_iterations()
        
        # Run simulation
        wins, ties, hands_played = run_simulation(player_cards, opponent_name, opponent_range, iterations)
        
        # Show results
        display_results(player_cards, opponent_name, opponent_range, wins, ties, hands_played)
        

        print("\n" + "="*50)
        choice = input("Run another simulation? (y/n): ").strip().lower()
        if choice not in ['y']:
            print("Thanks for using the Poker Monte Carlo Simulator!")
            break

if __name__ == "__main__":
    main()