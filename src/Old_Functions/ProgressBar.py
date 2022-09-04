from progress.bar import Bar

with Bar('Processing', max=1000) as bar:
    for i in range(1000):
        # Do some work
        bar.next()