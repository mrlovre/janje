import tkinter as tk
import io
import urllib.request
import PIL.Image as pim
import PIL.ImageTk as pimtk
import pyquery as pq

current_no = 1


def main():
    win = tk.Tk()

    def btn_callback(btn):

        def callback():
            global current_no
            if btn['text'] == '<':
                if current_no > 1:
                    current_no -= 1
            elif btn['text'] == '>':
                if current_no < 151:
                    current_no += 1
            else:
                pass
            refresh_gui()

        return callback

    btn_prev = tk.Button(win, text='<')
    btn_prev['command'] = btn_callback(btn_prev)
    btn_prev.pack(side='left')
    btn_next = tk.Button(win, text='>')
    btn_next['command'] = btn_callback(btn_next)
    btn_next.pack(side='right')
    canvas = tk.Canvas(win, relief='sunken', width='4c', height='4c', border=5)
    canvas.pack(side='top')
    o = canvas['border']
    canvas_image = canvas.create_image(o, o, anchor='nw')
    im_size = int(canvas['width']), int(canvas['height'])
    lbl_name = tk.Label(win, font=('TkDefaultFont', '12', 'bold'))
    lbl_name.pack(side='top')
    msg_desc = tk.Message(win, width='4c')
    msg_desc.pack(side='top')
    im_pokemon = None

    def refresh_gui():
        name, desc = scrape_data(get_url(current_no), ['name', 'desc'])
        lbl_name['text'] = name
        msg_desc['text'] = desc
        nonlocal im_pokemon
        im_pokemon = open_image(get_image_url(current_no), size=im_size)
        canvas.delete()
        show_image(canvas, im_pokemon, canvas_image)

    refresh_gui()
    win.mainloop()


def open_image(url, size=None):
    data = urllib.request.urlopen(url).read()
    image = pim.open(io.BytesIO(data))
    if size is not None:
        image = pim.Image.resize(image, size, pim.ANTIALIAS)
    im = pimtk.PhotoImage(image)
    return im


def show_image(canvas, image, canvas_image):
    canvas.itemconfigure(canvas_image, image=image)


def get_url(no):
    return 'http://www.serebii.net/pokedex-rs/{:03d}.shtml'.format(no)


def scrape_data(url, what) -> tuple:
    rval = ()
    document = pq.PyQuery(url=url)
    if 'name' in what:
        name = document('.dextab').eq(0).find('table td').eq(1)('font b').html().strip()
        rval += name,
    if 'desc' in what:
        desc = document('b:contains("Flavour Text")').parents('table').eq(1).find('tr').eq(3).find('td').eq(
            1).html().strip()
        rval += desc,
    return rval


def get_image_url(no):
    return 'http://www.serebii.net/art/th/{}.png'.format(no)


if __name__ == '__main__':
    main()
