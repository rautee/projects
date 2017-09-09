from IPython.display import display, HTML, clear_output

from ipywidgets import *

class ButtonN(Button):
    def __init__(self, n, nHandler, **kwargs):
        super(Button, self).__init__(**kwargs)
        self._click_handlers = CallbackDispatcher()
        self.on_msg(self._handle_button_msg)
        self.n = n
        self.__nHandler = nHandler
    def _handle_button_msg(self, _, content, buffers):
        """Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
            Content of the msg.
        """
        if content.get('event', '') == 'click':
            self._click_handlers(self)
            if self.__nHandler is not None:
                self.__nHandler(self.n)


class tttGameHandler:
    pathRefs = {
                        'row 1':{0,1,2},'row 2':{3,4,5},'row 3':{6,7,8},
                        'col 1':{0,3,6},'col 2':{1,4,7},'col 3':{2,5,8},
                        'dia 1':{0,4,8},'dia 2':{2,4,6}
    }
        
    tileRefs = {
                        0: {'col 1', 'dia 1', 'row 1'},1: {'col 2', 'row 1'},
                        2: {'col 3', 'dia 2', 'row 1'},3: {'col 1', 'row 2'},
                        4: {'col 2', 'dia 1', 'dia 2', 'row 2'},
                        5: {'col 3', 'row 2'},6: {'col 1', 'dia 2', 'row 3'},
                        7: {'col 2', 'row 3'},8: {'col 3', 'dia 1', 'row 3'}
    }
    
    def __init__(self, ai_vs = -1):
        self.turn = 1    
        self.player = 1
        self.winner = 0
        self.unoccupiedTiles = set(list(range(9)))
        self.tileValues=[0,0,0,0,0,0,0,0,0]
        self.AI = tttAI(self, play_with = ai_vs)

        self.__defaultLayout = Layout(width = "40px", height="40px", border = '2px solid #98a3ad')
        self.__defaultStyle = ButtonStyle(button_color = 'white')
        self.__p1Layout = Layout(width = "40px", height="40px", border = '2px solid #40c960')
        self.__p1Style = ButtonStyle(button_color='#e5f9ee')
        self.__p2Layout = Layout(width = "40px", height="40px", border = '2px solid #348de5')
        self.__p2Style = ButtonStyle(button_color='#e3f3f9')
        self.__winLayout = Layout(width = "40px", height="40px", border = '2px solid #ffd800')
        self.__winStyle = ButtonStyle(button_color='#FFF051')

        self.tileButtons = [ButtonN(n, self, layout = self.__defaultLayout, 
                                 style = self.__defaultStyle) for n in range(9)]
        for n in range(9):
            self.tileButtons[n].on_click(self.click)

        self.HUD = HTMLMath(value = '')
        self.updateHUD()

        self.displayBox = VBox([HBox([self.HUD], layout=Layout(justify_content='center')),
                                HBox(self.tileButtons[0:3], layout=Layout(justify_content='center')),
                                HBox(self.tileButtons[3:6], layout=Layout(justify_content='center')),
                                HBox(self.tileButtons[6:9], layout=Layout(justify_content='center'))])

        display(self.displayBox)
        self.AI.play()
    
    def getNthTileValue(self,n):
        if n >= 0 and n < 9:
            return self.tileValues[n]
        
    
    def getNthTileButton(self,n):
        if n >= 0 and n < 9:
            return self.tileButtons[n]
        
    
    def getPathValues(self,pathRef):
        if pathRef in self.pathRefs.keys():
            path = []
            for n in self.pathRefs[pathRef]:
                path += [self.getNthTileValue(n)]
            return tuple(path)
        else: return None
    
    def getPathButtons(self,pathRef):
        if pathRef in self.pathRefs.keys():
            path = []
            for n in self.pathRefs[pathRef]:
                path += [self.getNthTileButton(n)]
            return tuple(path)
        else: return None
    
    def checkWin(self):
        winner = None
        for pathRef in self.pathRefs:
            value = sum(self.getPathValues(pathRef))
            if value in (3,-3):
                self.highlightWin(pathRef)
                self.winner = 1 if value > 0 else 2
                #print(f'and increased self.turn from {self.turn} to 10*')
                self.turn = 10
    
    def highlightWin(self, pathRef):
        for button in self.getPathButtons(pathRef):
            button.style = self.__winStyle
            button.layout = self.__winLayout
    
    def updateHUD(self):
        if self.turn <= 9:
            #print(f'updated for {self.player} at turn {self.turn}')
            self.HUD.value = "<b><font color = '{color}'>Player {player}</font> [{mark}]</b>".format(
                color = '40c960' if self.player == 1 else '348de5', player=self.player, 
                mark = '✕' if self.player == 1 else '⭘')
        elif self.turn == 10:
            self.HUD.value ="""<b><font size = 4 color = '9700ef'>Game Over</font></b>
                            <br> <font size = 5 color = {text}</font>""".format(
                            text = '"#ff6600"> Player 1 <b>WON</b>!' if self.winner is 1 
                            else ('"#ff6600"> Player 2 <b>WON</b>!' if self.winner is 2
                            else '"#ffc700"> DRAW'))
    
    def updatePlayer(self):
        self.player = 1 if self.turn%2==1 else 2
    
    def markButton(self,n):
        if self.turn%2 == 1:
            self.tileButtons[n].description = '✕'
            self.tileButtons[n].layout = self.__p1Layout
            self.tileButtons[n].style = self.__p1Style
            self.tileValues[n] = 1
            
        else:
            self.tileButtons[n].description = '⭘'
            self.tileButtons[n].layout = self.__p2Layout
            self.tileButtons[n].style = self.__p2Style
            self.tileValues[n] = -1
    
    def click(self,b):
            pass
    
    def __call__(self, n):
        if self.turn <= 9 and n in self.unoccupiedTiles:
            self.markButton(n)
            current_tile = n
            self.unoccupiedTiles -= {n}
            self.AI.observe(n)
            self.turn += 1
            self.updatePlayer()
            #print(f'increased self.turn from {self.turn-1} to {self.turn} ^-^')
            self.checkWin()
            self.updateHUD()
            self.AI.play()


class tttAI:
    from random import randint
    from random import choice as rand
    def __init__(self, tttHandler, play_with = 1):
        self.game = tttHandler
        self.info = tttAIinfo()
        if play_with not in {-1,0,1,2}: raise ValueError('play_with must be a value from {0,1,2}')
        self.playnow = 1 if play_with in {2,0} else (-1 if play_with == -1 else 2)
        self.nextturn = 2 if play_with in {1,2} else (-1 if play_with == -1 else 1)
    
    def observe(self, n):
        currentplayer = self.game.player
        thisturn = self.game.turn
        self.info.update(currentplayer, n)
    
    def randTile(self):
        l = len(self.game.unoccupiedTiles)
        availabletiles = list(self.game.unoccupiedTiles)
        rand_i = self.randint(0,l-1)
        return availabletiles[rand_i]
    
    def selectTile(self):
        n = -1
        currentplayer = self.game.player
        otherplayer = 1 if currentplayer == 2 else 2
        thisturn = self.game.turn
        inactive = {True:[1,2],False:[]}
        active = {1:{True:[1],False:[2]}, 2:{True:[2],False:[1]}}
        if thisturn == 1:
            n = self.rand(range(0,9))
        elif thisturn == 2:
            n = 4 if 4 in self.game.unoccupiedTiles else self.rand([0,2,6,8])
        elif thisturn == 3:
            activetiles = self.info.activetiles(currentplayer)
            tiles = {}
            maxcount = 0
            options = []
            for tilenum in self.game.unoccupiedTiles:
                paths = self.info.tileset[tilenum](inactive, True)
                tiles[tilenum] = set()
                for path in paths:
                    tiles[tilenum] |= path(inactive, True)
                tiles[tilenum] -= {tilenum}
                l = len(tiles[tilenum]&activetiles)
                if l > maxcount:
                    options = [tilenum]
                    maxcount = l
                elif l == maxcount:
                    options += [tilenum]
                else: pass
            n = self.rand(options)
        elif thisturn == 4:
            n = self.info.stoptrapfrom(otherplayer)
            if n < 0:
                n = self.stopnodetrapfrom(otherplayer)
        elif thisturn < 10 :
            n = self.info.finishtrap(currentplayer)
            if n < 0: n = self.info.stoptrapfrom(otherplayer)
            if n < 0: n = self.stopnodetrapfrom(otherplayer)
            if n < 0:
                nodes = self.info.nodetiles(currentplayer)
                nodes = nodes[2] | nodes[3]
                n = self.rand(list(nodes)) if len(nodes) > 0 else -1
            if n < 0:
                activetiles = self.info.activetiles(currentplayer)
                oppactivetiles = self.info.activetiles(otherplayer)
                if len(activetiles) > 0:
                    n = self.rand(list(activetiles))
                elif len(oppactivetiles) > 0:
                    n = self.rand(list(oppactivetiles))
                else: n = -1
            if n < 0: n = self.rand(list(self.game.unoccupiedTiles))
        
        return n.id if isinstance(n, dooredset) else n
    
    def stopnodetrapfrom(self, otherplayer):
        currentplayer = 2 if otherplayer == 1 else 1
        n = -1
        inactive = {True:[1,2],False:[]}
        nodes = self.info.nodetiles(otherplayer) # dict key is the num of paths intersecting for each node in set of nodes
        options = []
        for path in self.info.activepaths(currentplayer):
            tilelist = tuple(path(inactive, True))
            if not self.info.isnode(tilelist[0], otherplayer):
                if not self.info.isnode(tilelist[1], otherplayer):
                    options += list(tilelist)
                else:
                    options += [tilelist[1]]
            else:
                if not self.info.isnode(tilelist[1], otherplayer):
                    options += [tilelist[0]]
            if len(options) == 0:
                if len(nodes[3]) == 0:
                    n = self.rand(list(nodes[2]))
                else:
                    n = self.rand(list(nodes[3]))
            else:
                n = self.rand(options)
        return n.id if isinstance(n, dooredset) else n
    
    def sleep(self):
        x = 1
        while x != 2**22:
            x+=1
            
    def play(self):
        if (self.game.turn <= 9):
            
            ai_n = self.selectTile()
            
            if self.playnow == self.game.turn:
                self.playnow += self.nextturn
                self.sleep()
                if ai_n > -1:
                    self.game(ai_n)
            
            

class tttAIinfo:
    from random import choice as __rand
    inactive = {True:[1,2],False:[]}
    active = {1:{True:[1],False:[2]}, 2:{True:[2],False:[1]}}
    def __init__(self):
        self.paths = tttGameHandler.pathRefs
        self.tiles = tttGameHandler.tileRefs
        
        self.occupiedtiles = {1: set(), 2: set()}
        
        self.basedoor = {} # self.basedoor[tilenum][player],[key] returns bool
        self.tiledoor = {} # self.tiledoor[tilenum],[key] returns bool
        self.pathdoor = {} # self.pathdoor[pthname],[key] returns bool
        self.tileset = {}  # self.tileset[tilenum],[key] returns set(dooredset paths)
        self.pathset = {}  # self.pathset[pthname],[key] returns set(dooredset tiles)
        
        for i in range(9):
            self.basedoor[i] = {1:door(1),2:door(2)}
            self.tiledoor[i] = door(self.basedoor[i][1] | self.basedoor[i][2])
            self.tileset[i] = dooredset(self.tiledoor[i])

            self.basedoor[i][1].setid(f'b{i}')
            self.basedoor[i][2].setid(f'b{i}')
            self.tiledoor[i].setid(i)
            self.tileset[i].setid(i)
            #self.tileset[i].setdata([f'~t{i} Data~'])

        for pathkey in self.paths:
            doorlist = {}
            for tilenum, i in zip(self.paths[pathkey], range(len(self.paths[pathkey]))):
                if i == 0:
                    doorlist[1] = self.basedoor[tilenum][1]
                    doorlist[2] = self.basedoor[tilenum][2]
                else:
                    doorlist[1] &= self.basedoor[tilenum][1]
                    doorlist[2] &= self.basedoor[tilenum][2]
            self.pathdoor[pathkey] = door(doorlist[1]|doorlist[2])
            self.pathset[pathkey] = dooredset(self.pathdoor[pathkey])

            self.pathdoor[pathkey].setid(f'{pathkey}')
            self.pathset[pathkey].setid(f'{pathkey}')
            #self.pathset[pathkey].setdata([f'~{pathkey} Data~'])

        for tile in self.tiles:
            data = []
            for pathname in self.tiles[tile]:
                data += [self.pathset[pathname]]
            self.tileset[tile].setdata(data)

        for path in self.paths:
            data = []
            for i in self.paths[path]:
                data += [self.tileset[i]]
            self.pathset[path].setdata(data)
    
    def update(self, player, n):
        opp = 1 if player == 2 else 2
        self.basedoor[n][opp].disable()
        self.occupiedtiles[player] |= {self.tileset[n]}
        
    
    def activetiles(self, player):
        opp = 1 if player == 2 else 2
        actvtiles = set()
        for tile in self.occupiedtiles[player]:
            for path in tile[player]:
                for pathtile in path[player]:
                    if pathtile(self.inactive):
                        actvtiles |= set([pathtile])
        return actvtiles
    
    def activepaths(self, player):
        opp = 1 if player == 2 else 2
        actvpaths = set()
        for tile in self.occupiedtiles[player]:
            for path in tile[player]:
                if path({True: player, False: opp}):
                    actvpaths |= {path}
        return actvpaths
    
    def stoptrapfrom(self, player):
        halftiles = []
        for path in self.activepaths(player):
            if len(path(self.active[player], True)) == 2:
                halftiles += list(path(self.inactive, True))
        if len(halftiles) > 0:
            n = self.__rand(halftiles)
            return n.id
        return -1
                
    def finishtrap(self, player):
        return self.stoptrapfrom(player)
    
    def nodetiles(self, player):
        nodes = {2:set(),3:set()}
        for tilenum in self.activetiles(player):
            l = len(self.tileset[tilenum](self.active[player],True))
            if l > 1:
                nodes[l] |= {self.tileset[tilenum]}
        return nodes
    
    def isnode(self, tile, player):
        if tile in self.activetiles(player):
            return len(tile(self.active[player],True)) > 1
        return False
                
class tttMain:
    def __init__(self):
        
        self.__buttonStyle = ButtonStyle(button_color = '#FFFBA0', font_weight = 'bold') 
        self.__buttonLayout = Layout(border = '2px solid #ffd800', height = '40px', width='180px')
        self.banner = HTML(value = '<font size=6 color="#FFD400">Chicky<font><font size=6 color="#ff6600"><b>Toe</b></font>')
        self.bannerBox = HBox([self.banner], layout=Layout(justify_content='center')) 
        self.widgets = [Button(description='P1 vs P2', style=self.__buttonStyle, layout=self.__buttonLayout),
                        Button(description='P1 vs Computer', style=self.__buttonStyle,layout=self.__buttonLayout),
                        Button(description='P2 vs Computer',style=self.__buttonStyle,layout=self.__buttonLayout),
                        Button(description='Computer vs Computer',style=self.__buttonStyle,layout=self.__buttonLayout)]
        
        self.mainBox = HBox([VBox(self.widgets)], layout=Layout(justify_content='center')) 
        
        self.back = Button(description='Back', style=ButtonStyle(button_color = 'white') ,
                           layout=Layout(border = '2px solid #f4ebb7', height = '35px', width='70px'))
        def back(b):
            clear_output()
            del self.t
            self.t = None
            self.__init__()
        
        self.back.on_click(back)
        
        def showback():
            self.subwidgets = HBox([self.back])
            display(self.subwidgets)
        
        def p1vsp2(b):
            clear_output()
            del self.mainBox
            display(self.bannerBox)
            self.t = tttGameHandler(ai_vs = -1)
            showback()
        self.widgets[0].on_click(p1vsp2)
        
        def p1vspc(b):
            clear_output()
            del self.mainBox
            display(self.bannerBox)
            self.t = tttGameHandler(ai_vs = 1)
            showback()
        
        self.widgets[1].on_click(p1vspc)
        
        def p2vspc(b):
            clear_output()
            del self.mainBox
            display(self.bannerBox)
            self.t = tttGameHandler(ai_vs = 2)
            showback()
        
        self.widgets[2].on_click(p2vspc)
        
        def pcvspc(b):
            clear_output()
            del self.mainBox
            display(self.bannerBox)
            self.t = tttGameHandler(ai_vs = 0)
            showback()
            
        self.widgets[3].on_click(pcvspc)
        
        display(self.bannerBox, self.mainBox)


class door:
    from collections import Hashable as __hashable
    from collections import Iterable as __iterable
    from math import inf as __highorder
    def __init__(self, key):
        self.__disable = False
        self.id = ''
        if isinstance(key, self.__doorlist):
            self.__order = self.__highorder
            self.__key = key
            #print('Higher order Door initialized.')
        elif isinstance(key, self.__hashable):
            self.__order = 0
            self.__key = {key: True}
            self.__keyrepr = str(key)
            #print('0th order Door initialized.')
        else: raise TypeError('`key` must be hashable or a list of doors')
            
    def setid(self, ID):
        self.id = ID
        
    def disable(self):
        self.__disable = True
        
    def enable(self):
        self.__disable = False
    
    def __getitem__(self, key):
        if self.__disable: return False
        
        if isinstance(key, dict):
            keys = key
            if set(keys) == {True,False}:
                if not (isinstance(keys[True], self.__iterable) and isinstance(keys[False], self.__iterable)):
                    keys[True] = [keys[True]]
                    keys[False] = [keys[False]]
                return all(self.__key[key] for key in keys[True]) and not any(self.__key[key] for key in keys[False])
            else: raise KeyError("Expected a dictionary with keys (True,False).")
        else:
            try:
                return self.__key[key]
            except KeyError:
                return False 
    
    def __and__(self, otherdoor):
        if isinstance(otherdoor, door):
            return self.__doorlist(self) & self.__doorlist(otherdoor)
        elif isinstance(otherdoor, self.__doorlist):
            return self.__doorlist(self) & otherdoor
        else: raise TypeError(f'Cannot combine door object with <{type(otherdoor)}> object using `&`.')

    def __or__(self, otherdoor):
        if isinstance(otherdoor, door):
            return self.__doorlist(self) | self.__doorlist(otherdoor)
        elif isinstance(otherdoor, self.__doorlist):
            return self.__doorlist(self) | otherdoor
        else: raise TypeError(f'Cannot combine door object with <{type(otherdoor)}> object using `|`.')
    
    def __repr__(self):
        s = f'{self.id}:'
        if self.__order == 0:
            s += self.__keyrepr
        else: s += repr(self.__key)
        s += '·ƒ' if self.__disable else '·τ'
        return s
            
    class __doorlist:
        def __init__(self, onedoor):
            if isinstance(onedoor, door):
                self.doors = [[onedoor]] 
        def __getitem__(self, key):
            return any( all(y[key] for y in x) for x in self.doors)
        def __and__(self, otherdoor):
            if isinstance(otherdoor, door):
                self.doors[0] += [otherdoor]
                return self
            elif isinstance(otherdoor, type(self)):
                self.doors[0] += otherdoor.doors[0]
                return self
            else: raise TypeError(f'Cannot combine door object with <{type(otherdoor)}> object using `&`.')
        
        def __or__(self, otherdoor):
            if isinstance(otherdoor, door):
                self.doors += [otherdoor]
                return self
            elif isinstance(otherdoor, type(self)):
                self.doors += otherdoor.doors
                return self
            else: raise TypeError(f'Cannot combine door object with <{type(otherdoor)}> object using `&`.')
        def __displist(self, alist):
            s = '['
            if isinstance(alist, (list, dict)):
                l = len(alist)
                for x, i in zip(alist, range(l)):
                    if isinstance(x, (list,dict)):
                        s += self.__displist(x)
                    else:
                        s += repr(x)
                    s += ',' if i < l-1 else ''
            s += ']'
            return s
        def __repr__(self):
            return self.__displist(self.doors)


class dooredset:
    from collections import Iterable as __iterable
    def __init__(self, doors):
        self.__data = None
        if isinstance(doors, door):
            self.__doors = doors
        else: raise TypeError("Non-door type passed through <doors> argument.")
            
    def setdata(self, data):
        self.__data = set(data)
        
    def setid(self, ID):
        self.id = ID
        
    
    def __call__(self, key, send_dooredsets_of_data =  False):
        if send_dooredsets_of_data:
            #print([[dat, type(dat)] for dat in self.__data])
            return {(dat if dat(key) else None) for dat in self.__data} - {None}
        return self.__doors[key] 
    
    def __repr__(self):
        data ='['
        l = len(self.__data)
        for x, i in zip(self.__data, range(l)):
            if isinstance(x, (dooredset,door)):
                data += (f'δ:{x.id}')
            else:
                data += str(x)
            data += ',' if i < l-1 else ''
        data += ']'
        return f'{self.id}'#: {data}' # » doors: {self.__doors}'
    
    def __getitem__(self, key):
        if isinstance(key, dict):
            keys = key
            if set(keys) == {True,False}:
                if not (isinstance(keys[True], self.__iterable) and isinstance(keys[False], self.__iterable)):
                    keys[True] = [keys[True]]
                    keys[False] = [keys[False]]
                    
                if all(self.__doors[key] for key in keys[True]) and not any(self.__doors[key] for key in keys[False]):
                    return self.__data
                
            else: raise KeyError("Expected a dictionary with keys (True,False).")
        if self.__doors[key]:
            return self.__data
        else: 
            return set()
    
    def __eq__(self, other):
        return other == self.id
    
    def __lt__(self, other):
        return self.id < other
    
    def __gt__(self, other):
        return self.id > other
        
    def __hash__(self):
        return hash(self.id)  
