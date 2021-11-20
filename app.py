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
        
    def quit(self):
        self.finish_run()
        self.root.destroy()
    
    def __init__(self):
        
        self.finish = False
        self.wait = True
        
        self.root = tk.Tk()
        self.root.title('ScreenShoter')
        self.root.iconbitmap('slide_icon.ico')
        self.root.geometry("250x130")
        self.root.config(bg='dimgray', highlightcolor='white')
        
        self.root.protocol('WM_DELETE_WINDOW', self.quit)  

        self.root.tk_setPalette(background='#40E0D0', foreground='black',
               activeBackground='black', activeForeground='black')
        
        self.second_sleep = 1

        label_enter = tk.Label(bg= 'gray', height = 3, width = 35)
        label_enter.grid(row=0, column=0, columnspan=2)
#         label_enter = tk.Label(bg= 'gray', height = 3, width = 35)
#         label_enter.grid(row=0, column=1, columnspan=1)
        
        entry_name = tk.Entry(bg='cornflowerblue', width = 18)
        entry_name.grid(row=0,column=1,columnspan=2,padx=0,pady=10)
        
        # entry.pack()
#         print(help(tk.Button), sep ='\n\n',end='\n\n')
        
        button_start = tk.Button(self.root, text='start', padx=40, pady=20, command=lambda: self.run(entry_name), background='cornflowerblue')
        button_end = tk.Button(self.root, text='end', padx=40, pady=20, command = self.finish_run, background='cornflowerblue')

        button_start.grid(row=1, column=0, padx=0, pady=5)
        button_end.grid(row=1, column=1, pady=5)

        
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
            self.last_imgs = []
            
            self.cat = entry.get().replace(' ','_')
            if self.cat not in os.listdir():
                os.mkdir(self.cat)

            self.root.iconify()
            self.sleep(5)
            
            i = 0
            while True:

                mss().shot(mon=0, output=f'{self.cat}/screen.png')
                IMG = plt.imread(f'{self.cat}/screen.png')

                if i == 0:
#                     img  = get_slide(IMG)
                    img = IMG.copy()
                    plt.imsave(f'{self.cat}/{i}.png', img)
                    self.last_imgs.append(img.copy())

                    i += 1
                    self.sleep()
                    continue

#                 img_new =  get_slide(IMG)
                img_new = IMG.copy()
                
                slide_set = [the_same_slides(im_, img_new) for im_ in self.last_imgs[-5:]]
                if sum(slide_set) == 0:
                    i += 1
                    img = img_new
                    plt.imsave(f'{self.cat}/{i}.png', img)
                    self.last_imgs.append(img.copy())

                self.sleep()
                if self.finish:
                    break

            save_docx(self.cat)
            print('the work is done')
            self.wait = True

        
if __name__ == '__main__':
    ScreenShoter()