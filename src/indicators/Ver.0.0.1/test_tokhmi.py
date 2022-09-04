from random import seed
from random import randint
import numpy as np
import tensorflow as tf 

print(tf.__version__)

@tf.function(jit_compile=True)
def mips(qy, db, k=10, recall_target=0.95):
  dists = tf.einsum('ik,jk->ij', qy, db)
  # returns (f32[qy_size, k], i32[qy_size, k])
  return tf.nn.approx_max_k(dists, k=k, recall_target=recall_target)

qy = tf.random.uniform((256,128))
db = tf.random.uniform((2048,128))
dot_products, neighbors = mips(qy, db, k=20)

print(dot_products)
print(neighbors)

# Chromosome = {}

# Chromosome[0] = {
# 		'high_period': 100,
# 		'low_period': 50,
# 		'distance_lines': 0,
# 		'cross_line': 1,
# 		'max_st': 0.1,
# 		'max_tp': 0.2,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}

# Chromosome[1] = {
# 		'high_period': 100,
# 		'low_period': 50,
# 		'distance_lines': 0,
# 		'cross_line': 1,
# 		'max_st': 0.1,
# 		'max_tp': 0.2,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}
# Chromosome[2] = {
# 		'high_period': 100,
# 		'low_period': 50,
# 		'distance_lines': 0,
# 		'cross_line': 1,
# 		'max_st': 0.1,
# 		'max_tp': 0.2,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}
# Chromosome[3] = {
# 		'high_period': 150,
# 		'low_period': 100,
# 		'distance_lines': 2,
# 		'cross_line': 3,
# 		'max_st': 0.3,
# 		'max_tp': 0.4,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}
# Chromosome[4] = {
# 		'high_period': 150,
# 		'low_period': 100,
# 		'distance_lines': 2,
# 		'cross_line': 3,
# 		'max_st': 0.3,
# 		'max_tp': 0.4,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}
# Chromosome[5] = {
# 		'high_period': 150,
# 		'low_period': 100,
# 		'distance_lines': 2,
# 		'cross_line': 3,
# 		'max_st': 0.3,
# 		'max_tp': 0.4,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}

# i = 6
# while i < 12:
# 	max_tp = randint(10, 80)/100
# 	max_st = randint(10, 70)/100
		
# 	while max_tp < max_st:
# 		max_tp = randint(10, 80)/100
# 		max_st = randint(10, 70)/100

# 	Chromosome[i] = {
# 		'high_period': randint(5, 500),
# 		'low_period': randint(5, 400),
# 		'distance_lines': randint(0, 6),
# 		'cross_line': randint(0, 300),
# 		'max_st': max_st,
# 		'max_tp': max_tp,
# 		'signal': None,
# 		'score_buy': 0,
# 		'score_sell': 0
# 		}

# 	if (Chromosome[i]['high_period'] <= Chromosome[i]['low_period'] + 10): continue

# 	i += 1


# for key in Chromosome.keys():
# 	print('1===> ',Chromosome[key])

# for key in Chromosome.keys():
# 	i = 0
# 	while i < len(Chromosome):
# 		if key == i:
# 			i += 1
# 			continue
# 		if (
# 			Chromosome[key]['high_period'] == Chromosome[i]['high_period'] and
# 			Chromosome[key]['low_period'] == Chromosome[i]['low_period'] and
# 			Chromosome[key]['distance_lines'] == Chromosome[i]['distance_lines'] and
# 			Chromosome[key]['cross_line'] == Chromosome[i]['cross_line'] and
# 			Chromosome[key]['max_st'] == Chromosome[i]['max_st'] and
# 			Chromosome[key]['max_tp'] == Chromosome[i]['max_tp']
# 			):

# 			max_tp = randint(10, 80)/100
# 			max_st = randint(10, 70)/100
		
# 			while max_tp < max_st:
# 				max_tp = randint(10, 80)/100
# 				max_st = randint(10, 70)/100

# 			high_period = randint(5, 500)
# 			low_period = randint(5, 400)
# 			while high_period <= low_period + 10:
# 				high_period = randint(5, 500)
# 				low_period = randint(5, 400)

# 			Chromosome[i] = {
# 						'high_period': high_period,
# 						'low_period': low_period,
# 						'distance_lines': randint(0, 6),
# 						'cross_line': randint(0, 300),
# 						'max_st': max_st,
# 						'max_tp': max_tp,
# 						'signal': None,
# 						'score_buy': 0,
# 						'score_sell': 0
# 						}
# 		i += 1
# print()
# for key in Chromosome.keys():
# 	print('2===> ',Chromosome[key])