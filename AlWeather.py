from tkinter import Tk, Frame, SUNKEN, Label, Button
from tkinter import font, StringVar, BOTH, X, Entry
from tkinter import messagebox
from configparser import ConfigParser
from PIL import ImageTk, Image
import os
import requests
import geocoder
from datetime import datetime

cwd = os.path.dirname(os.path.realpath(__file__))


class AlWeather:
    def __init__(self):
        root = Tk(className=" ALWEATHER ")
        root.geometry("500x483+1410+550")
        root.resizable(0, 0)
        root.config(bg="white")
        root.iconbitmap(os.path.join(cwd+'\\UI\\icons', 'alweather.ico'))
        root.overrideredirect(1)
        mainframe = Frame(root, bg="white")

        def liftWindow():
            root.lift()
            root.after(1000, liftWindow)

        def callback(event):
            root.geometry("400x175+1500+840")

        def showScreen(event):
            root.deiconify()
            root.overrideredirect(1)

        def screenAppear(event):
            root.overrideredirect(1)

        def hideScreen():
            root.overrideredirect(0)
            root.iconify()

        configFile = cwd+'\\AlWeather\\config.ini'
        config = ConfigParser()
        config.read(configFile)
        apiKey = config['API_KEY']['key']
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

        def getWeather(city):
            try:
                result = requests.get(url.format(city, apiKey))
                if result:
                    json = result.json()
                    city = json['name']
                    country = json['sys']['country']
                    hum = json['main']['humidity']
                    win = json['wind']['speed']
                    win = win * 3.6
                    press = json['main']['pressure']
                    feelTemp = json['main']['feels_like']
                    feelTemp = feelTemp - 273.15
                    tempK = json['main']['temp']
                    tempC = tempK - 273.15
                    tempF = (tempK - 273.15) * 9 / 5 + 32
                    icon = json['weather'][0]['icon']
                    weather = json['weather'][0]['main']
                    description = json['weather'][0]['description']
                    zone = json['timezone']
                    sunr = json['sys']['sunrise']
                    sunr = sunr + zone
                    sunr = int(sunr)
                    sunr = datetime.utcfromtimestamp(sunr).strftime('%H:%M')
                    suns = json['sys']['sunset']
                    suns = suns + zone
                    suns = int(suns)
                    suns = datetime.utcfromtimestamp(suns).strftime('%H:%M')
                    final = (city.upper(), country, tempC, tempF, icon,
                             weather.upper(), description, hum, win, press,
                             feelTemp, sunr, suns)
                    return final
                else:
                    return None
            except Exception as e:
                print(e)
                error = 'Sorry for the inconvinience. Due to network issue ' \
                        'unable to give weather updates of current location.'
                messagebox.showerror('ALWEATHER ERROR', error)

        def search():
            city = cityVar.get()
            weather = getWeather(city)
            if weather:
                locationLabel['text'] = '{}, {}'.format(weather[0], weather[1])
                path = cwd+'\\AlWeather\\icons\\{}.png'.format(weather[4])
                img = ImageTk.PhotoImage(Image.open(path))
                imageLabel['image'] = img
                imageLabel.photo = img
                tempLabel['text'] = ('{:.2f} °C, {:.2f} °F'.format(weather[2],
                                     weather[3]))
                weatherLabel['text'] = weather[5]
                humidityLabel['text'] = '{} %'.format(weather[7])
                windLabel['text'] = '{:.2f} Km/h'.format(weather[8])
                pressureLabel['text'] = '{} hPa'.format(weather[9])
                sunriseLabel['text'] = '{}'.format(weather[11])
                sunsetLabel['text'] = '{}'.format(weather[12])
            else:
                messagebox.showerror('ALWEATHER ERROR',
                                     'Cannot find city {}'.format(city))

        textHighlightFont = font.Font(family='OnePlus Sans Display', size=10,
                                      weight='bold')
        appHighlightFont = font.Font(family='OnePlus Sans Display', size=12,
                                     weight='bold')

        titleBar = Frame(root, bg='#141414', relief=SUNKEN, bd=0)
        icon = Image.open(os.path.join(cwd + '\\UI\\icons',
                          'alweather.ico'))
        icon = icon.resize((30, 30), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
        iconLabel = Label(titleBar, image=icon)
        iconLabel.photo = icon
        iconLabel.config(bg='#141414')
        iconLabel.grid(row=0, column=0, sticky="nsew")
        titleLabel = Label(titleBar, text='ALWEATHER', fg='#909090',
                           bg='#141414', font=appHighlightFont)
        titleLabel.grid(row=0, column=1, sticky="nsew")
        closeButton = Button(titleBar, text="x", bg='#141414', fg="#909090",
                             borderwidth=0, command=root.destroy,
                             font=appHighlightFont)
        closeButton.grid(row=0, column=3, sticky="nsew")
        minimizeButton = Button(titleBar, text="-", bg='#141414', fg="#909090",
                                borderwidth=0, command=hideScreen,
                                font=appHighlightFont)
        minimizeButton.grid(row=0, column=2, sticky="nsew")
        titleBar.grid_columnconfigure(0, weight=1)
        titleBar.grid_columnconfigure(1, weight=30)
        titleBar.grid_columnconfigure(2, weight=1)
        titleBar.grid_columnconfigure(3, weight=1)
        titleBar.pack(fill=X)

        try:
            ipAddress = requests.get('http://api.ipify.org/').text
            location = geocoder.ip(ipAddress)
            defaultloc = getWeather(location.city)
            path = cwd+'\\AlWeather\\icons\\{}.png'.format(defaultloc[4])
            img = ImageTk.PhotoImage(Image.open(path))

            cityVar = StringVar()
            cityEntry = Entry(mainframe, textvariable=cityVar)
            cityEntry.config(bg='white', font=appHighlightFont,
                             highlightbackground='black',
                             highlightcolor='black', highlightthickness=3,
                             borderwidth=0, bd=0)
            cityEntry.pack(fill=X)

            weatherBtn = Button(mainframe, borderwidth=0, text='SEARCH',
                                command=search)
            weatherBtn.config(bg='black', fg='white', font=appHighlightFont,
                              height=2)
            weatherBtn.pack(fill=X)

            locationFrame = Frame(mainframe)

            locationLabel = Label(locationFrame,
                                  text='{}, {}'.format(defaultloc[0].upper(),
                                                       defaultloc[1].upper()))
            locationLabel.config(bg='white', font=appHighlightFont, height=2,
                                 highlightbackground='black',
                                 highlightcolor='black', highlightthickness=3,
                                 borderwidth=0)
            locationLabel.pack(fill=X)

            locationFrame.config(bg='white', highlightbackground='black',
                                 highlightcolor='black', highlightthickness=3,
                                 borderwidth=0, bd=0)
            locationFrame.pack(fill=X)

            frame = Frame(mainframe)

            sunrpng = Image.open(cwd+'\\AlWeather\\icons\\sunrise.png')
            sunrpng = sunrpng.resize((100, 100), Image.ANTIALIAS)
            sunrpng = ImageTk.PhotoImage(sunrpng)
            sunrico = Label(frame, image=sunrpng)
            sunrico.photo = sunrpng
            sunrico.config(bg='white')
            sunrico.grid(row=0, column=0, rowspan=2, sticky="nsew")

            sunrise = Label(frame, text='SUNRISE')
            sunrise.config(bg='white', font=textHighlightFont)
            sunrise.grid(row=0, column=1, sticky="nsew")

            sunriseLabel = Label(frame, text='{}'.format(defaultloc[11]))
            sunriseLabel.config(bg='white', font=textHighlightFont)
            sunriseLabel.grid(row=1, column=1, sticky="nsew")

            sunspng = Image.open(cwd+'\\AlWeather\\icons\\sunset.png')
            sunspng = sunspng.resize((100, 100), Image.ANTIALIAS)
            sunspng = ImageTk.PhotoImage(sunspng)
            sunsico = Label(frame, image=sunspng)
            sunsico.photo = sunspng
            sunsico.config(bg='white')
            sunsico.grid(row=0, column=2, rowspan=2, sticky="nsew")

            sunset = Label(frame, text='SUNSET')
            sunset.config(bg='white', font=textHighlightFont)
            sunset.grid(row=0, column=3, sticky="nsew")

            sunsetLabel = Label(frame, text='{}'.format(defaultloc[12]))
            sunsetLabel.config(bg='white', font=textHighlightFont)
            sunsetLabel.grid(row=1, column=3, sticky="nsew")

            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
            frame.grid_columnconfigure(3, weight=1)
            frame.config(bg='white', highlightbackground='black',
                         highlightcolor='black', highlightthickness=3,
                         borderwidth=0, bd=0)
            frame.pack(fill=X)

            imageFrame = Frame(mainframe)

            imageLabel = Label(imageFrame, image=img)
            imageLabel.photo = img
            imageLabel.config(bg='black', highlightbackground='black',
                              highlightcolor='black', highlightthickness=3,
                              borderwidth=0, bd=0)
            imageLabel.pack(fill=BOTH, expand=True)

            imageFrame.config(bg='black', highlightbackground='black',
                              highlightcolor='black', highlightthickness=3,
                              borderwidth=0, bd=0)
            imageFrame.pack(fill=X)

            horizontalFrame = Frame(mainframe)

            humidity = Label(horizontalFrame, text='HUMIDITY')
            humidity.config(bg='white', font=textHighlightFont)
            humidity.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            temp = Label(horizontalFrame, text='TEMPERATURE')
            temp.config(bg='white', font=textHighlightFont)
            temp.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

            weatherType = Label(horizontalFrame, text='WEATHER')
            weatherType.config(bg='white', font=textHighlightFont)
            weatherType.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

            wind = Label(horizontalFrame, text='WIND')
            wind.config(bg='white', font=textHighlightFont)
            wind.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

            pressure = Label(horizontalFrame, text='PRESSURE')
            pressure.config(bg='white', font=textHighlightFont)
            pressure.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

            humidityLabel = Label(horizontalFrame,
                                  text='{} %'.format(defaultloc[7]))
            humidityLabel.config(bg='white', font=textHighlightFont)
            humidityLabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

            tempLabel = Label(horizontalFrame,
                              text=f'{round(defaultloc[2], 2)} °C, ' +
                              f'{round(defaultloc[3],2)} °F')
            tempLabel.config(bg='white', font=textHighlightFont)
            tempLabel.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

            weatherLabel = Label(horizontalFrame, text=defaultloc[5].upper())
            weatherLabel.config(bg='white', font=textHighlightFont)
            weatherLabel.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

            windLabel = Label(horizontalFrame, text='{:.2f} Km/h'
                              ''.format(defaultloc[8]))
            windLabel.config(bg='white', font=textHighlightFont)
            windLabel.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

            pressureLabel = Label(horizontalFrame, text='{} hPa'
                                  ''.format(defaultloc[9]))
            pressureLabel.config(bg='white', font=textHighlightFont)
            pressureLabel.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")

            horizontalFrame.grid_columnconfigure(0, weight=1)
            horizontalFrame.grid_columnconfigure(1, weight=1)
            horizontalFrame.grid_columnconfigure(2, weight=1)
            horizontalFrame.grid_columnconfigure(3, weight=1)
            horizontalFrame.grid_columnconfigure(4, weight=1)
            horizontalFrame.config(bg='white', highlightbackground='black',
                                   highlightcolor='black',
                                   highlightthickness=3, borderwidth=0, bd=5)
            horizontalFrame.pack(fill=X)

            mainframe.config(bg='white', highlightbackground='black',
                             highlightcolor='black', highlightthickness=3,
                             borderwidth=0, bd=0)
            mainframe.pack(fill=BOTH, expand=True)

        except Exception as e:
            print(e)
            errorFrame = Frame(mainframe)

            errorpng = Image.open(cwd+'\\AlWeather\\icons\\inconvinience.png')
            errorpng = errorpng.resize((500, 450), Image.ANTIALIAS)
            errorpng = ImageTk.PhotoImage(errorpng)
            errorico = Label(errorFrame, image=errorpng)
            errorico.photo = errorpng
            errorico.config(bg='white')
            errorico.pack(fill=BOTH, expand=True)

            errorFrame.config(bg='white', highlightbackground='black',
                              highlightcolor='black', highlightthickness=3,
                              borderwidth=0, bd=0)
            errorFrame.pack(fill=X)

            mainframe.config(bg='white', highlightbackground='black',
                             highlightcolor='black', highlightthickness=3,
                             borderwidth=0, bd=0)
            mainframe.pack(fill=BOTH, expand=True)

        finally:
            titleBar.bind("<B1-Motion>", callback)
            titleBar.bind("<Button-3>", showScreen)
            titleBar.bind("<Map>", screenAppear)

            liftWindow()
            root.mainloop()


if __name__ == '__main__':
    AlWeather()
