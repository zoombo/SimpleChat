import tkinter
# import tkinter.ttk
import pygubu
import netifaces


class AppGui:
    def __init__(self, mainFrame):
        #mainFrame = mainFrame
        mainFrame.resizable(False, False)
        # Подключаем Рисовалку гуев
        builder = pygubu.Builder() 
        # Загружаем в Рисовалку файл с описание что и где рисовать 
        builder.add_from_file('MainGUI.ui')
        # Загружаем объект mainFrame гуев в наше главное окно mainWindow  
        mainFrame = builder.get_object('mainFrame', mainFrame)
        #builder.connect_callbacks(mainFrame)

        # Добываем объекты типа Text и прикрепляем соответствующие Scrollbar'ы
            # Тут окно вывода изображения
        messageViewer = builder.get_object('messageViewer', mainFrame)
        messageViewer_scroll = builder.get_object('messageViewer_scroll', mainFrame)
                # Прикрепляем скролл
        messageViewer_scroll['command'] = messageViewer.yview
        messageViewer['yscrollcommand'] = messageViewer_scroll.set
            # Тут окно подключенных пользователей
        membersList = builder.get_object('membersList', mainFrame)
        membersList_scroll = builder.get_object('membersList_scroll', mainFrame)
                # Прикрепляем скролл
        membersList_scroll['command'] = membersList.yview
        membersList['yscrollcommand'] = membersList_scroll.set

        # Достаем кнопку конфигурации 
        configButton = builder.get_object('configButton', mainFrame)
            # Кнопка конфигурации вызывает метод в котором рисуется новое меню  
        configButton.config(command = AppGui.configMenu)

        
    def configMenu():
        # Создаем новое окно
        configMenu = tkinter.Tk()
        configMenu.resizable(False, False)
        # builderConfigMenu = pygubu.Builder().add_from_file('C:/Users/Dimasik/Projects/Python3_5_2/SimpleChat/configMenu.ui')
            # Так не правильно; так мы присваиваем, объекту builderConfigMenu, результат 
            # работы метода add_from_file. 
            # Я думал так: сначала объект builderConfigMenu инициализируется с помощью определения его
            # класса, а потом для него вызывается метод add_from_file.
        # Так правильно 
        builderConfigMenu = pygubu.Builder()
        builderConfigMenu.add_from_file('configMenu.ui')
        
        # Достаем окошко конфига и рисуем его на окно configMenu
        configFrame = builderConfigMenu.get_object('configMenu', configMenu)
        # Достаём все элементы 
        autoSearchUseID = builderConfigMenu.get_object('autoSearchUseID', configFrame)
        entryID = builderConfigMenu.get_object('entryID', configFrame)
        entryIP = builderConfigMenu.get_object('entryIP', configFrame)
        entryPort = builderConfigMenu.get_object('entryPort', configFrame)
        entryMask = builderConfigMenu.get_object('entryMask', configFrame)
        confirmButton = builderConfigMenu.get_object('confirmButton', configFrame)
        # Кнопка выбора "роли" Auto; Client; Server.
        selectRole = builderConfigMenu.get_object('selectRole', configFrame)
        selectRole_menu = tkinter.Menu(selectRole, tearoff = False)
        selectRole['menu'] = selectRole_menu 
        
        # Тут должна быть функция которая изменяет состояние entryID 
        # в зависимости от состояния кнопки
        def setStateEntryID():
            if autoSearchUseID['variable'] == autoSearchUseID['onvalue']:
                entryID.config(state = 'normal')
            else:
                entryID.config(state = 'disable')
                


        autoSearchUseID.config(command = setStateEntryID)

        # Простенькое замыкание. Возвращает функцию которая помнит в какое состояние 
        # нужно выставить параметр 'text' менюшки selectRole. 
        # Без замыканий наглядней, с ними эффективней.
        # TODO: допилить выставление состояния остальных полей и Checkbutton'ов.
        def checkButton(state):
            def setRole():
                # Сразу меняем надпись на кнопке
                selectRole.config(text = state)
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

rootWindow = tkinter.Tk()
AppGui(rootWindow)
rootWindow.mainloop()
