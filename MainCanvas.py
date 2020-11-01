from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import ProcessData
import pandas as pd
import numpy as np
import math
import webcolors
import skimage.io as io
import skimage.transform as transform
# class cls:
#     def __init__(self):
#         self.y = APP_UI.y
class Canvas(FigureCanvas):
    # def _init(self):
    #     import APP_UI
    #     self.app_ui = APP_UI()
    def __init__(self, parent=None, width=10, height=10, dpi=80):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # self.axes.transData.transform_point([x,y])

    def symlog(self, x, y):
        mapx = np.abs(x)
        mapy = np.abs(y)
        val = 5*np.log2(np.sqrt(mapx**2 + mapy ** 2))
        val[val<0]=0
        mapx = val * np.cos(np.arctan(mapy/(mapx + .0000001)))
        mapy = val * np.sin(np.arctan(mapy/(mapx + .0000001)))
        return np.sign(x) * mapx, np.sign(y) * mapy

    def symexp(self, x, y):
        mapx = np.abs(x)
        mapy = np.abs(y)
        val = np.power(2,np.sqrt(mapx**2 + mapy ** 2))
        val[val<0]=0
        mapx = val * np.cos(np.arctan(mapy/(mapx + .0000001)))
        mapy = val * np.sin(np.arctan(mapy/(mapx + .0000001)))
        return np.sign(x) * mapx, np.sign(y) * mapy
    # def onclick(event):
    #     print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #           ('double' if event.dblclick else 'single', event.button,
    #            event.x, event.y, event.xdata, event.ydata))
    #
    # cid = FigureCanvas.mpl_connect(onclick('button_press_event'))

#do we need the following two methods?
    def spaghettiPlot(self):
        import pandas as pd
        import numpy as np
        data = ProcessData.importData('data0.csv')['SMOIS']
        self.axes.contour(np.array(data).reshape(699, 639))
        self.draw()

    def filledContour(self):

        data = ProcessData.importData('data0.csv')['SMOIS']
        self.contourf = self.axes.contourf(np.array(data).reshape(699, 639))
        self.draw()

    def clearPlt(self):
        self.fig.clear()
        self.axes = self.figure.add_subplot(111)
        self.draw()
    def clearPlt2(self):
        self.fig.clear()
        self.axes = self.figure.add_subplot(111)
    def plot_contour(self,data,level):
        self.axes.contour(np.array(data['levels']).reshape(699, 639), level, colors=['g', 'r', 'y'])
        self.draw()

    # def setTextbasedonIsoline(self):
    #     value1 = self.horizontalSlider_isoline1.value() / 100
    #     value2 = self.horizontalSlider_isoline2.value() / 100
    #     value3 = self.horizontalSlider_isoline3.value() / 100
    #     return value1,value2,value3

    def generate_images(self,filtered_graph,filename, data,levels,column,alpha_cf = 1,flag_dir = 0,flag_content = 0,magnitude = 0,
                        cmap='Colormap 1',cline='copper',arrowscale = 'Linear', cvector_high2low = 'Black', cvector_low2high = 'Blue', line_opacity = 0.4,line_width=0.5):
        # b1 = 4
        # print(b1)
        #import APP_UI

        def getRGBdecr(hex):
            hex = hex.lstrip('#')
            hlen = len(hex)
            return tuple(np.array([int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3)])/255.0)
        rgb_colors = [getRGBdecr('#d7191c'),getRGBdecr('#fdae61'),getRGBdecr('#a6d96a'),getRGBdecr('#1a9641')]


        cmap_dict =  {
        'Colormap 1':['#2b83ba','#abdda4','#ffffbf','#fdae61','#d7191c'],
        'Colormap 2':['#f6eff7','#bdc9e1','#67a9cf','#02818a'],
        'Colormap 3':['#238b45','#66c2a4','#b2e2e2','#edf8fb'],
        'Colormap 4':['#feebe2','#fbb4b9','#f768a1','#ae017e'],
        'Colormap 5' :['#f1eef6','#bdc9e1','#74a9cf','#0570b0'],
        'Colormap 6':['#f2f0f7','#cbc9e2','#9e9ac8','#6a51a3']
        #'Colormap 1':['#7fc97f','#beaed4','#fdc086','#ffff99'],
        #'Colormap 2':['#1b9e77','#d95f02','#7570b3','#e7298a'],
        #'Colormap 3':['#a6cee3','#1f78b4','#b2df8a','#33a02c'],
        #'Colormap 4':['#e41a1c','#377eb8','#4daf4a','#984ea3'],
        #'Colormap 5' :['#66c2a5','#fc8d62','#8da0cb','#e78ac3'],
        #'Colormap 6':['#8dd3c7','#ffffb3','#bebada','#fb8072']
        }

        #cvector_high2low_dict = {'Black':['#000000'], 'Blue': ['#0000FF'], 'Red': ['#ff0000'], 'Green': ['#00ff00']}
        self.clearPlt2()

        if filename[-3:] != 'csv':
            ext = self.axes.get_xlim() + self.axes.get_ylim()
            self.axes.imshow(transform.resize(io.imread(filename), (699, 639)))
        filtered_graph = filtered_graph[
            ['level', 'node_x', 'node_y', 'path', 'aggregated_weight', 'actual_weight', 'normalized',
             'res_dir_x_HL', 'res_dir_y_HL','res_dir_x_LH', 'res_dir_y_LH',
             'res_dir_x_1_HL', 'res_dir_y_1_HL', 'res_dir_x_1_LH', 'res_dir_y_1_LH',
             'resultant','mag_HL','mag_LH']]


        data['levels'] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        self.axes.contour(np.array(data['levels']).reshape(699, 639), levels, colors=cmap_dict[cmap], alpha=line_opacity,linewidths=line_width)
        if(flag_content == 0 or flag_content == 1):
            self.axes.contourf(np.array(data['levels']).reshape(699, 639), [0,levels[0],levels[1],levels[2],1], colors=cmap_dict[cmap], alpha=alpha_cf)
            # import APP_UI
            # value1 = APP_UI.horizontalSlider_isoline1.value() / 100
            # value2 = APP_UI.horizontalSlider_isoline2.value() / 100
            # value3 = APP_UI.horizontalSlider_isoline3.value() / 100
            # a = '0' + ' - ' + str(value1)
            # b = str(value1) + ' - ' + str(value2)
            # c = str(value2) + ' - ' + str(value3)
            # d = str(value3) + ' - ' + '100'

            # b=4
            # print(b)
            # import APP_UI
            # # from APP_UI import setIsoLineSlider2Listener
            # a = APP_UI.setIsoLineSlider2Listener()
            # print (a)
            # plt.colorbar()
            # proxy = [plt.Rectangle((0, 0), 1, 1, fc= 'black')]
            # texts = ["Data Description"]
            # plt.legend(proxy,texts)
            # plt.show()
            # self.axes.colorbar(np.array(data['levels']).reshape(699, 639), shrink=0.9)
            # proxy1 = plt.Rectangle((0, 0), 1, 1, fc=cmap_dict[cmap].index('0'),
            #                        alpha=0.7, linewidth=3, label='foo')
            # self.axes.patches += proxy1
            # colors = ["#78c3f1","#78c3f1","#78c3f1","#78c3f1"]
            colors= cmap_dict[cmap]
            #string1 = self.setTextbasedonIsoline()
            texts = ["0 - Isoline1", "Isoline1 - Isoline2", "Isoline2 - Isoline3", "Isoline3 - 100"]
            # texts = [a, b, c, d]
            # print (len(texts))
            patches = [mpatches.Patch(color=colors[i],label = "{:s}".format(texts[i]))for i in range(len(texts))]
            self.axes.legend(handles = patches,bbox_to_anchor = (0.5,0.01),loc = 'lower center', ncol=4)
            # plt.show()
        #self.axes[0][-1].legend()

        #filtered_graph = filtered_graph[filtered_graph['normalized'] >= 0.01]
        p10 = np.percentile(filtered_graph['normalized'], 10)
        p90 = np.percentile(filtered_graph['normalized'], 90)
        filtered_graph = filtered_graph[(filtered_graph['normalized'] >= p10) & (filtered_graph['normalized'] <= p90) ]
        df1 = filtered_graph[#(filtered_graph['resultant'] >= 0) &
            (filtered_graph['mag_HL'] >= magnitude)].copy()
        df2 = filtered_graph[#(filtered_graph['resultant'] < 0) &
            (filtered_graph['mag_LH'] >= magnitude)].copy()

# Exponential, Logarithmic and Normalized value finding

        x1 = df1['res_dir_x_1_HL'].min()
        y1 = df1['res_dir_y_1_HL'].min()
        x2 = max(df1['res_dir_x_1_HL'].max(), -x1)
        y2 = max(df1['res_dir_y_1_HL'].max(), -y1)
        delta = max(x2,y2)+0.00000001
        #jyoti: not perfect, but works now
        df1.loc[:, 'nor_x_1_HL'] = 5*((df1['res_dir_x_1_HL'])/ (delta)).values
        df1.loc[:, 'nor_y_1_HL'] = 5*((df1['res_dir_y_1_HL'])/ (delta)).values
        #df1['res_dir_x_1_HL'] = ((df1['res_dir_x_1_HL'])/ (delta)).values
        #df1['res_dir_y_1_HL'] = ((df1['res_dir_y_1_HL'])/ (delta)).values
        #

        x3 = df2['res_dir_x_1_LH'].min()
        y3 = df2['res_dir_y_1_LH'].min()
        x4 = max(df2['res_dir_x_1_LH'].max(),-x3)
        y4 = max(df2['res_dir_y_1_LH'].max(),-y3)
        delta = max(x4, y4)+0.00000001
        #jyoti: not perfect, but works now
        df2.loc[:, 'nor_x_1_LH'] = 3*((df2['res_dir_x_1_LH']) / (delta)).values
        df2.loc[:, 'nor_y_1_LH'] = 3*((df2['res_dir_y_1_LH']) / (delta)).values
        #df2['res_dir_x_1_LH'] = ((df2['res_dir_x_1_LH']) / (delta)).values
        #df2['res_dir_y_1_LH'] = ((df2['res_dir_y_1_LH']) / (delta)).values
        #df2.loc[:, 'nor_x_1_LH'] = ((df2['res_dir_x_1_LH'] - x3) / (y3 - x3)).values
        #df2.loc[:, 'nor_y_1_LH'] = ((df2['res_dir_y_1_LH'] - x4) / (y4 - x4)).values
#########
        #scale = math.exp(filtered_graph['mag'].min()+20)
        if(flag_content == 0 or flag_content == 2):
            if(arrowscale == 'Linear'):
                if(flag_dir == 0 or flag_dir==1):
                    self.axes.quiver(df1['node_x'], df1['node_y'], df1['res_dir_x_1_HL'], df1['res_dir_y_1_HL'],
                        width=0.0009, headwidth=5.5, headlength=5.5, color= cvector_high2low, scale_units = 'inches', scale=100)
                if (flag_dir == 0 or flag_dir == 2):
                    self.axes.quiver(df2['node_x'], df2['node_y'], df2['res_dir_x_1_LH'], df2['res_dir_y_1_LH'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale_units = 'inches', scale=100)
            elif(arrowscale == 'Exponential'):
                if (flag_dir == 0 or flag_dir == 1):
                    a,b = self.symexp(df1['nor_x_1_HL'],df1['nor_y_1_HL'])
                    self.axes.quiver(df1['node_x'], df1['node_y'], a,b,
                        width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_high2low, scale_units = 'inches', scale=10)

                if (flag_dir == 0 or flag_dir == 2):
                    a, b = self.symexp(df2['nor_x_1_LH'], df2['nor_y_1_LH'])
                    self.axes.quiver(df2['node_x'], df2['node_y'], a,b,
                                 width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale_units = 'inches', scale=10)

            elif (arrowscale == 'Logarithmic'):
                if (flag_dir == 0 or flag_dir == 1):
                    a,b = self.symlog(df1['nor_x_1_HL'],df1['nor_y_1_HL'])
                    self.axes.quiver(df1['node_x'], df1['node_y'], a,b,
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_high2low, scale_units = 'inches', scale=10)

                if (flag_dir == 0 or flag_dir == 2):
                    a,b = self.symlog(df2['nor_x_1_LH'], df2['nor_y_1_LH'])
                    self.axes.quiver(df2['node_x'], df2['node_y'], a,b,
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale_units = 'inches', scale=10)

            elif (arrowscale == 'Normalized'):
                if (flag_dir == 0 or flag_dir == 1):
                    #print("0 1 Exponential")
                    self.axes.quiver(df1['node_x'], df1['node_y'], df1['nor_x_1_HL'], df1['nor_y_1_HL'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_high2low, scale_units = 'inches', scale=10)

                if (flag_dir == 0 or flag_dir == 2):
                    self.axes.quiver(df2['node_x'], df2['node_y'], df2['nor_x_1_LH'], df2['nor_y_1_LH'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high,  scale_units = 'inches', scale=10)
        self.draw()
#import APP_UI