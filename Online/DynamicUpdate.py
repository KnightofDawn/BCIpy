import matplotlib.pyplot as plt


# used to dynamically update data
class DynamicUpdate(object):
    def __init__(self, nChan):
        # Set up plot
        self.nChan = nChan
        self.figure, self.ax = plt.subplots(nChan, sharex=True)
        if nChan > 1:
            self.lines = {}
            for i in range(nChan):
                self.lines[i], = self.ax[i].plot([], [])
                # self.ax[i].set_ylim([-1,1])
                # Auto scale on unknown axis
                self.ax[i].set_autoscaley_on(True)
        else:
            self.lines = self.ax.plot([], [])
            # self.ax.set_autoscaley_on(True)
        self.figure.show()

    def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)
        if self.nChan > 1:
            for i in range(self.nChan):
                self.lines[i].set_xdata(xdata)
                self.lines[i].set_ydata(ydata[:, i])
                # Need both of these in order to scale
                self.ax[i].relim()
                self.ax[i].autoscale_view()
        else:
            self.lines.set_xdata(xdata)
            self.lines.set_ydata(ydata)
            # Need both of these in order to scale
            self.ax.relim()
            self.ax.autoscale_view()

        # Need to draw and flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def close(self):
        self.figure.close()

    # run
    def __call__(self, data):
        # update data
        self.on_running(range(data.shape[0]), data)
