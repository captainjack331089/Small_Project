#coding: utf8
#card suits: '♣', '♠', '♦', '♥'

from random import shuffle

#初始化一副牌
def shuffle_card():
    """
    初始化一副52张的牌
    :return:
    """
    suits = ['♠', '♣', '♦', '♥']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []

    for suit in suits:
        for card in cards:
            deck.append(suit + ' ' + card )

    shuffle(deck)
    return(deck)

#依次给玩家，庄家，玩家，庄家各发两张牌
def deal_card(deck, hand_card):
    """
    给参与者（庄家和玩家）发牌
    :return:
    """
    d_card = deck.pop()
    hand_card.append(d_card)
    return d_card

#要的话继续调用deal_card()，并计算，如果爆掉，打印'玩家输了！'
## 计算手牌
def calculate_hand(hand_card):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10,
              'A': 11}
    sum = 0
    ace_count = 0
    for i in hand_card:
        if values[i[2:]] == 11:
            ace_count += 1
        sum += values[i[2:]]
        if sum > 21 and ace_count > 0:
            sum -= 10
            ace_count -= 1
    # print('ace count = %d' %ace_count)
    # print('sum = %d' %sum )
    return sum

##check玩家的牌是不是blackjack， 如果是，check dealer的手牌。
def is_Blackjack(hand_card):
    sum = calculate_hand(hand_card)
    if sum == 21:
        return True
    else:
        return False
##check是不是爆掉了
def is_boosted(hand_card):
    sum = calculate_hand(hand_card)
    if sum > 21:
        return True
    else:
        return False

def blackjack():
    print('Game is Started!')
    deck = shuffle_card()
    dealer_hand = []
    player_hand = []
    count = -1

    print('现在开始发牌！')

    for i in range(2):
        deal_card(deck, player_hand)
        deal_card(deck, dealer_hand)
    myhand = '你手中的牌为： %s %s' %(player_hand[0], player_hand[1])
    hisrealhand = 'dealer的手牌为： %s %s' %(dealer_hand[0], dealer_hand[1])
    hishand = 'dealer的手牌为： 未知 %s' %dealer_hand[1]
    print(myhand)
    print(hishand)

    if is_Blackjack(player_hand) and is_Blackjack(dealer_hand):
        print('Draw! Next Round!')
    elif is_Blackjack(player_hand) and not is_Blackjack(dealer_hand):
        print('Player Win!')
    elif is_Blackjack(dealer_hand) and not is_Blackjack(player_hand):
        print('Dealer Win!')
        print('Dealer 手牌为： %s %s' %(dealer_hand[0],dealer_hand[1]))


    choice = input('要不要继续发牌？y/n： ')
    while choice in ('y' or 'Y'):
        deal_card(deck, player_hand)
        print('给你发了一张: %s' %player_hand[-1])
        myhand += ' ' + player_hand[-1]
        print('你现在的手牌为： ' + myhand)
        if is_boosted(player_hand):
            print('你爆了！下一局。。。')
            return
        else:
            choice = input('要不要继续发牌？y/n： ')

    if choice == 'n' or 'N':
        print('看下庄家牌：')
        print('庄家手牌为：' + hisrealhand)

        while calculate_hand(dealer_hand) < 17:
            print('Dealer 没有到17， 给dealer发牌！')
            deal_card(deck, dealer_hand)
            print('Dealer发了一张: %s' % dealer_hand[-1])
            hisrealhand += ' ' + dealer_hand[-1]
            print('Dealer 现在的手牌为： ' + hisrealhand)
            if is_boosted(dealer_hand):
                print('Dealer 爆了！你赢了！')
                return

        print('Dealer 牌发完了！现在计算谁获胜！')
        print('玩家手牌为: ' + myhand)
        print('Dealer 手牌为: ' + hisrealhand)
        if calculate_hand(dealer_hand) > calculate_hand(player_hand):
            print('Dealer 获胜！')
        elif calculate_hand(dealer_hand) < calculate_hand(player_hand):
            print('玩家获胜')
        else:
            print('打平!')



blackjack()