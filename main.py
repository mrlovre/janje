import tkinter as tk
import io
import urllib.request
import PIL.Image as pim
import PIL.ImageTk as pimtk
import pyquery as pq

current_no = 1


def set_current_no(new_value):
    if new_value is not None and 1 <= new_value <= 151:
        global current_no
        current_no = new_value


def main():
    win = tk.Tk()
    win.wm_title('Pokedex')
    btn_prev = tk.Button(win, text='<')
    btn_prev.pack(side='left')
    btn_next = tk.Button(win, text='>')
    btn_next.pack(side='right')
    fr_selector = tk.Frame(win)
    ent_num = tk.Entry(fr_selector, width=5)
    ent_num.pack(side='left')
    btn_go = tk.Button(fr_selector, border=3, text='Go!')
    btn_go.pack(side='left')
    canvas = tk.Canvas(win, relief='sunken', width='4c', height='4c', border=5)
    canvas.pack(side='top')
    o = canvas['border']
    canvas_image = canvas.create_image(o, o, anchor='nw')
    im_size = int(canvas['width']), int(canvas['height'])
    lbl_name = tk.Label(win, font=('TkDefaultFont', '12', 'bold'))
    lbl_name.pack(side='top')
    msg_desc = tk.Message(win, width='4c')
    msg_desc.pack(side='top')
    fr_selector.pack(side='top')
    im_pokemon = None

    def btn_callback(btn):

        def callback():
            if btn['text'] == '<':
                set_current_no(current_no - 1)
            elif btn['text'] == '>':
                set_current_no(current_no + 1)
            elif btn['text'] == 'Go!':
                value = try_parse(ent_num.get(), int)
                set_current_no(value)
                ent_num.delete(0, 'end')
            else:
                return
            refresh_gui()

        return callback

    btn_prev['command'] = btn_callback(btn_prev)
    btn_next['command'] = btn_callback(btn_next)
    btn_go['command'] = btn_callback(btn_go)

    def refresh_gui():
        name, desc = scrape_data(get_url(current_no), ['name', 'desc'])
        lbl_name['text'] = name
        msg_desc['text'] = desc
        nonlocal im_pokemon
        im_pokemon = open_image(get_image_url(current_no), size=im_size)
        canvas.delete()
        show_image(canvas, im_pokemon, canvas_image)
        btn_prev['state'] = 'normal'
        btn_next['state'] = 'normal'
        if current_no <= 1:
            btn_prev['state'] = 'disabled'
        elif current_no >= 151:
            btn_next['state'] = 'disabled'
        win.pack_slaves()

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
        desc = (document('b:contains("Flavour Text")')
                .parents('table').eq(1).find('tr').eq(3).find('td').eq(1).html().strip())
        rval += desc,
    return rval


def get_image_url(no):
    return 'http://www.serebii.net/art/th/{}.png'.format(no)


def try_parse(s, f):
    try:
        return f(s)
    except ValueError:
        return None


if __name__ == '__main__':
    main()
