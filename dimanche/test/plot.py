import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot()

ax.axis([0, 10, 0, 10])

ax.text(3, 5, "le prix de l'√©lectricit√©: ", style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})



plt.show()