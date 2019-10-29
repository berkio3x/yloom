from tkinter import Tk
import glob
from tkinter.ttk import Treeview
from tkinter import Frame




root = Tk()

tree = Treeview()
tree.insert('', 'end', 'widgets', text='Widget Tour')
 
# Same thing, but inserted as first child:
tree.insert('', 0, 'gallery', text='Applications')

# Treeview chooses the id:
id = tree.insert('', 'end', text='Tutorial')

# Inserted underneath an existing node:
tree.insert('widgets', 'end', text='Canvas')
tree.insert(id, 'end', text='Tree')
tree.grid(row=1,column=1)


root.configure(bg='#272822')
root.geometry("600x500")

from collections import defaultdict

#def createTree(tree, node):
#    """
#        Tree = {a:
#                    {
#                        b: {
#                            c: {}
#                        },
#                        d: {
#                            e: {}
#                        }
#                    }
#                x : {
#                    y: {}
#                }
#                    
#
#    """
#    if node == {}:
#        d
#    t = tree.insert(node, 'end', text=node)
#    createTree(t,
#    
#    return tree
    

def getFiles(path):
    #d = defaultdict({})
    files = glob.glob(f"{path}/**", recursive=True)
    dct = {}
    for f in files:
        p = dct
        for i in  f.split('/'):
            p = p.setdefault(i,{})
        
    return dct


def createTree(files):
    """
        /a/b/c
        /a/b/c/d
        /a/b/c/d/e
        /a/b/f

        {a:{b:{c:{d:{e:None}},f:None}
    """
    d = {}
    for i in files:
        items = i.split('/')
            
    
        



    for f in files:
        items= f.split('/')
        head = items[0]
        tail = items[1:]


if __name__ == '__main__':
    files = getFiles("/Users/dev/Downloads/v8pbackend")
    import pprint; pprint.pprint(files)
    


    tree = createTree(files)

root.mainloop()
