### Risk
A simple script for calculating the likely outcome of a Risk battle.

## Arguments
The script takes in the number of attackers and defenders as arguments.

## Returns
The likelihood of victory, and the average number of survivors (attackers).

## Usage
I have an 11 stack, should I attack that 10 stack? Let's find out!

```sh
yarn risk 10 10 ## likelihood of victory 52.8% with 2.41 survivors on average
```

We can't attack with all 11 stacks, because we have to leave one behind. So when we attack we'll have 10 attacking into 10. The script tells us we have a 52.8% chance of winning, and on average we'll have 2.41 survivors (3.41 if you include the stack left behind).
