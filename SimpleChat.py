import tkinter
#import tkinter.ttk
import pygubu


class AppGui:
    def __init__(self, mainFrame):
        #mainFrame = mainFrame
        mainFrame.resizable(False, False)
        # Подключаем Рисовалку гуев
        builder = pygubu.Builder() 
        # Загружаем в Рисовалку файл с описание что и где рисовать 
        builder.add_from_file('C:/Users/Dimasik/Projects/Python3_5_2/SimpleChat/MainGUI.ui')
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
            # Я думал так сначала объект builderConfigMenu инициализируется с помощью определения его
            # класса, а потом для него вызывается метод add_from_file.
        # Так правильно
        builderConfigMenu = pygubu.Builder()
        builderConfigMenu.add_from_file('C:/Users/Dimasik/Projects/Python3_5_2/SimpleChat/configMenu.ui')
        
        # Достаем окошко конфига и рисуем его на окно configMenu
        configFrame = builderConfigMenu.get_object('configMenu', configMenu)
        
        confirmButton = builderConfigMenu.get_object('confirmButton', configFrame)
       
        def setServerConfig():
            serverConf = Server('ILovePython!', '192.168.1.1', 10000)
       
        confirmButton.config(command = setServerConfig)

        
        
        # Запускаем обработчик окна
        configMenu.mainloop()

class Server:
    def __init__(self, appID, appIP, appPort):
        self.appID = appID
        self.appIP = appIP
        self.appPort = appPort
        print(self.appID, self.appIP, self.appPort)



rootWindow = tkinter.Tk()
AppGui(rootWindow)
rootWindow.mainloop()
