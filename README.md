## **Motivation**
This is another small project in my quest to learn more about incomplete information games and how reinforcement learning can be used to converge at their optimal strategies.
I have previously implemented the counterfactual regret minimization algorithm for rock-paper-scissors and gained insights on the essence of the algorithm and how it achieves its goal, and
here I decided to implement it on a slightly more complex game called Kuhn Poker.

## **How it works**
First a little bit about Kuhn Poker from my good friend ChatGPT:  

Kuhn Poker is one of the simplest models of a poker game. It was invented by Harold W. Kuhn in 1950 as a way to study strategic decision-making in imperfect-information games.
Because it is small and mathematically tractable, it’s often used in game theory, AI, and poker research as a “toy game” to test strategies like Nash equilibrium and Counterfactual
Regret Minimization (CFR).

Here’s how it works:

### *Setup*
- Players: 2
- Deck: Only 3 cards (commonly Jack, Queen, King or just numbered 1, 2, 3).
- Antes: Each player antes (pays) 1 chip to the pot before cards are dealt.
- Deal: Each player is dealt 1 card (face-down, privately known to them).

### *Betting Rules*
- There is only one round of betting.
- Player 1 (the first to act) can either:
  - Check (bet nothing, pass the option to Player 2), or
  - Bet (wager 1 more chip).

- Player 2 then responds:
  - If Player 1 checked, Player 2 may check back (end betting) or bet.
  - If Player 1 bet, Player 2 may fold (losing the ante) or call (matching the bet).

### *Showdown*
- If betting ends without a fold, both reveal their cards.
- The higher card wins the pot.

### *Payoffs*
- Each player starts with -1 chip (the ante).
- Bets and calls add more chips to the pot.
- The winner takes the pot.

### *Strategy Insights*
- Bluffing exists even in this tiny game. For example, a player holding the lowest card sometimes bets to represent strength and force a fold.
- Mixed strategies are required for optimal play. A Nash equilibrium involves randomization—e.g., betting weak hands with some probability and calling with medium hands part of the time.
- Despite only 3 cards, the game is deep enough to illustrate key ideas in poker: value betting, bluffing, and balance.

Now that we know about Kuhn Poker, let me explain the counterfactual regret minimization algorithm on a high level:  
The CFR algorithm essentially involves self-play, countless times, and in each iteration of the game, the bot compares it's expected pay off from taking various actions,
and quantifies how much it regrets not taking certain actions (with respect to the cumulative expected value of that decision point) in the game tree. It weights these regrets based on the probability of arriving at those information sets due to the opponent (assuming the opponent uses an identical strategy). As the algorithm calculates it's regrets at each infoset, it updates it's strategy at that infoset such that it chooses each action with a probability that is proportional to the running sum of regret values for that action. With each updated strategy at each infoset, it stores a sum of strategies for each infoset and the average of these strategies is what converges to the nash equilibrium strategy, which is the most optimal strategy that guarantees the player to not lose in expectation.  

To investigate the more specific implementation of the algorithm for Kuhn Poker we must first take a look at it's game tree:











