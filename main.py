from tkinter import *
from tkinter import ttk, StringVar
import inspect
from tkinter import filedialog
from importlib import reload
import os
from PIL import ImageTk, Image
from tkinter import messagebox
import default_route_file as routeFile


class route_analyser_app():
    default_path = os.getcwd()
    print(default_path)

    # initial variable
    initialRemoveList = ['__cached__', '__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
    maxOccurrence = 0
    routeStationDict = {}
    dictOfAllStation = {}
    listOfAllStationName = []
    oldRouteList = []
    routeList = []



    
    def routeIsSelected(self, event):
        if self.selectedRoute.get()!='Select the route':
            self.selectedRouteStationListbox.delete(0,END)
            i = 0
            for ele in self.routeStationDict[self.selectedRoute.get()]:
                ele = str(i+1) + '. ' + str(ele)
                i+=1
                self.selectedRouteStationListbox.insert(END, ele)
            # self.reset_scrollregion("e")
            if self.root.winfo_height()==300:
                self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()+180}") # to update the scrollbar
            else:
                self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()+1}")
                self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()-1}")
        else:
            self.selectedRouteStationListbox.delete(0,END)
            self.selectedRouteStationListbox.insert(0, "--Select the route--")
        self.selectedRouteStationFrame.pack(fill=BOTH, expand=1)

    def makeComfortable(self, stationName):
        def removeExtraSpace(strings):
            """It will remove multiple spaces and tab
                remove brts, brt"""
            space = strings.split(' ')
            
            for i in range(space.count("")):
                space.remove("")
            #for ele in space:
    #    	    if ele.endswith("brts")
            
            xspace = []
            for ele in space:
                if ele.count("\t")>0:
                    filter = ele.split("\t")
                    for i in range(filter.count("")):
                        filter.remove("")
                    ele = ''.join(filter) 
                xspace.append(ele)
            return ''.join(xspace)
        
        stationName = stationName.lower()
        removeList = ["brts", "brt", "'", "`", "‘", "’", "junction"]
        for ele in removeList:
            stationName = stationName.replace(ele,"")
        # TODO: remove vowel form the station
        replaceDict = {"z":"s", "e":"a", "i":"y"}
        for ele in replaceDict:
            stationName = stationName.replace(ele, replaceDict[ele])
        stationName = removeExtraSpace(stationName)
        return stationName

    def returnFoundedRouteFor(self, station):
        foundedRoute = []
        trueStationName = station
        for key in self.routeStationDict:
            for ele in self.routeStationDict[key]:
                xele = self.makeComfortable(ele) # Original station name is stored in ele
                station = self.makeComfortable(station)
                # ele = ele + "---" + station + "---"
                # raise ValueError(ele)
                if xele==station:
                    foundedRoute.append(key)
                    trueStationName = ele
                    break
        return (trueStationName, foundedRoute)

    def occurrenceOf(self, station):
        return self.dictOfAllStation[station]

    # show the dialogbox if givenStationName is in self.listOfAllStationName
    # def openSelectionBox(givenStationName, trueStationName, fromOrToStation): # it will change the value in the entry widget
    #     def selected(fromOrTo):
    #         if fromOrTo=="from":
    #             self.fromStation.delete(0, END)
    #             self.fromStation.insert(0, BXSuggestedStationListbox.get(ANCHOR))
    #         elif fromOrTo=="to":
    #             self.toStation.delete(0, END)
    #             self.toStation.insert(0, BXSuggestedStationListbox.get(ANCHOR))
    #         elif fromOrTo=="from-oneStation":
    #             self.fromStation.delete(0, END)
    #             self.fromStation.insert(0, BXSuggestedStationList[0])
    #         elif fromOrTo=="to-oneStation":
    #             self.toStation.delete(0, END)
    #             self.toStation.insert(0, BXSuggestedStationList[0])
    #         self.suggestedStationBX.destroy()
    #         self.stationIsGiven()
        
    #     #raise ValueError(givenStationName, ", ", trueStationName)
    #     if (givenStationName!="") and (trueStationName!="") and (givenStationName==trueStationName):
    #         # raise ValueError("here")
    #         BXSuggestedStationList = []
    #         for stationName in self.listOfAllStationName:
    #             stationNameCheck = self.makeComfortable(stationName)
    #             givenStationNameCheck = self.makeComfortable(givenStationName)
    #             if stationNameCheck=='':
    #                 stationNameCheck = stationName
    #             if givenStationNameCheck=='':
    #                 givenStationNameCheck = givenStationName
    #             if (stationNameCheck).count(givenStationNameCheck)>0:
    #                 if BXSuggestedStationList.count(stationName)==0:
    #                     BXSuggestedStationList.append(stationName)
    #         if len(BXSuggestedStationList)>=1:
    #             self.suggestedStationBX = Toplevel()
    #             #raise ValueError("here")
    #             self.suggestedStationBX.title("Select the station...")
    #             # Making frame for set scrollbar
    #             BXSuggestedStationFrame = Frame(self.suggestedStationBX, bg='white')
    #             BXSuggestedStationFrameScrollbar = Scrollbar(BXSuggestedStationFrame, orient=VERTICAL)
    #                 # Making listbox into the frame
    #             BXSuggestedStationListbox = Listbox(BXSuggestedStationFrame, yscrollcommand=BXSuggestedStationFrameScrollbar.set)
    #                 # Configuring scrollbar before packing of listbox 
    #             BXSuggestedStationFrameScrollbar.config(command=BXSuggestedStationListbox.yview)
    #             BXSuggestedStationFrameScrollbar.pack(side=RIGHT, fill=Y)
    #             BXSuggestedStationListbox.pack(fill=X)
    #             BXSuggestedStationFrame.pack(fill=X)
                
    #             for ele in BXSuggestedStationList:
    #                 BXSuggestedStationListbox.insert(END, ele)
                
    #             BXSelectBtn = Button(self.suggestedStationBX, text="Select", command=lambda: selected(fromOrToStation))
    #             BXSelectBtn.pack(padx=50, pady=(0,10), fill=X)
                
    #             # self.suggestedStationBX.mainloop()
                
    #         elif len(BXSuggestedStationList)==1:
    #             raise ValueError("here")
    #             selected(fromOrToStation+"-oneStation")

    # status = ''
    def stationIsGiven(self):
        fromStationRouteList = []
        toStationRouteList = []
        
        # making list of first station's route
        fromStation_local_var = self.fromStation.get()
        fromStationData = self.returnFoundedRouteFor(fromStation_local_var) # toStationData[0] is currectToStationName & toStationData[1] is foundedRouteList
        self.fromStation.delete(0, END)
        self.fromStation.insert(0, fromStationData[0])
        self.suggestedRouteListbox.delete(0, END)
        self.suggestedRouteListbox.insert(END, f"Route from '{fromStation_local_var.capitalize()}' Station:")
        for ele in fromStationData[1]:
            fromStationRouteList.append(ele)
            ele = '- ' + ele
            self.suggestedRouteListbox.insert(END, ele)
        
        # making list of last station's route
        toStation_local_var = self.toStation.get()
        toStationData = self.returnFoundedRouteFor(toStation_local_var)
        self.toStation.delete(0, END)
        self.toStation.insert(0, toStationData[0])
        self.suggestedRouteListbox.insert(END, " ")
        self.suggestedRouteListbox.insert(END, f"Route from '{toStation_local_var.capitalize()}' Station:")
        for ele in toStationData[1]:
            toStationRouteList.append(ele)
            ele = '- ' + ele
            self.suggestedRouteListbox.insert(END, ele)
        


        # making list of suggested route
        suggestedRouteList = []
            
            # ********************************************suggesting if routes are same********************************************
        single_route = self.onSingleRoute((fromStation_local_var).capitalize(), fromStationRouteList, (toStation_local_var).capitalize(), toStationRouteList)
        if single_route!=None:
            for ele in single_route:
                suggestedRouteList.append(ele)
        else:
            # ********************************************suggesting if route need to be changed at once********************************************
            double_route = self.onDoubleRoute((fromStation_local_var).capitalize(), fromStationRouteList, (toStation_local_var).capitalize(), toStationRouteList)
            if double_route!=None:
                for ele in double_route:
                    suggestedRouteList.append(ele)
            else:
                tripple_route = self.onTrippleRoute((fromStation_local_var).capitalize(), fromStationRouteList, (toStation_local_var).capitalize(), toStationRouteList)
                if tripple_route!=None:
                    for ele in tripple_route:
                        suggestedRouteList.append(ele)




        # parse the suggestedRouteList
        xsuggestedRouteList = []
        for ele in suggestedRouteList:
            repetition = int(len(ele)/3)
            xele = ""
            index = 0
            for i in range(repetition):
                if index==0:
                    xele = ele[index] + " - " + ele[index+1] + " (" + ele[index+2] + ")"
                    index+=3
                else:
                    xele = xele + "<->" + ele[index] + " - " + ele[index+1] + " (" + ele[index+2] + ")"
                    index+=3
            xsuggestedRouteList.append(xele)


        self.suggestedRouteListbox.insert(END, "")
        self.suggestedRouteListbox.insert(END, f"Suggested route: ")
        index = 1
        for ele in xsuggestedRouteList:
            eleList = ele.split("<->")
            if len(eleList)==1:
                ele = str(index) + '. ' + ele
                self.suggestedRouteListbox.insert(END, ele)
                index+=1
            else:
                first = "yes"
                for ele in eleList:
                    if first=="yes":
                        ele = str(index) + '. ' + ele
                        first = 'no'
                    else:
                        ele = "    " + ele
                        
                    self.suggestedRouteListbox.insert(END, ele)
                index+=1

    def onSingleRoute(self, station1, station1RouteList, station2, station2RouteList):
        returnList = []
        for route in station1RouteList:
            if station2RouteList.count(route)>0:
                item = [station1.capitalize(), station2.capitalize(), route]
                returnList.append(item)
        if returnList!=[]:
            return returnList
        else:
            return None

    def onDoubleRoute(self, station1, station1RouteList, station2, station2RouteList):
        returnList = []
        fromStationRouteMaxOccurredStation = {}
        toStationRouteMaxOccurredStation = {}
        tempMaxOccurrence = self.maxOccurrence


        # removing routes in toStationRouteList which contatins self.fromStation 
        # removing routes in fromStationRouteList which contatins self.toStation 
        for route in station1RouteList.copy():
            for station in self.routeStationDict[route]:
                if station.lower()==station2.lower():
                    station1RouteList.remove(route)
        for route in station2RouteList.copy():
            for station in self.routeStationDict[route]:
                if station.lower()==station1.lower():
                    station2RouteList.remove(route)
        
        # making dict(stationName: routes) of most occurred station
        while tempMaxOccurrence>1:
            for routeName in station1RouteList:
                stationsInRoute = self.routeStationDict[routeName]
                for station in stationsInRoute:
                    if self.occurrenceOf(station)==tempMaxOccurrence:
                        try:
                            fromStationRouteMaxOccurredStation[station].append(routeName) # adding element in list
                        except:
                            fromStationRouteMaxOccurredStation[station] = [routeName,] # making new dictionary element if it is not available
                        
            for routeName in station2RouteList:
                stationsInRoute = self.routeStationDict[routeName]
                for station in stationsInRoute:
                    if self.occurrenceOf(station)==tempMaxOccurrence:
                        try:
                            toStationRouteMaxOccurredStation[station].append(routeName)
                        except:
                            toStationRouteMaxOccurredStation[station] = [routeName,]
            tempMaxOccurrence-=1

        # Removeing given station if it is available in MaxOccurredStation
        try:
            fromStationRouteMaxOccurredStation.pop(station1RouteList)
        except:
            pass
        try:
            toStationRouteMaxOccurredStation.pop(station2RouteList)
        except:
            pass
        
        # suggesting if toStationRouteMaxOccurredStation.keys == fromStationRouteMaxOccurredStation.keys
        toStationRouteMaxOccurredStationList = list(toStationRouteMaxOccurredStation.keys())
        for key in fromStationRouteMaxOccurredStation:
            if toStationRouteMaxOccurredStationList.count(key)>0:
                fromToMidStationRoute = fromStationRouteMaxOccurredStation[key] # list of route number
                midTotoStationRoute = toStationRouteMaxOccurredStation[key]
                # if fromToMidStationRoute!=midTotoStationRoute:
                # if (key.lower()!=(fromStation_local_var).lower()) and (key.lower()!=(self.toStation.get()).lower()):
                # for ele in fromToMidStationRoute.copy():
                #     fromToMidStationRoute = ele.capitalize()
                item1 = [(self.fromStation.get()).capitalize(), key, ", ".join(fromToMidStationRoute)]
                
                # for ele in midTotoStationRoute.copy():
                #     midTotoStationRoute = ele.capitalize()
                item2 = [key, (self.toStation.get()).capitalize(), ", ".join(midTotoStationRoute)]
                item = item1 + item2
                returnList.append(item)
        if returnList!=[]:
            return returnList
        else:
            return None

    def onTrippleRoute(self, station1, station1RouteList, station2, station2RouteList):
        returnList = []
        fromStationRouteMaxOccurredStation = {}
        toStationRouteMaxOccurredStation = {}
        tempMaxOccurrence = self.maxOccurrence

        # removing routes in toStationRouteList which contatins self.fromStation 
        # removing routes in fromStationRouteList which contatins self.toStation 
        for route in station1RouteList.copy():
            for station in self.routeStationDict[route]:
                if station.lower()==station2.lower():
                    station1RouteList.remove(route)
        for route in station2RouteList.copy():
            for station in self.routeStationDict[route]:
                if station.lower()==station1.lower():
                    station2RouteList.remove(route)
        
        # making dict(stationName: routes) of most occurred station
        while tempMaxOccurrence>1:
            for routeName in station1RouteList:
                stationsInRoute = self.routeStationDict[routeName]
                for station in stationsInRoute:
                    if self.occurrenceOf(station)==tempMaxOccurrence:
                        try:
                            fromStationRouteMaxOccurredStation[station].append(routeName) # adding element in list
                        except:
                            fromStationRouteMaxOccurredStation[station] = [routeName,] # making new dictionary element if it is not available
                        
            for routeName in station2RouteList:
                stationsInRoute = self.routeStationDict[routeName]
                for station in stationsInRoute:
                    if self.occurrenceOf(station)==tempMaxOccurrence:
                        try:
                            toStationRouteMaxOccurredStation[station].append(routeName)
                        except:
                            toStationRouteMaxOccurredStation[station] = [routeName,]
            tempMaxOccurrence-=1
        
        # Removeing given station if it is available in MaxOccurredStation
        try:
            fromStationRouteMaxOccurredStation.pop(station1RouteList)
        except:
            pass
        try:
            toStationRouteMaxOccurredStation.pop(station2RouteList)
        except:
            pass
        
        # suggesting if single route is available between two maxOccuredStation
        fromStationRouteMaxOccurredStationList = list(fromStationRouteMaxOccurredStation.keys())
        toStationRouteMaxOccurredStationList = list(toStationRouteMaxOccurredStation.keys())
        for midStation1 in fromStationRouteMaxOccurredStationList:
            for midStation2 in toStationRouteMaxOccurredStationList:
                midStation1Data = self.returnFoundedRouteFor(midStation1)
                midStation2Data = self.returnFoundedRouteFor(midStation2)
                
                single_route = self.onSingleRoute(midStation1, midStation1Data[1], midStation2, midStation2Data[1])
                if single_route!=None:
                    # making route list from station1-station2-route formet
                    xsingle_route = []
                    index = 2
                    for route in single_route:
                        xsingle_route.append(route[index])
                        index += 3
                    
                    item1 = [station1.capitalize(), midStation1.capitalize(), ", ".join(fromStationRouteMaxOccurredStation[midStation1])]
                    item2 = [midStation1.capitalize(), midStation2.capitalize(), ", ".join(xsingle_route)]
                    item3 = [midStation2.capitalize(), station2.capitalize(), ", ".join(toStationRouteMaxOccurredStation[midStation2])]
                    item = item1 + item2 + item3
                    returnList.append(item)
        if returnList!=[]:
            return returnList
        else:
            return None




    def updateFromStationSuggestionListbox(self, name_list):
        self.suggestedFromStationListbox.delete(0, END)
        # here we have 2 option
        # 1.sort by len
        # name_list = set(name_list)
        # name_list = sorted(name_list, key=len)
        
        # 2.upper element are contains continues word
        new_name_list = []
        for ele in name_list:
            if new_name_list.count(ele)==0:
                new_name_list.append(ele)
        for ele in new_name_list:
            self.suggestedFromStationListbox.insert(END, ele)

    def checkFromStation(self, e):
        word = self.fromStation.get()
        if word=='':
            self.suggestedFromStationFrame.grid_forget()
        else:
            self.suggestedFromStationFrame.grid(row=2, column=0, padx=10, pady=(0,10), sticky='ew')
            charList = list(word)
            wordOccurenceDict = {}
            new_list = []
            
        # Adding element by its continuous occurrence
            for ele in self.listOfAllStationName:
                if (ele.lower()).count(word)>0:
                    new_list.append(ele)
                comfortEle = self.makeComfortable(ele)
                comfortWord = self.makeComfortable(word)
                if comfortEle.count(comfortWord)>0:
                    new_list.append(ele)
        
        # adding element by occurrence of character
            # making dict of char & its occurrence
            for char in charList:
                try:
                    wordOccurenceDict[char] +=1
                except:
                    wordOccurenceDict[char] = 1
            
            # adding ele in new_list
            for ele in self.listOfAllStationName:
                append = False
                for keyChar in wordOccurenceDict:
                    #raise ValueError(f"{keyChar}:{ele}	{wordOccurenceDict[keyChar]}:{(ele.lower()).count(keyChar)}")
                    if (ele.lower()).count(keyChar)>=wordOccurenceDict[keyChar]:
                        append = True
                        continue
                    else:
                        append = False
                        break
                if append==True:
                    if new_list.count(ele)==0:
                        new_list.append(ele)
            # error = new_list
            # raise ValueError(error + ["    "] + new_list)
            self.updateFromStationSuggestionListbox(new_list)

    # def checkFromStation(e):
    #     word = self.fromStation.get()
    #     word = word.lower()
    #     if word=='':
    #         self.suggestedFromStationFrame.grid_forget()
    #     else:
    #         self.suggestedFromStationFrame.grid(row=2, column=0, padx=20, pady=(0,10), sticky='ew')
    #         new_list = []
    #         for ele in self.listOfAllStationName:
    #             if (ele.lower()).count(word)>0:
    #                 new_list.append(ele)
    #             comfortEle = self.makeComfortable(ele)
    #             comfortWord = self.makeComfortable(word)
    #             if comfortEle.count(comfortWord)>0:
    #                 new_list.append(ele)
    #         self.updateFromStationSuggestionListbox(new_list)

    def from_station_is_selected(self, e):
        self.fromStation.delete(0, END)
        self.fromStation.insert(0, self.suggestedFromStationListbox.get(ANCHOR))
        self.suggestedFromStationFrame.grid_forget()
        self.stationIsGiven()
        
    def updateToStationSuggestionListbox(self, name_list):
        self.suggestedToStationListbox.delete(0, END)
        name_list = set(name_list)
        for ele in name_list:
            self.suggestedToStationListbox.insert(END, ele)
        
    def checkToStation(self, e):
        word = self.toStation.get()
        word = word.lower()
        if word=='':
            self.suggestedToStationFrame.grid_forget()
        else:
            self.suggestedToStationFrame.grid(row=2, column=1, padx=(0,10), pady=(0,10), sticky='ew')
            new_list = []
            for ele in self.listOfAllStationName:
                if (ele.lower()).count(word)>0:
                    new_list.append(ele)
                comfortEle = self.makeComfortable(ele)
                comfortWord = self.makeComfortable(word)
                if comfortEle.count(comfortWord)>0:
                    new_list.append(ele)
            self.updateToStationSuggestionListbox(new_list)

    def to_station_is_selected(self, e):
        self.toStation.delete(0, END)
        self.toStation.insert(0, self.suggestedToStationListbox.get(ANCHOR))
        self.suggestedToStationFrame.grid_forget()
        self.stationIsGiven()
        
    def ListoutAllStation(self):
        self.dictOfAllStation = {}
        self.listOfAllStationName = []
        self.maxOccurrence = 1
        for route in self.routeList:
            for station in self.routeStationDict[route]:
                if self.listOfAllStationName.count(station)==0:
                    self.listOfAllStationName.append(station)
                    self.dictOfAllStation[station] = 1
                else:
                    self.dictOfAllStation[station]+=1
                    if self.dictOfAllStation[station]>self.maxOccurrence:
                        self.maxOccurrence = self.dictOfAllStation[station]
        #self.suggestedRouteListbox.insert(END, self.occurrenceOf("Railway Station Terminal"))
        i = 0
        self.suggestedRouteListbox.delete(0, END)
        for key in self.dictOfAllStation:
            ele = str(i+1) + '. ' + key + ": " + str(self.dictOfAllStation[key])
            i+=1
            self.suggestedRouteListbox.insert(END, ele)



    # menu functions
        # functions of choose route file
    def copy_routeFile_in_defaultRouteFile(self, fileName):
        with open(fileName, "r") as f:
            content = f.read() # coping data from given file
        with open(self.default_path+"/default_route_file.py", 'w') as f:
            f.write(content) # dumping data to default file
            # Making the list of availble route
    def make_initial_thing(self):
        # global self.maxOccurrence, self.dictOfAllStation, self.routeList, self.oldRouteList, self.routeStationDict, self.initialRemoveList, self.listOfAllStationName,  routeFile
        self.maxOccurrence = 0
        self.routeStationDict = {}
        self.dictOfAllStation = {}
        self.listOfAllStationName = []
        self.oldRouteList = self.routeList
        self.routeList = []
        # reloading default file and self.routeList
        reload(routeFile)
        self.routeList = dir(routeFile)
        for ele in self.initialRemoveList:
            try:
                self.routeList.remove(ele)
            except:
                pass
        
        # removing old route name (rather routeFile is reloded it is still not removed)
        for ele in self.oldRouteList:
            try:
                self.routeList.remove(ele)
            except:
                pass
        self.oldRouteList = []

        # Making (route, staion) dictionary
        inspectedList = inspect.getmembers(routeFile)
        routeStationlist = []
        for ele in self.routeList:
            for obj in inspectedList:
                if obj[0]==ele:
                    routeStationlist.append(obj)
        self.routeStationDict = dict(routeStationlist)
        for key in self.routeStationDict:
            i = 0
            for station in self.routeStationDict[key]:
                self.routeStationDict[key][i] = station.capitalize()
                i+=1
        
        # changing default value of canvas1Frame1 children
        self.selectRoute["values"] = self.routeList
        self.ListoutAllStation()

    def changeRouteFile(self):
        try:
            newRouteFile = filedialog.askopenfilename(initialdir=self.default_path, title='Choose route file', filetypes=(('Python files', '*.py'), ("Text file", "*.txt")))
            self.copy_routeFile_in_defaultRouteFile(newRouteFile)
            self.make_initial_thing()
            self.selectedRouteStationListbox.delete(0,END)
            self.selectedRouteStationFrame.pack_forget()
            self.selectedRoute.set("Select the route")
        except FileNotFoundError:
            pass
        except Exception as e:
            raise e
        
    def open_notepad(self):
        def open_text_editor():
            popup.destroy()
            try:
                os.system("notepad.exe")
            except Exception as e:
                raise e
        popup = Toplevel(self.root)
        lbl1 = Label(popup, text="Make file like this")
        lbl1.pack(padx=3, pady=4, fill=X)
        self.smpl_img = ImageTk.PhotoImage(Image.open("sample.png"))
        lbl2 = Label(popup, image=self.smpl_img)
        lbl2.pack()
        dn_btn = Button(popup, text="Ok", command=open_text_editor)
        dn_btn.pack(ipadx=30, pady=3)

        

    def run(self):
        self.root = Tk()
        self.root.title("Route Analyser")
        self.root.geometry("480x680")
        self.root.resizable(False, True)
        try:
            os.chdir(self.default_path)
        except:
            print(1)
        try:
            self.root.wm_iconbitmap("route_app.ico")
        except:
            print(2)
        
        

        # wwidth = self.root.winfo_screenwidth()-100
        # wheight = self.root.winfo_screenheight()-100
        # self.root.geometry(f"{wwidth}x{wheight}")
        # self.root.minsize(900,800)


        self.routeList = dir(routeFile) # returns name of route and other elements like in self.initialRemoveList
        for ele in self.initialRemoveList: # self.initialRemoveList is initial variable
            try:
                self.routeList.remove(ele)
            except:
                pass

        # Making (route, staion) dictionary
        inspectedList = inspect.getmembers(routeFile)
        self.routeStationDict = []
        for ele in self.routeList:
            for obj in inspectedList:
                if obj[0]==ele:
                    self.routeStationDict.append(obj)
        self.routeStationDict = dict(self.routeStationDict)
        for key in self.routeStationDict:
            i = 0
            for station in self.routeStationDict[key]:
                self.routeStationDict[key][i] = station.capitalize()
                # self.routeStationDict[key][i] = self.routeStationDict[key][i].replace("brts", "BRTS")
                # self.routeStationDict[key][i] = self.routeStationDict[key][i].replace("brt", "BRT")
                i+=1




        # making menu and sub menu
        my_menu = Menu(self.root)
        self.root.config(menu=my_menu)

            # edit menu
        edit_menu = Menu(my_menu, tearoff=0)
        edit_menu.add_command(label='Choose Route File', command=self.changeRouteFile)
        edit_menu.add_command(label='Make/Edit Route File', command=self.open_notepad)
        my_menu.add_cascade(label='Edit', menu=edit_menu)


        # making frame for full screen scrollbar
        wrepper1 = LabelFrame(self.root)
        canvas1Scrollbar = Scrollbar(wrepper1, orient=VERTICAL)
        self.canvas1 = Canvas(wrepper1, yscrollcommand=canvas1Scrollbar.set)
        canvas1Scrollbar.config(command=self.canvas1.yview)
        canvas1Scrollbar.pack(side=RIGHT, fill=Y)
        canvas1Frame1 = Frame(self.canvas1)


        # Making listbox for showing the station
            # Making frame for set scrollbar
        self.selectedRouteStationFrame = Frame(canvas1Frame1, bg='white')
        selectedRouteStationScrollbar = Scrollbar(self.selectedRouteStationFrame, orient=VERTICAL)
            # Making listbox into the frame
        self.selectedRouteStationListbox = Listbox(self.selectedRouteStationFrame, yscrollcommand=selectedRouteStationScrollbar.set)
        self.selectedRouteStationListbox.insert(0, "--Select the route--")
            # Configuring scrollbar before packing of listbox 
        selectedRouteStationScrollbar.config(command=self.selectedRouteStationListbox.yview)
        selectedRouteStationScrollbar.pack(side=RIGHT, fill=Y)
        self.selectedRouteStationListbox.pack(fill=X)

        # Getting station input through entry widget in frame
        detailsFrame = Frame(canvas1Frame1)
        #detailsFrameScrollbar = Scrollbar(detailsFrame, orient=VERTICAL)
        #detailsFrame.config(yscrollcommand=detailsFrameScrollbar.set)
        #detailsFrameScrollbar.config(command=detailsFrame.yview)
        #detailsFrameScrollbar.pack(side=RIGHT, fill=Y)

        fromLabel = Label(detailsFrame, text="From: ", width=30)
        fromLabel.grid(row=0, column=0, pady=(10,0), sticky='ew')
        self.fromStation = Entry(detailsFrame)
        self.fromStation.bind("<KeyRelease>", self.checkFromStation)
        self.fromStation.grid(row=1, column=0, padx=10, pady=(0,10), sticky='ew')

        toLabel = Label(detailsFrame, text="To: ", width=30)
        toLabel.grid(row=0, column=1, pady=(10,0), sticky='ew')
        self.toStation = Entry(detailsFrame)
        self.toStation.bind("<KeyRelease>", self.checkToStation)
        self.toStation.grid(row=1, column=1, padx=(0,10), pady=(0,10), sticky='ew')

        # Making listbox for showing suggested from Stations
            # Making frame for suggestedStationListbox scrollbar
        self.suggestedFromStationFrame = Frame(detailsFrame)
        suggestedFromStationYScrollbar = Scrollbar(self.suggestedFromStationFrame, orient=VERTICAL)
        suggestedFromStationXScrollbar = Scrollbar(self.suggestedFromStationFrame, orient=HORIZONTAL)
            # Making listbox into the frame
        self.suggestedFromStationListbox = Listbox(self.suggestedFromStationFrame, yscrollcommand=suggestedFromStationYScrollbar.set, xscrollcommand=suggestedFromStationXScrollbar.set, font=("Helvetica", 9), selectmode="single")
        self.suggestedFromStationListbox.bind("<<ListboxSelect>>", self.from_station_is_selected)
            # Configuring the scrollbar
        suggestedFromStationYScrollbar.config(command=self.suggestedFromStationListbox.yview)
        suggestedFromStationYScrollbar.pack(side=RIGHT, fill=Y)
        suggestedFromStationXScrollbar.config(command=self.suggestedFromStationListbox.xview)
        suggestedFromStationXScrollbar.pack(side=BOTTOM, fill=X)
            # packing listbox & frame
        self.suggestedFromStationListbox.pack(fill=X)
        # self.suggestedFromStationFrame.grid(row=2, column=0, padx=20, pady=(0,10), sticky='ew')

        # Making listbox for showing suggested to Stations
            # Making frame for self.suggestedToStationListbox scrollbar
        self.suggestedToStationFrame = Frame(detailsFrame)
        suggestedToStationYScrollbar = Scrollbar(self.suggestedToStationFrame, orient=VERTICAL)
        suggestedToStationXScrollbar = Scrollbar(self.suggestedToStationFrame, orient=HORIZONTAL)
            # Making listbox into the frame
        self.suggestedToStationListbox = Listbox(self.suggestedToStationFrame, yscrollcommand=suggestedToStationYScrollbar.set, xscrollcommand=suggestedToStationXScrollbar.set, font=("Helvetica", 9))
        self.suggestedToStationListbox.bind("<<ListboxSelect>>", self.to_station_is_selected)
            # Configuring the scrollbar
        suggestedToStationYScrollbar.config(command=self.suggestedToStationListbox.yview)
        suggestedToStationYScrollbar.pack(side=RIGHT, fill=Y)
        suggestedToStationXScrollbar.config(command=self.suggestedToStationListbox.xview)
        suggestedToStationXScrollbar.pack(side=BOTTOM, fill=X)
            # packing listbox & frame
        self.suggestedToStationListbox.pack(fill=X)
        # self.suggestedToStationFrame.grid(row=2, column=1, padx=(0,20), pady=(0,10), sticky='ew')

        # continueBtn = Button(detailsFrame, text='Continue', command=self.stationIsGiven)
        # continueBtn.grid(row=3, column=0, columnspan=2, padx=200, pady=10, sticky='ew')

        # Making listbox for showing suggested routes
            # Making frame for self.suggestedRouteListbox scrollbar
        suggestedRouteFrame = Frame(detailsFrame)
        suggestedRouteYScrollbar = Scrollbar(suggestedRouteFrame, orient=VERTICAL)
        suggestedRouteXScrollbar = Scrollbar(suggestedRouteFrame, orient=HORIZONTAL)
            # Making listbox into the frame
        self.suggestedRouteListbox = Listbox(suggestedRouteFrame, yscrollcommand=suggestedRouteYScrollbar.set, xscrollcommand=suggestedRouteXScrollbar.set, height=30)
            # Configuring the scrollbar
        suggestedRouteYScrollbar.config(command=self.suggestedRouteListbox.yview)
        suggestedRouteYScrollbar.pack(side=RIGHT, fill=Y)
        suggestedRouteXScrollbar.config(command=self.suggestedRouteListbox.xview)
        suggestedRouteXScrollbar.pack(side=BOTTOM, fill=X)
            # packing listbox & frame
        self.suggestedRouteListbox.pack(fill=X)
        suggestedRouteFrame.grid(row=4, column=0, columnspan=2, padx=30, pady=10, sticky='ew')


        detailsFrame.pack(fill=BOTH, expand=1)
        self.canvas1.create_window((0,0), window=canvas1Frame1, anchor=NW)
        self.canvas1.pack(side=LEFT, fill=BOTH, expand=1)
        # self.canvas1.bind("<Configure>", lambda e: self.canvas1.config(scrollregion = self.canvas1.bbox("all")))
        wrepper1.bind("<Configure>", lambda e: self.canvas1.config(scrollregion = self.canvas1.bbox("all")))
        wrepper1.pack(padx=10, pady=10, fill=BOTH, expand=1)


        # Making the combobox for selection of route
        self.selectedRoute = StringVar()
        self.selectedRoute.set("Select the route")
        self.selectRoute = ttk.Combobox(canvas1Frame1, textvariable=self.selectedRoute, width=30, font=("Helvetica", 14))
        self.selectRoute["values"] = self.routeList
        self.selectRoute["state"] = 'readonly' # or normal
        self.selectRoute.pack(fill=X)
        self.selectRoute.bind('<<ComboboxSelected>>', self.routeIsSelected)

        self.ListoutAllStation()
        self.root.mainloop()

if __name__=="__main__":
    route_analyser_app().run()