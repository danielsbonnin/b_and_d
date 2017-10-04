# Blocks And Dollars
#### *Django web application for tracking kids' homework, allowance, screen time, and more.*

[Screenshots Album](https://imgur.com/a/jQOnf)
## Table of Contents

* [Features](#features)  
    * [Screen time](#screen-time)
    * [Dollars](#dollars)
    * [Coins](#coins)
    * [Blocks](#blocks)
    * [Coin Store](#coin-store)
* [Setup](#setup)
    * [Raspberry Pi](#raspberry-pi)
    * [Apache](#apache)
* [Usage](#usage)  


Blocks and Dollars is a tool to simplify some repetitive parenting tasks. 

# Features
## Screen Time
Screen time can be highly distracting, so Blocks and Dollars implements a little gentle structure:
* Kids must be logged in to Blocks and Dollars when using screens
    * Kids can log in via web interface from any web-enabled device
* Kids must complete daily requirements before logging in
    * Reading
        * What book
        * Start/end pages
    * Homework completed
        * School/independent study
    * IXL skills completed
        * Online learning platform
* Parents set screentime limits
    * Each child has their own baseline daily screen time limit
 * Kids can purchase screen time
     * A Dollars balance can be used to purchase screen time (Parent sets price)  

[Table of Contents](#table-of-contents)
 # Dollars 
 A virtual "account" simplifies the administration of a child's weekly allowance
 * Parents set the weekly allowance
 * Each child's balance increments daily
 * Dollars represents "actual" money, and kids can ask to exchange at the parent's convenience, or ask to "spend" their Dollars on 
 purchases.
 * A form on the Child page, allows the child to manually alter their balance. 
     * The Dollars form requires a "reason" to be entered.
     * Every transaction is logged, in case an audit is required.  

[Table of Contents](#table-of-contents)

# Blocks and Coins
An incentive system that encourages saving, and enables parents to place weight on purchases they prefer their children to have.

* ### Coins
    * Unit of currency
    * Does **NOT** map to actual currency 
    (e.g. if 1 Coin buys a certain item that costs $5, 2 Coins does not necessarily buy an item worth $10.)
    * Coin prices are decided per-item, for example:  

        Child:
        > How many coins is this skateboard (actual cost($60.00))?

        Parent:
        > 4 coins

        Child:
        > How many coins is this video game? (actual cost($40.00))?

        Parent:
        > 5 coins  
* ### Blocks
    * 5 Blocks earns 1 Coin
    * Blocks accrue weekly or are earned meritoriously
    * Blocks can be removed for disciplinary reasons.
    * The Blocks form requires a "reason".
        * Every transaction is logged, in case an audit is required. 

[Table of Contents](#table-of-contents)

### Coin Store
* Parents can add items to the coin store
    * Coin Store items are visible from the Child portal  

[Table of Contents](#table-of-contents)

## Setup
* ### Raspberry Pi
    * *Coming Soon!*
* ### Apache
    * *Coming Soon!*
## Usage
*Coming Soon!*  

[Table of Contents](#table-of-contents)
