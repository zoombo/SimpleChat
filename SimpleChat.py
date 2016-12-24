import tkinter
#import tkinter.ttk
import pygubu


mainFrame = tkinter.Tk()
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

mainFrame.mainloop()


