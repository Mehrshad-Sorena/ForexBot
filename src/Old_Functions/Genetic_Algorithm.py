from random import seed
from random import randint

Chromosome = {}
apply_to = {
	0: 'open',
	1: 'close',
	2: 'high',
	3: 'low',
	4: 'HL/2',
	5: 'HLC/3',
	6: 'HLCC/4'
}

range(1)
value = randint(0, 100)

i = 0
while i < 6:
	Chromosome[i] = {
		'sl': '',
		'tp': '',
		'diff_min_max': randint(1, 100),
		'window_size': randint(10, 100),
		'apply_to': apply_to[randint(0, 6)],
		'ma_period': randint(3, 6),
		'macd_slow': randint(10, 100),
		'macd_fast': randint(5, 50),
		'rsi_period': randint(1, 28),
		'tenkan_sen': randint(1, 18),
		'kijun_sen': randint(1, 52),
		'senkou_span': randint(1, 104)
	}
	res = list(Chromosome[i].keys()).index 
	print(res)
	i += 1
