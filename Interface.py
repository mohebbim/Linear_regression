import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style, cm, animation
from tkinter import Frame,Tk,Label,Entry,Button,Text,Scrollbar,VERTICAL,END,ttk
from tkinter.filedialog import askopenfilename
from mpl_toolkits.mplot3d import axes3d
import tkinter as tk
# plt.switch_backend('TkAgg')
style.use('bmh')
LARGE_FONT = ("Verdana", 15)
TEXT_BOX_FONT = ("consolas", 13)
fig= plt.figure()
# mng = plt.get_current_fig_manager()
graph1 = fig.add_subplot(224, axisbg='white')
ctmap = fig.add_subplot(121, axisbg='white')
surface = fig.add_subplot(222, projection='3d', axisbg='white')
line, = graph1.plot([], [])
ctmap_infotext = ctmap.text(0.002, 0.002, '', transform=ctmap.transAxes, style='italic',
                                      bbox={'facecolor': 'yellow', 'alpha': 0.5, 'pad': 10})
class Interface(Frame):
    def __init__(self, window,**kwargs):
        Frame.__init__(self, window)


        self.iteration_program=0
        self.learningRate = 0.01
        self.iteration_num = 100
        self.b = 0
        self.m = 0
        self.data = []
        self.x = []
        self.y = []
        self.widges()


        ####--- Adding the UI widgets in our window Frame---#######

        # LABELS
    def widges (self):
        self.lblb = Label(root, text="Initial intercept", font=LARGE_FONT)
        self.lblb.place(x=400,y=6)

        self.lblm = Label(root, text="Initial slope", font=LARGE_FONT)
        self.lblm.place(x=400,y=35)

        self.lbllr = Label(root, text="learning rate", font=LARGE_FONT)
        self.lbllr.place(x=400,y=62)

        self.lbliter = Label(root, text="num_iteration", font=LARGE_FONT)
        self.lbliter.place(x=400,y=90)

        self.lblbrowse = Label(root, text="Load your data first!", fg='red', font=("Helvetica", 20))
        self.lblbrowse.place(x=25, y=8)
        # ENTRIES
        self.txtb = Entry(root)
        self.txtb.place(x=600, y=8)
        self.txtb.insert(0, self.b)

        self.txtm = Entry(root)
        self.txtm.place(x=600, y=38)
        self.txtm.insert(0, self.m)

        self.txtlr = Entry(root)
        self.txtlr.place(x=600, y=68)
        self.txtlr.insert(0, self.learningRate)

        self.txtiter = Entry(root)
        self.txtiter.place(x=600, y=97)
        self.txtiter.insert(0, self.iteration_num)

        # BUTTONS

        self.Button_browse = Button(root, text="Brows-CSV", command=self.browser)
        self.Button_browse.place(x=100, y=55)

        self.Button_apply = Button(root, text="Apply", command=self.apply)
        self.Button_apply.place(x=750, y=55)

        self.Button_sub = Button(root, text="Start Analysis", command=self.run)
        self.Button_sub.place(x=750, y=85)

        self.Button_exit = Button(root, text="Quit", command=self.quit)
        self.Button_exit.place(x=750, y=555)

        # TEXT BOX
        self.txtbox = Text(root, height=15, width=100, font=TEXT_BOX_FONT, fg='blue')
        self.txtbox.place(x=10,y=200)
        #SCROLL BAR
        self.yscrollbar = Scrollbar(root, orient=VERTICAL, command=self.txtbox.yview)
        self.yscrollbar.place(x=910,y=200,height=305)

        interface_text = '1. Load your data-set with x-y values \n2. Set the initial parameters and click apply \n3. Start gradient-descent !\n'
        self.txtbox.insert(END, interface_text)

    def apply(self):  # This function allows you to get the value of the entries
        self.b = float(self.txtb.get())
        self.m = float(self.txtm.get())
        self.learningRate = float(self.txtlr.get())
        self.iteration_num = int(self.txtiter.get())

        interface_text = "\nInitialisation completed!\nStarting gradient descent at b = {0}, m = {1}, error = {2}\n".format(self.b, self.m,
                                                                                    self.error(self.m, self.b,self.data))

        self.txtbox.insert(END, interface_text)

    def browser(self):
        fname = askopenfilename(filetypes=[("csv files", "*.csv")])
        print(fname)
        csvfile = open(fname)
        reader = csv.reader(csvfile)
        self.data = list(reader)
        print(self.data)
        interface_text = '\nData loaded .....\n'
        self.txtbox.insert(END, interface_text)

        for k, l in self.data:
            self.x.append(float(k))
            self.y.append(float(l))
        print(self.x)
        print(self.y)

    def error(self,m,b,data):
        self.data = data
        self.m = m
        self.b = b
        totalError = 0
        for i in range(len(self.data)):
            totalError += (self.y[i] - (self.m * self.x[i] +self.b)) ** 2
        return totalError

    def update(self):

        db = 0.0
        dm = 0.0
        for g in range(len(self.data)):
            db += -(self.y[g] - (self.m * self.x[g] + self.b))  # calculating the derivative for the intercept at each x,y point and summing them up
            dm += -(self.x[g] * ( self.y[g] - (self.m * self.x[g] + self.b)))  # calculating the derivative for the slope at each x,y point and summing them up
        self.b += - (self.learningRate * db)  # updating the intercept
        self.m += - (self.learningRate * dm)  # updating the slope

    def anim_init(self):
        global ctmap,graph1,line,surface,ctmap_infotext
        graph1.autoscale(enable=True,axis='both', tight=False)
        graph1.set_xlabel("X", color='k')
        graph1.set_ylabel("Y", color='k')
        graph1.scatter(self.x, self.y, label='Points', color='m', s=70, marker='o')
        mmm, bbb = np.polyfit(self.x, self.y, 1)
        graph1.plot(self.x, [mmm * xi + bbb for xi in self.x], ls='dotted', c='r', label='Best fit line')
        graph1.legend(bbox_to_anchor=(0., 0.98, 1., .005), loc=3, ncol=3, fancybox=True, shadow=True,mode="expand",)
        graph1.add_line(line)
        ms = np.linspace((mmm - 30), (mmm + 30), 75)
        bs = np.linspace((bbb - 30), (bbb + 30), 75)
        M, B = np.meshgrid(ms, bs)
        zs = np.array([self.error(mp, bp, self.data)
                       for mp, bp in zip(np.ravel(M), np.ravel(B))])
        Z = zs.reshape(M.shape)
        surface.plot_surface(M, B, Z, rstride=1, cstride=1, cmap=cm.rainbow, alpha=0.5)
        surface.set_xlabel('slope')
        surface.set_ylabel('intercept')
        surface.set_zlabel('TSSE')
        ctmap.set_xlabel('Slope')
        ctmap.set_ylabel('Intercept')
        ctmap_infotext.set_text('')
        ctmap.set_xlim((mmm - 30), (mmm + 30))
        ctmap.set_ylim((bbb - 30), (bbb + 30))
        ctmap.contour(M, B, Z, 175, cmap=cm.rainbow)
        ctmap.scatter(mmm,bbb,label='Target',color='red',marker='x',s=300)
        ctmap.legend(loc='upper left', ncol=3, fancybox=True, shadow=True)
        return line,ctmap_infotext

    def animate(self,*args):
        global ctmap,graph1,line,surface,ctmap_infotext
        self.update()
        self.iteration_program = self.iteration_program + 1
        self.interface_text= '\nPrediction at n: '+ str(self.iteration_program)+ '\nTSSE:'+ str( "%.2f" % self.error(self.m, self.b, self.data))+ '\nIntercept:'+str( "%.2f" % self.b)+ '\nSlope:'+ str("%.2f" % self.m)
        self.txtbox.insert(END, self.interface_text)
        xx = np.asarray(self.x, dtype=float)
        line.set_data(xx, self.m * xx + self.b)
        ctmap_infotext.set_text('Prediction at i '+ str(self.iteration_program)+ '\nTSSE: '+
                                   str( "%.4f" % self.error(self.m, self.b, self.data))+
                                   '\nIntercept: '+str( "%.4f" % self.b)+ '\nSlope: '+ str("%.4f" % self.m))
        ctmap.scatter(self.m, self.b, c='k', s=35)
        surface.scatter(self.m, self.b, self.error(self.m, self.b, self.data), c='k', s=35)
        for i in range(self.iteration_num):
            # print('i', iteration_program, '  m', m)
            if self.iteration_program == self.iteration_num:
                print("Reached specified iteration")
            break
            # update_surface()

    def run(self):

        # mng.window.state('zoomed')
        line_ani = animation.FuncAnimation(fig, self.animate, init_func=self.anim_init, frames=self.iteration_num, interval=2, repeat=False)
        plt.show()



# if __name__ == '__main__':
root = Tk()
root.wm_title("Linear Regression____GRADIENT DESCENT")
root.geometry("950x600+500+300")
interface = Interface(root)
interface.mainloop()

