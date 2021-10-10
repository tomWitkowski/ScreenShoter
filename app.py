import tkinter as tk
import time, os
from threading import Thread
import matplotlib.pyplot as plt
from mss import mss
from slide_utils import flatten_screen, get_borders, get_slide, the_same_slides
from docx_utils import save_docx


class ScreenShoter:
    
    def thread(method):
        def inner(*args, **kwargs):
            Thread(target = lambda: method(*args, **kwargs)).start()
        return inner
        
    
    def __init__(self):
        
        self.finish = False
        self.wait = True
        
        self.root = tk.Tk()
        self.root.title('ScreenShoter')
        self.root.iconbitmap('slide_icon.ico')
        self.root.geometry("280x150")
        self.root.config(bg='dimgray', highlightcolor='white')
        
        self.root.tk_setPalette(background='#40E0D0', foreground='black',
               activeBackground='black', activeForeground='gray')
        
        self.second_sleep = 1

        entry_name = tk.Entry()
        entry_name.grid(row=0,column=0,columnspan=2,padx=20,pady=10)

        # entry.pack()
#         print(help(tk.Button), sep ='\n\n',end='\n\n')
        
        button_start = tk.Button(self.root, text='start', padx=40, pady=20, command=lambda: self.run(entry_name), background='cornflowerblue')
        button_end = tk.Button(self.root, text='end', padx=40, pady=20, command = self.finish_run, background='cornflowerblue')
        button_quit = tk.Button(self.root, text = 'quit', command = self.root.quit, background='tomato')

        button_start.grid(row=1, column=0, padx=4, pady=5)
        button_end.grid(row=1, column=1, pady=5)

        button_quit.grid(row=1, column=2, columnspan=2, padx=20, pady=50)
        
        self.root.mainloop()
        self.finish_run()
        
        
    def finish_run(self):
        self.finish = True

        
    def sleep(self, sec: float = None):
        if sec is None:
            sec = self.second_sleep
        
        for _ in range(int(sec*100)):
            time.sleep(0.01)
            if self.finish:
                break
        
    @thread
    def save(self):
        save_docx(self.cat)
        
        
    @thread
    def run(self, entry):
        
        if self.wait:
            self.wait = False
            
            self.cat = entry.get().replace(' ','_')
            if self.cat not in os.listdir():
                os.mkdir(self.cat)

            self.root.iconify()
            self.sleep(0.1)
            
            i = 0
            while True:

                mss().shot(mon=0, output=f'{self.cat}/screen.png')
                IMG = plt.imread(f'{self.cat}/screen.png')

                if i == 0:
                    img  = get_slide(IMG)
                    plt.imsave(f'{self.cat}/{i}.png', img)

                    i += 1
                    self.sleep()
                    continue

                img_new =  get_slide(IMG)

                if not the_same_slides(img, img_new):
                    i += 1
                    img = img_new
                    plt.imsave(f'{self.cat}/{i}.png', img)

                self.sleep()
                if self.finish:
                    break

            save_docx(self.cat)
            print('the work is done')
            self.wait = True

        
if __name__ == '__main__':
    ScreenShoter()