# Algorithm Problem


# coins  [1, 5, 7, 9, 11]
# customer comes in with the 25 amount of money.
# The program should return 3, from 11 + 9 + 5
# Sometimes, our coins left in any branch may need to be made available or sufficient
# for exchange.
# For example, if the sub-branch only has [7, 9] coins, a customer wants to exchange
# for 20.
# The program should return -1


import tensorflow as tf

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Variables
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
global coins
# coins = { "coin_0": 0, "coin_1": 1, "coin_5": 1, "coin_7": 3, "coin_9": 2, "coin_11": 1 }
coins = { "coin_0": 0, "coin_1": 1, "coin_5": 1, "coin_7": 3, "coin_9": 2, "coin_11": 100 }
messsage = { "message" : {} }

global selected_coins
selected_coins = []

global avaliable_coins
global coin_values
global coin_values
global return_amount
global cal_matrix
global pointer
# pointer = tf.constant(int(len(coins) - 1))
pointer = tf.constant( 25 )

global coin_index
coin_index = tf.constant(int(len(coins) - 1))

print( coins )

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Class / Functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def f1():
	global coins
	global pointer
	global coin_index
	global return_amount
	global selected_coins
	global avaliable_coins
	global coin_values
	global cal_matrix
	
	# print( int(pointer) )
	### coin_index conditions
	### If there is avaliable coin to select
	coin_values = [ x for x in coins.values( ) ]
	avaliable_coins = [ int(x.split('_')[1]) for x in coins.keys( ) ]
	
	
	# print( coin_values )
	# print( avaliable_coins )
	# print( return_amount )
	
	if return_amount > 0 :
		
		# 25 - 11 > 0
		# 14 - 11 > 0 
		print( 'return_amount: ' + str( return_amount) + ' coin_index: ' + str( coin_index.numpy() ) + ' avaliable_coins: ' + str( avaliable_coins[coin_index] ) + ' coin_values: ' + str( coin_values[coin_index] ) )
			
		if return_amount - avaliable_coins[coin_index] >= 0 and coin_values[coin_index] > 0 :
	
			return_amount = return_amount - avaliable_coins[coin_index]
			selected_coins.append( avaliable_coins[coin_index] )
			
			### update back calculating coins
			coins[list(coins.keys())[coin_index]] = coins[list(coins.keys())[coin_index]] - 1
			# print(coins[list(coins.keys())[coin_index]])
			# print( coins )
			# print( 'coin_index: ' + str( coin_index.numpy() ) + ' avaliable_coins: ' + str( avaliable_coins[coin_index] ) + ' coin_values: ' + str( coin_values[coin_index] ) )
			
		else :
			print( 'coin_index = coin_index - 1' )
			coin_index = coin_index - 1
			
	if coin_index == -1 :
		coin_index = tf.constant(int(len(coins) - 1))
	
	# if return_amount > 0 and coin_values[coin_index] != 0 :
	
		# if coin_values[coin_index] <= return_amount :
	
			# selected_coins.append( avaliable_coins[coin_index] )
			# return_amount = return_amount - avaliable_coins[coin_index]
			
			# print( 'return_amount' )
			# print( return_amount )
		
			## update back calculating coins
			# coins[list(coins.keys())[coin_index]] = coins[list(coins.keys())[coin_index]] - 1
			# print(coins[list(coins.keys())[coin_index]])
			
		# else :
		
			# coin_index = tf.subtract(coin_index, 1)
		
		# coins[int(coin_index)] = coins[int(coin_index)] - 1
		# print( coins )
		
	
	## It can mixed coins together then condition is select different coins value more than x times
	# if int(pointer) == 0 and tf.reduce_sum(selected_coins).numpy() < return_amount :
	if int(pointer) == 0 and return_amount > 0 :
		selected_coins = [ -1 ]
		messsage["message"][len( messsage["message"] )] = 'No avalibale coin'
	
	elif int(pointer) > 0 and return_amount == 0 :
		messsage["message"][len( messsage["message"] )] = 'Done!'
		pointer = tf.constant( 0 )
	
	else :	
		pointer = tf.subtract(pointer, 1)


	# messsage["message"][len( messsage["message"] )] = 'Done!'

	return
	
def f2():
	global pointer
	
	if ( pointer.numpy() > 0 ):
		messsage["message"][len( messsage["message"] )] = 'No amount to return'
		pointer = tf.constant(0)
		selected_coins.append( -1 )
	
	return

def	calculate_amount_of_coins( return_amount, coins ):
	global selected_coins
	global avaliable_coins
	global coin_values
	global cal_matrix
	global pointer

	coin_values = [ x for x in coins.values( ) ]
	avaliable_coins = [ int(x.split('_')[1]) for x in coins.keys( ) ]
	cal_matrix = tf.ones([ 1, len(avaliable_coins) ]) * return_amount
	cal_matrix = tf.where( tf.math.greater_equal( cal_matrix, avaliable_coins ), avaliable_coins, 0 ).numpy()[0]


	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	r = tf.cond( tf.greater(return_amount, 0), f1, f2 )
	
	return selected_coins


return_amount = 25
print( 'coins: ' )
print( calculate_amount_of_coins( return_amount, coins ) )

print( 'message: ' )
for msg in messsage["message"]:
	print( messsage["message"][msg] )