import tkinter
# import tkinter.ttk
import pygubu
import netifaces


class AppGui:
    def __init__(self, rootWindow):
        self.mainFrame = rootWindow
        self.mainFrame.resizable(False, False)
        # Подключаем Рисовалку гуев
        self.mainFrameBuilder = pygubu.Builder() 
        # Загружаем в Рисовалку файл с описанием что и где рисовать 
        self.mainFrameBuilder.add_from_file('MainGUI.ui')
        # Загружаем объект mainFrame гуев в наше главное окно mainWindow  
        self.mainFrame = self.mainFrameBuilder.get_object('mainFrame', self.mainFrame)
        #builder.connect_callbacks(mainFrame)

        # Добываем объекты типа Text и прикрепляем соответствующие Scrollbar'ы
            # Тут окно вывода сообщений + scrollbar
        self.messageViewer = self.mainFrameBuilder.get_object('messageViewer', self.mainFrame)
        self.messageViewer_scroll = self.mainFrameBuilder.get_object('messageViewer_scroll', self.mainFrame)
                # Прикрепляем scrollbar к окну 
        self.messageViewer_scroll['command'] = self.messageViewer.yview
        self.messageViewer['yscrollcommand'] = self.messageViewer_scroll.set
            # Тут окно подключенных пользователей
        self.membersList = self.mainFrameBuilder.get_object('membersList', self.mainFrame)
        self.membersList_scroll = self.mainFrameBuilder.get_object('membersList_scroll', self.mainFrame)
                # Прикрепляем скролл
        self.membersList_scroll['command'] = self.membersList.yview
        self.membersList['yscrollcommand'] = self.membersList_scroll.set

        # Достаем кнопку конфигурации 
        self.configButton = self.mainFrameBuilder.get_object('configButton', self.mainFrame)
            # Кнопка конфигурации вызывает метод в котором рисуется новое меню  
        self.configButton.config(command = self.configMenu)

        
    def configMenu(self):
        # Создаем новое окно
        self.configMenuFrame = tkinter.Tk()
        self.configMenuFrame.resizable(False, False)
        # builderConfigMenu = pygubu.Builder().add_from_file('C:/Users/Dimasik/Projects/Python3_5_2/SimpleChat/configMenu.ui')
            # Так не правильно; так мы присваиваем, объекту builderConfigMenu, результат 
            # работы метода add_from_file. 
            # Я думал так: сначала объект builderConfigMenu инициализируется с помощью определения его
            # класса, а потом для него вызывается метод add_from_file.
        # Так правильно 
        self.builderConfigMenu = pygubu.Builder()
        self.builderConfigMenu.add_from_file('configMenu.ui')
        
        # Достаем окошко конфига и рисуем его на окно configMenu
        self.configMenuFrame = self.builderConfigMenu.get_object('configMenu', self.configMenuFrame)
        # Достаём все элементы 
        self.autoSearchUseID = self.builderConfigMenu.get_object('autoSearchUseID', self.configMenuFrame)
        self.entryID = self.builderConfigMenu.get_object('entryID', self.configMenuFrame)
        self.entryIP = self.builderConfigMenu.get_object('entryIP', self.configMenuFrame)
        self.entryPort = self.builderConfigMenu.get_object('entryPort', self.configMenuFrame)
        self.entryMask = self.builderConfigMenu.get_object('entryMask', self.configMenuFrame)
        self.confirmButton = self.builderConfigMenu.get_object('confirmButton', self.configMenuFrame)
        # Кнопка выбора "роли" Auto; Client; Server.
        self.selectRole = self.builderConfigMenu.get_object('selectRole', self.configMenuFrame)
        self.selectRole_menu = tkinter.Menu(self.selectRole, tearoff = False)
        self.selectRole['menu'] = self.selectRole_menu 
        
        # Тут должна быть функция(метод) которая изменяет состояние entryID 
        # в зависимости от состояния кнопки
        def setStateEntryID():
            if self.intState.get() == 1:
                self.entryID.config(state = 'normal')
            elif self.intState.get() == 0:
                self.entryID.config(state = 'disabled')                
        # Тут указываем переменную (self.intState) для Checkbutton'ины --> autoSearchUseID 
        # !!! и указываем окно(master = self.configMenuFrame) в котором будет отрабатываться 
        # наша Checkbutton'ина иначе, при изменении состояния, значение переменной меняться не будет, 
        # т.к. Checkbutton'ина будет плавать в окне configMenuFrame а её переменная хз где.
        self.intState = tkinter.BooleanVar(master = self.configMenuFrame)
        # А тут определяем саму Checkbutton'ину и её параметрами.
        self.autoSearchUseID.config(variable = self.intState, command = setStateEntryID, onvalue = 1, offvalue = 0)

        # Простенькое замыкание. Возвращает функцию которая помнит в какое состояние 
        # нужно выставить параметр 'text' менюшки selectRole. 
        # Без замыканий наглядней, но их тоже надо освоить.
        # TODO: допилить выставление состояния остальных полей и Checkbutton'ов.
        def checkButton(state):
            def setRole():
                # Сразу меняем надпись на кнопке
                self.selectRole.config(text = state)
                if state == 'Server':
                    autoSearchUseID.config(state = 'normal')
                    entryID.config(state = 'normal')
                    entryIP.delete(0, 100)
                    entryIP.insert(0, NetworkCSA.getIPthisPC())
                    entryIP.config(state = 'disable')
                    entryMask.config(state = 'disable')
                elif state == 'Client':
                    entryIP.delete(0, 100)
                    entryIP.insert(0, NetworkCSA.getIPthisPC())
                    entryIP.config(state = 'disable')
                    entryMask.config(state = 'disable')
                elif state == 'Auto':
                    pass
            
            return setRole

        stateAuto = checkButton('AutoSearch')
        stateClient = checkButton('Client')
        stateServer = checkButton('Server')
        
        selectRole_menu.add_command(label = 'AutoSearch', command = stateAuto)
        selectRole_menu.add_command(label = 'Client', command = stateClient)
        selectRole_menu.add_command(label = 'Server', command = stateServer)
        
        
        # Запускаем обработчик окна
        configMenu.mainloop()

    
        


class NetworkCSA:
    def getIPthisPC():
        ifacesThisPC = netifaces.interfaces()
        ipThisPC = netifaces.ifaddresses(ifacesThisPC[0]) 
        clearIP = ((ipThisPC[2])[0])['addr']
        return clearIP

rootW = tkinter.Tk()
AppGui(rootW)
rootW.mainloop()
