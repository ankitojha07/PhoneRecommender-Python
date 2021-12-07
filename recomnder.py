from tkinter import *
from time import sleep, time

class recomnder:
    GREY_LIGHT = "#e6e1da"

    def __init__(self, size = "900X450", sizeLock=False):
        self.filterCollection={}  # {'name': [frame, [checkbox, var], [checkbox, var] ]}
        self.itemCollection = []  #  [[Frame, image]]
        self.products = []         # register all products and will be used in filtering operations
        self.window = Tk()
        self.window.title("Mobile Recommender")
        self.window.geometry(size)
        if sizeLock:
            self.window.resizable(height=False, width=False)
    
    def AddHeader(self, heading = "No Heading", fontStyle="Helvetica", fontSize=16):
        self.header = Frame(self.window, bg="grey", borderwidth=4)
        self.header.pack(fill='x', side=TOP)
        self.heading = Label(self.header,bg='grey', text=heading, font=(fontStyle, fontSize))
        self.heading.pack(side=LEFT)

    def AddFilterBar(self, width=24):
        # we create a main frame for filters
        self.filterBarMain = Frame(self.window, bg='grey', relief=SUNKEN, borderwidth=4)
        self.filterBarMain.pack(side=LEFT, fill=Y)
        Label(self.filterBarMain, text='Filters'+' '*width, font=('areal', 12, 'bold')).pack(side=TOP)
        # we create a canvas inside the main frame
        self.filterBarCanvas = Canvas(self.filterBarMain, bg='grey')
        self.filterBarCanvas.pack(side=LEFT, fill=BOTH, expand=1)
        # we add a scrollbar in main frame for canvas
        self.filterScroll = Scrollbar(self.filterBarCanvas,orient='vertical', command=self.filterBarCanvas.yview)
        self.filterScroll.pack(side=RIGHT, fill=Y)
        self.filterBarCanvas.configure(yscrollcommand=self.filterScroll.set)
        self.filterBarCanvas.bind('<Configure>', lambda e: self.filterBarCanvas.configure(scrollregion=self.filterBarCanvas.bbox("all")))
        # we create another frame in canvas
        self.filterBar = Frame(self.filterBarCanvas)
        self.filterBarCanvas.create_window((0,0), window=self.filterBar, anchor='nw')

    def InsertFilter(self, name, option):
        #this list will contail the whole list of checkboxs
        self.filterCollection[name] = [None]    
        self.filterCollection[name][0] = Frame(self.filterBar, bg='grey', relief=GROOVE, borderwidth=1)
        self.filterCollection[name][0].pack(side=TOP, fill='x', pady=0)
        Label(self.filterCollection[name][0], text=name, font=("areal", 11, 'bold'), foreground='white', bg="grey")\
        .grid(column=0, row=0, sticky='w')
        #adding checkbox with filter options
        a = 0
        for i in option:
            a+=1
            self.filterCollection[name].append([None, BooleanVar()])  # [Checkbox, Bool Var]
            self.filterCollection[name][a][0] = Checkbutton(self.filterCollection[name][0], text=i, font=("areal", 10),
                                                            variable=self.filterCollection[name][a][1], foreground='white',
                                                             bg="grey", selectcolor='#000080', activebackground="#696969",
                                                             command=self.FilterProduct)
            self.filterCollection[name][a][0].grid(row = a, column = 0, sticky='w', padx=20)

    def AddSearchBar(self):
        self.searchFrame = Frame(self.window)
        self.searchFrame.pack(side=TOP, pady=10,padx=100, fill=X)
        self.searchBar = Entry(self.searchFrame, bg=recomnder.GREY_LIGHT)
        self.searchBar.pack(side=LEFT, fill=X, expand=True)
        self.searchButton = Button(self.searchFrame, text="Search", bg='grey', width=15)
        self.searchButton.pack(side=LEFT, padx=2)

    def AddBody(self, width=600):
        # Insert a main frame for a body
        self.bodyMain = Frame(self.window, bg='#000080')
        self.bodyMain.pack(side=TOP, fill=BOTH, expand=1)
        # insert a canvas in main frame
        self.bodyCanvas = Canvas(self.bodyMain, bg='#000080')
        self.bodyCanvas.pack(side=LEFT, fill=BOTH, expand=1)
        # we add a scrollbar in main frame for canvas
        self.bodyScroll = Scrollbar(self.bodyCanvas,orient='vertical', command=self.bodyCanvas.yview)
        self.bodyScroll.pack(side=RIGHT, fill=Y, expand=0)
        self.bodyCanvas.configure(yscrollcommand=self.bodyScroll.set)
        self.bodyCanvas.bind('<Configure>', lambda e: self.bodyCanvas.configure(scrollregion=self.bodyCanvas.bbox("all")))
        # we create another frame in canvas
        self.body = Frame(self.bodyCanvas, bg='#000080')
        self.bodyCanvas.create_window((0,0), window=self.body, anchor='nw', width=width)
        
    def InsertItem(self, title="Samsung mobile new m31 8gb ram 4gb rom",price=9999, features = {}, image_url=""):
        # adding main frame
        self.itemCollection.append({'mainFrame':None, 'imageFrame':None, 'textFrame':None, 'img':None}) # (main frame, image frame, text frame)
        self.itemCollection[-1]['mainFrame'] = Frame(self.body, relief=GROOVE, borderwidth=1)
        self.itemCollection[-1]['mainFrame'].pack(side=TOP, expand=1, fill=X, padx=30, pady=2)
        # image frame
        self.itemCollection[-1]['imageFrame'] = Frame(self.itemCollection[-1]['mainFrame'])
        self.itemCollection[-1]['imageFrame'].pack(side=LEFT, fill=Y)
        self.itemCollection[-1]['img'] = PhotoImage(file=image_url)
        Label(self.itemCollection[-1]['imageFrame'], image=self.itemCollection[-1]['img']).pack(side=LEFT, fill=Y, pady=20, padx=10)
        # Text frame
        self.itemCollection[-1]['titleFrame'] = Frame(self.itemCollection[-1]['mainFrame'])
        self.itemCollection[-1]['titleFrame'].pack(side=TOP, fill=X, expand=1)
        Label(self.itemCollection[-1]['titleFrame'], text=title, font=('Consolas', 14, 'bold')).grid(row=0, column=0)
        self.itemCollection[-1]['textFrame'] = Frame(self.itemCollection[-1]['mainFrame'])
        self.itemCollection[-1]['textFrame'].pack(side=LEFT, fill=BOTH, expand=1)
        Row, Column = 1, 0
        for i in features:
            Label(self.itemCollection[-1]['textFrame'], text=str(i)+": "+str(features[i]+"   "), font=('Consolas', 12, ),foreground='Grey' ).grid(row=Row, column=Column, sticky='w')
            Column+=1
            if Column==2:
                Row += 1
                Column = 0
        Row = Row+1 if Column!=0 else Row
        self.itemCollection[-1]['priceFrame'] = Frame(self.itemCollection[-1]['mainFrame'])
        self.itemCollection[-1]['priceFrame'].pack(side=BOTTOM, fill=X, expand=1)
        Label(self.itemCollection[-1]['priceFrame'], text='₹'+str(price), font=('Consolas', 14,'bold' ),foreground='Green' ).pack(side=RIGHT, pady=20)

    def ProductRegister(self, product):
        self.products = product

    def MakeQuery(self):
        # create query in dict form using value of filters checkbuttons 
        query = {}
        for i in self.filterCollection:
            q = []
            for j in self.filterCollection[i][1::]:
                if j[1].get():
                    q.append(j[0].cget("text"))
            if len(q) != 0:
                query[i] = q
        return query
    
    def RepackItems(self):
        # it will show all items in the body i.e repack all items
        for i in self.itemCollection:
            i["mainFrame"].pack(side=TOP, expand=1, fill=X, padx=30, pady=2)

    def FilterProduct(self):
        self.RepackItems()
        query = self.MakeQuery()
        for q in query:
            if q=="Price":
                self.FilterPrice(query[q])
                continue
            product_no = 0
            for p in self.products:
                if p["features"].get(q) is None or p["features"][q] not in query[q]:
                    # hide the product which is not following the query demand
                    self.itemCollection[product_no]["mainFrame"].pack_forget()
                product_no += 1

    def FilterPrice(self, q):
        # price filter is different from other filters because it doesn't woky by seaching
        # it is based of range so required another logic
        s, e = 0, 0
        for i in q:
            if i=="<5,000": s, e = 0, 5000
            elif i == "5,000 - 10,000": s, e = 5000, 10000
            elif i == "10,000 - 25,000": s, e = 10000, 25000
            elif i == "25,000 - 50,000": s, e = 25000, 50000
            elif i == ">50,000": s, e = 50000, float('inf')
            product_no = 0
            for p in self.products:
                cost = int("".join( p["price"].split(",")))
                if cost<s or cost>e:
                    # hide the product which is not following the query demand
                    self.itemCollection[product_no]["mainFrame"].pack_forget()
                product_no += 1


    def ShowWindow(self):
        self.window.mainloop()