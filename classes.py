import random
import pygame

class Card:
    # Initialize the Card object with suit, rank, and face_up status
    def __init__(self, suit, rank, face_up=True):
        self.suit = suit  # Suit of the card (e.g., hearts, spades)
        self.rank = rank  # Rank of the card (e.g., Ace, 2, King)
        self.face_up = face_up  # Whether the card is face up or face down
        self.card_image_path = f"C:/Users/3 Stars Laptop/Desktop/Game/cards/{rank}_of_{suit}.png"  # Path to card image
        self.card_image = self.load_image()  # Load the image for the card

    # Method to load the card image
    def load_image(self):
        try:
            # Try to load the image file
            image = pygame.image.load(self.card_image_path)
            image = pygame.transform.scale(image, (85, 125))  # Resize image to 80x125
            return image
        except pygame.error:
            # If an error occurs (e.g., file not found), use a placeholder image
            print(f"Error loading image for {self.rank} of {self.suit}")
            placeholder_image = pygame.Surface((80, 125))  # Create a blank white surface
            placeholder_image.fill((255, 255, 255))  # Fill the placeholder with white color
            return placeholder_image
    # Method to flip the card (change its face-up/face-down status)
    def flip(self):
        self.face_up = not self.face_up
    # String representation of the card (e.g., Face Up: King of Hearts)
    def __str__(self):
        return f"{'Face Up' if self.face_up else 'Face Down'}: {self.rank}{self.suit}"

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # List of card suits
    ranks = ['Ace' , '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']  # List of card ranks
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]  # Create the deck of cards
        self.shuffle()
    def shuffle(self):
        random.shuffle(self.cards)  # Shuffle the deck
    def draw_card(self, count=1):
        drawn_cards = []
        for _ in range(count):
            if self.cards:
                drawn_cards.append(self.cards.pop())  # Draw cards from the deck
        return drawn_cards
    def is_empty(self):
        return len(self.cards) == 0  # Check if the deck is empty
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class Tableau:
    def __init__(self):
        self.piles = {i: LinkedList() for i in range(7)}  # Initialize 7 piles as LinkedLists
    def reveal_bottom_face_down(self):
        for i, pile in self.piles.items():
            if not pile.is_empty():
                current_node = pile.head
                while current_node.next is not None:
                    current_node = current_node.next
                last_card = current_node.data
                if not last_card.face_up:
                    last_card.flip()  # Flip the bottom face-down card
                    print(f"Revealed bottom face-down card in Pile {i + 1}: {last_card}")
    def add_card_to_pile(self, pile_index, card):
        if pile_index in self.piles:
            self.piles[pile_index].insert_at_tail(card)  # Add card to the specified pile
    def __str__(self):
        return '\n'.join(f'Pile {i}: {self.piles[i].display()}' for i in range(len(self.piles)))  # Display piles

class Foundation:
    def __init__(self):
        self.piles = [Stack() for _ in range(4)]  # Initialize 4 piles for the foundation
    def add_card_to_foundation(self, pile_index, card):
        if 0 <= pile_index < len(self.piles):
            self.piles[pile_index].push(card)  # Add card to the specified pile in the foundation
    def move_card_from_foundation(self, pile_index):
        card = self.piles[pile_index].pop()  # Move (pop) card from the specified foundation pile
        return card
    def __str__(self):
        return '\n'.join(f'Foundation {i}: {self.piles[i]}' for i in range(len(self.piles)))  # Display foundation piles
    
class waste_pile:
    def __init__(self):
        self.cards = Stack()  # Initialize the stack for the waste pile
    def is_empty(self):
        return self.cards.is_empty()  # Check if the waste pile is empty
    def add_card(self, card):
        self.cards.push(card)  # Add a card to the waste pile
    def remove_card(self):
        return self.cards.pop()  # Remove and return the top card from the waste pile
    def top_card(self):
        return self.cards.peek()  # Return the top card without removing it
    def display(self):
        return self.cards.display()  # Display all cards in the waste pile
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)  # String representation of the waste pile
    
class stockpile:
    def __init__(self):
        self.cards = Queue()  # Initialize the queue for the stockpile
    def is_empty(self):
        return self.cards.is_empty()  # Check if the stockpile is empty
    def add_card(self, card):
        self.cards.enqueue(card)  # Add a card to the stockpile
    def remove_card(self):
        return self.cards.dequeue()  # Remove and return the top card from the stockpile
    def top_card(self):
        return self.cards.peek()  # Return the top card without removing it
    def display(self):
        return self.cards.display()  # Display all cards in the stockpile
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)  # String representation of the stockpile
        
class Game:
    def __init__(self):
        self.deck = Deck()  # Initialize the deck of cards
        self.tableau = Tableau()  # Initialize the tableau piles
        self.foundation = Foundation()  # Initialize the foundation piles
        self.stockpile = stockpile()  # Initialize the stockpile
        self.waste_pile = waste_pile()  # Initialize the waste pile
        self.move_history = Stack()  # Stack to store move history
        self.card_tracking = {}  # Dictionary to track card positions
        self.hint = None  # Placeholder for hint functionality
        for i in range(7):  # Initialize the tableau piles
            pile_cards = []
            for j in range(i + 1):
                card = self.deck.draw_card()[0]
                card.face_up = False  # Cards are face down initially
                pile_cards.append(card)
            pile_cards[-1].face_up = True  # Flip the last card face up
            for card in pile_cards:
                self.tableau.add_card_to_pile(i, card)  # Add cards to tableau
                self.card_tracking[str(card)] = [("Tableau", i)]  # Track card position
        self.initialize_stockpile()  # Initialize the stockpile with remaining cards
        self.log_tableau_state()  # Log the initial state of the tableau

    def move_cards(self, from_pile_name: str, from_index: int, to_index: int, to_pile_name: str, num_cards: int):
        if from_pile_name == "waste" and to_pile_name == "tableau":  # Move from waste to tableau
            if not self.waste_pile.is_empty():
                cards_to_move = self.waste_pile.top_card()  # top card from waste
                if self.is_move_valid(cards_to_move, to_index):  # Validate the move
                    self.save_state()  # Save the current state for undo functionality
                    print(self.waste_pile.remove_card())  # Remove card from waste
                    self.tableau.add_card_to_pile(to_index, cards_to_move)  # Move card to tableau
                    print(f"Moved {num_cards} card(s) from Waste to Tableau pile {to_index}.")
                else:
                    return "Invalid move to tableau pile."
            else:
                return "Waste pile is empty, cannot move."
        elif from_pile_name == "tableau" and to_pile_name == "foundation":  # Move from tableau to foundation
            if num_cards != 1:
                return "Only one card can be moved to foundation at a time."
            else:
                from_pile = self.tableau.piles[from_index]
                if not from_pile.is_empty():
                    top_card = from_pile.get_last()  # Get the top card of the tableau pile
                    destination_pile = self.foundation.piles[to_index]
                    if (destination_pile.is_empty() and top_card.rank == 'Ace') or \
                    (not destination_pile.is_empty() and top_card.suit == destination_pile.peek().suit and
                        self.is_one_rank_lower(destination_pile.peek(), top_card)):  # Validate the move to foundation
                        self.save_state()  # Save the current state for undo functionality
                        from_pile.remove_tail()  # Remove card from tableau
                        destination_pile.push(top_card)  # Add card to foundation
                        print(f"Moved card from Tableau pile {from_index} to Foundation pile {to_index}.")
                        self.tableau.reveal_bottom_face_down()  # Reveal bottom card in tableau
                    else:
                        return "Invalid move to foundation pile from tableau."
        elif from_pile_name == "tableau" and to_pile_name == "tableau":  # Move from tableau to tableau
            source_pile = self.tableau.piles[from_index]
            if not source_pile.is_empty():
                source_pile_size = source_pile.size()
                check_card = source_pile.get_node_at_index(source_pile_size - num_cards )
                print(check_card)
                if self.is_move_valid(check_card, to_index): 
                    print("valid move")
                    self.save_state()  # Validate the move
                    cards_to_move = [source_pile.remove_tail() for _ in range(num_cards)]  # Remove cards from source tableau
                    cards_to_move.reverse()
                    for card in cards_to_move:
                        self.tableau.add_card_to_pile(to_index, card)  # Move cards to target tableau
                    print(f"Moved {num_cards} card(s) from Tableau pile {from_index} to Tableau pile {to_index}.")
                    self.tableau.reveal_bottom_face_down()  # Reveal bottom card in tableau
                else:
                    return "Invalid move to target tableau pile."
        elif from_pile_name == "waste" and to_pile_name == "foundation":  # Move from waste to foundation
            if not self.waste_pile.is_empty():
                card_move = self.waste_pile.top_card()  # Get the top card from the waste
                print(card_move , " cards to move 1")
                destination_pile = self.foundation.piles[to_index]
                if (destination_pile.is_empty() and card_move.rank == 'Ace') or \
                    (not destination_pile.is_empty() and card_move.suit == destination_pile.peek().suit and
                    self.is_one_rank_lower(destination_pile.peek(), card_move)): 
                    self.save_state() # Validate the move to foundation
                    move_card = self.waste_pile.remove_card()  # Remove card from waste pile
                    print(move_card , " cards to move")
                    destination_pile.push(move_card)  # Add card to foundation pile
                    print(f"Moved card from Waste to Foundation pile {to_index}.")
                else:
                    return "Invalid move to foundation pile from waste."
            else:
                return "Waste pile is empty, cannot move."
        else:
            return "Unsupported move type or invalid pile names."
        return ""  # Return empty string if the move is valid

    def find_hint(self):
        # Loop through each tableau pile to find a valid move
        for tableau_idx, tableau_pile in self.tableau.piles.items():
            if not tableau_pile.is_empty():  # Check if the tableau pile is not empty
                top_card = tableau_pile.display()[-1]  # Get the top card of the tableau pile
                # Check if the card can be moved to a foundation pile
                for foundation_idx, foundation_pile in enumerate(self.foundation.piles):
                    if (foundation_pile.is_empty() and top_card.rank == 'Ace') or \
                            (not foundation_pile.is_empty() and top_card.suit == foundation_pile.peek().suit and
                            self.is_one_rank_lower(top_card, foundation_pile.peek())):
                        # Valid move to foundation found, set hint and return
                        self.hint = ('tableau', tableau_idx, 'foundation', foundation_idx, 1)
                        return
                # Check if the card can be moved to another tableau pile
                for other_tableau_idx, other_tableau_pile in self.tableau.piles.items():
                    if other_tableau_idx != tableau_idx and self.is_move_valid(top_card, other_tableau_idx):
                        # Valid move to another tableau pile found, set hint and return
                        self.hint = ('tableau', tableau_idx, 'tableau', other_tableau_idx, 1)
                        return
        # If there are no valid moves in tableau piles, check the waste pile
        if not self.waste_pile.is_empty():
            waste_card = self.waste_pile.top_card()  # Get the top card from the waste pile
            for tableau_idx, tableau_pile in self.tableau.piles.items():
                if self.is_move_valid(waste_card, tableau_idx):  # Check if the card can be moved to a tableau pile
                    # Valid move from waste to tableau found, set hint and return
                    self.hint = ('waste', 0, 'tableau', tableau_idx, 1)
                    return
        # If no valid move is found, set hint to None
        self.hint = None

    def is_move_valid(self, card, to_pile):
        # Check if the destination pile is empty, any card can be placed in an empty pile
        if self.tableau.piles[to_pile].is_empty():
            return True
        # Get the top card of the destination pile
        top_card = self.tableau.piles[to_pile].display()[-1]
        if top_card.face_up:
            # Check if the card is of opposite color and one rank lower than the top card
            print(top_card , "top cards of destination")
            print(self.is_opposite_color(card, top_card) , self.is_one_rank_lower(card, top_card) )
            return (self.is_opposite_color(card, top_card) and self.is_one_rank_lower(card, top_card))
        # If the top card is face-down, the move is not valid
        return False

    def is_opposite_color(self, card1, card2): # check the card is opposite colors 
        print("first 1 ", card1.suit in ['Hearts', 'Diamonds'] and card2.suit in ['Clubs', 'Spades'] )
        print("first 2 ", card1.suit in ['Clubs', 'Spades'] and card2.suit in ['Hearts', 'Diamonds'])
        return (card1.suit in ['Hearts', 'Diamonds'] and card2.suit in ['Clubs', 'Spades']) or \
            (card1.suit in ['Clubs', 'Spades'] and card2.suit in ['Hearts', 'Diamonds'])

    def is_one_rank_lower(self, card1, card2): # check card is one rank lower to other card
        rank_order = self.deck.ranks
        return rank_order.index(card1.rank) == rank_order.index(card2.rank) - 1

    def initialize_stockpile(self): # initialize the stockpile with remaining cards
        remaining_cards = self.deck.draw_card(len(self.deck.cards))
        for card in remaining_cards:
            self.stockpile.add_card(card)

    def log_tableau_state(self): # log the initial state of the tableau
        for i, (key, pile) in enumerate(self.tableau.piles.items()):
            cards = pile.display()
            card_descriptions = []
            
            for card in cards:
                state = 'up' if card.face_up else 'down'
                card_descriptions.append(f"{card.rank} of {card.suit} ({state})")
            
            print(f"Tableau Pile {key}: {', '.join(card_descriptions)}")

    def draw_from_stockpile(self):
        # Check if stockpile has cards, and draw the top card to waste pile
        if not self.stockpile.is_empty():
            # self.save_state()
            drawn_card = self.stockpile.remove_card()
            drawn_card.face_up = True  # Set card face-up
            self.waste_pile.add_card(drawn_card)
            self.card_tracking[str(drawn_card)] = [("Waste Pile", 0)]  # Track the drawn card's position
        # If stockpile is empty, check if waste pile has cards to refill the stockpile
        elif not self.waste_pile.is_empty():
            while not self.waste_pile.is_empty():
                card = self.waste_pile.remove_card()
                card.face_up = False  # Set cards face-down when moving back to stockpile
                self.stockpile.add_card(card)  # Add cards back to stockpile

    def check_win(self):
        # Check if all foundation piles have 13 cards (one of each rank)
        for i, pile in enumerate(self.foundation.piles):
            if pile.size() != 13:
                return False  # If any pile doesn't have 13 cards, the game is not won yet
                
        print("You Win!")  # If all piles have 13 cards, print winning message
        return True  # Return True indicating that the player has won

    def save_state(self):
        # Create a copy of the stockpile with the face-up state of each card
        stockpile_copy = []
        stockpile_copy = self.stockpile.display()
        waste_pile_copy = []
        waste_pile_copy = self.waste_pile.display()
        # Create a copy of the tableau piles with the face-up state of each card
        tableau_cards = {}
        for key, pile in self.tableau.piles.items():
            pile_cards = []
            while not pile.is_empty():
                card = pile.remove_tail()  # Remove cards from the tableau pile
                pile_cards.append((card, card.face_up))  # Store each card's face-up state
            # Restore the tableau piles in reverse order
            for card, _ in reversed(pile_cards):
                pile.insert_at_tail(card)
            tableau_cards[key] = pile_cards  # Store the tableau state
        # Create a copy of the foundation piles with the face-up state of each card
        foundation_cards = []
        for pile in self.foundation.piles:
            pile_cards = []
            while not pile.is_empty():
                card = pile.pop()  # Remove cards from the foundation pile
                pile_cards.append((card, card.face_up))  # Store each card's face-up state
            # Restore the foundation piles in reverse order
            for card, _ in reversed(pile_cards):
                pile.push(card)
            foundation_cards.append(pile_cards)  # Store the foundation state

        # Create a state dictionary containing all the copies
        state = {
            'stockpile': stockpile_copy,
            'waste_pile': waste_pile_copy,
            'tableau': tableau_cards,
            'foundation': foundation_cards
        }
        # Push the state onto the move history stack for undo functionality
        self.move_history.push(state)

    def undo(self):
        # Check if there are any moves in the history to undo
        if self.move_history.size() > 0:
            # Pop the last state from the move history stack
            last_state = self.move_history.pop()

            # Clear the waste pile and restore it from the last state
            self.waste_pile.cards.clear()
            for card in last_state['waste_pile']:
                self.waste_pile.add_card(card)

            # Clear the stockpile and restore it from the last state
            self.stockpile.cards.clear()
            for card in last_state['stockpile']:
                self.stockpile.add_card(card)

            # Restore each tableau pile from the last state
            for pile_key, saved_pile_cards in last_state['tableau'].items():
                self.tableau.piles[pile_key].clear()
                for card, face_up in reversed(saved_pile_cards):
                    card.face_up = face_up  # Restore the face-up state
                    self.tableau.piles[pile_key].insert_at_tail(card)

            # Restore each foundation pile from the last state
            for i, saved_pile_cards in enumerate(last_state['foundation']):
                self.foundation.piles[i].clear()
                for card, face_up in reversed(saved_pile_cards):
                    card.face_up = face_up  # Restore the face-up state
                    self.foundation.piles[i].push(card)

            # Return True to indicate that the undo was successful
            return True

        # Return False if there are no moves to undo
        return False

    def __str__(self):
        # Return a string representation of the current state of the game
        return f"Tableau:\n{self.tableau}\n\nFoundation:\n{self.foundation}\n\nStockpile:\n{self.stockpile}"

class Node:
    def __init__(self, data):
        # Initialize a new node with given data and set next to None
        self.data = data
        self.next = None

class LinkedList:
    
    def __init__(self):
        # Initialize the linked list with the head set to None
        self.head = None

    def is_empty(self):
        # Check if the linked list is empty (i.e., head is None)
        return self.head is None

    def get_last(self):
        # Get the last element in the linked list
        if self.is_empty():
            raise IndexError("Cannot get last element from an empty linked list.")
        current = self.head
        while current.next:  # Traverse to the last node
            current = current.next
        return current.data
    
    def insert_at_head(self, data):
        # Insert a new node with data at the beginning (head) of the linked list
        new_node = Node(data)
        new_node.next = self.head  # Point new node to the current head
        self.head = new_node  # Update head to new node
        
    def insert_at_tail(self, data):
        # Insert a new node with data at the end (tail) of the linked list
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node  # If the list is empty, make new node the head
        else:
            current = self.head
            while current.next:  # Traverse to the last node
                current = current.next
            current.next = new_node  # Add new node at the end
            
    def get_node_at_index(self, index):
        # Get the data of the node at a specific index in the linked list
        if index < 0:
            raise IndexError("Index cannot be negative")
        
        current = self.head
        current_index = 0

        while current:
            if current_index == index:
                return current.data  # Return data when the index is found
            current = current.next
            current_index += 1

        # If we reach here, the index was out of bounds
        raise IndexError("Index out of bounds")
    
    
    def insert_at_index(self, index, data):
        # Insert a new node at a specific index in the linked list
        if index < 0:
            raise IndexError("Index cannot be negative")
        
        new_node = Node(data)
        
        if index == 0:
            self.insert_at_head(data)  # If index is 0, insert at head
            return
        
        current = self.head
        for _ in range(index - 1):  # Traverse to the node before the given index
            if current is None:
                raise IndexError("Index out of bounds")
            current = current.next
        
        # Insert the new node at the given index
        new_node.next = current.next
        current.next = new_node
        
    def remove_tail(self):
        # Remove and return the last node from the linked list
        if self.is_empty():
            raise IndexError("Pop from empty linked list")
        
        current = self.head
        if current.next is None:  # If only one element exists
            value = current.data
            self.head = None  # Set head to None
            return value
        while current.next and current.next.next:  # Traverse to the second last node
            current = current.next
        
        value = current.next.data  # Get the last node's data
        current.next = None  # Remove the last node
        return value
    
    def peek(self):
        # Return the data of the first element in the linked list
        if self.is_empty():
            raise IndexError("Peek from empty linked list")
        return self.head.data
    
    def clear(self):
        # Clear all elements from the linked list
        self.head = None

    def display(self):
        # Return a list of all elements in the linked list
        current = self.head
        elements = []
        while current:  # Traverse through the list and collect the data
            elements.append(current.data)
            current = current.next
        return elements

    def delete(self, key):
        # Delete the first occurrence of the key from the linked list
        current = self.head
        if current and current.data == key:
            self.head = current.next  # If the key is at head, update head
            current = None
            return

        prev = None
        while current and current.data != key:  # Traverse to find the node with the key
            prev = current
            current = current.next

        if current is None:  # If key is not found
            return

        prev.next = current.next  # Remove the node by linking the previous node to the next node
        current = None

    def size(self):
        # Return the number of elements in the linked list
        current = self.head
        count = 0
        while current:  # Traverse the list and count nodes
            count += 1
            current = current.next
        return count

class Stack:
    def __init__(self):
        # Initializes an empty stack
        self.items = []

    def is_empty(self):
        # Returns True if the stack is empty, otherwise False
        return len(self.items) == 0

    def push(self, item):
        # Adds an item to the top of the stack
        self.items.append(item)

    def clear(self):
        """Clears all items from the stack."""
        self.items = []

    def pop(self):
        # Removes and returns the top item from the stack
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    def peek(self):
        # Returns the top item from the stack without removing it
        if not self.is_empty():
            return self.items[-1]
        else:
            print("peek from empty stack")
            return -1

    def size(self):
        # Returns the number of items in the stack
        return len(self.items)

    def display(self):
        # Returns a copy of the items in the stack
        return self.items.copy()

    def __str__(self):
        # String representation of the stack
        return str(self.items)


class Queue:
    def __init__(self):
        # Initializes an empty queue
        self.items = []

    def is_empty(self):
        # Returns True if the queue is empty, otherwise False
        return len(self.items) == 0

    def enqueue(self, item):
        # Adds an item to the end of the queue
        self.items.append(item)

    def dequeue(self):
        # Removes and returns the front item from the queue
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("dequeue from empty queue")

    def clear(self):
        """Clears all items from the queue."""
        self.items = []

    def peek(self):
        # Returns the front item of the queue without removing it
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("peek from empty queue")

    def size(self):
        # Returns the number of items in the queue
        return len(self.items)

    def display(self):
        # Returns a copy of the items in the queue
        return self.items[:]

    def __str__(self):
        # String representation of the queue
        return str(self.items)
