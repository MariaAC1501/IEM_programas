import os
import pandas as pd
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZScope, TikZNode, TikZOptions, TikZCoordinate, TikZNodeAnchor, TikZPath,\
    UnsafeCommand,\
    VerticalSpace, HorizontalSpace, NewLine,\
    LongTable
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic

datos = pd.read_csv("malla_EM.csv")

def textcolor(size,vspace,color,bold,text,hspace="0"):
    dump = NoEscape(r"\par")
    if hspace!="0":
        dump += NoEscape(HorizontalSpace(hspace,star=True).dumps())
    dump += NoEscape(Command("fontsize",arguments=Arguments(size,vspace)).dumps())
    dump += NoEscape(Command("selectfont").dumps()) + NoEscape(" ")
    if bold==True:
        dump += NoEscape(Command("textbf", NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())).dumps())
    else:
        dump += NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())
    #dump += NoEscape("\par")
    return dump

def colocar_curso(codigo,nombre,columna,semestre,horasteoria,horaspractica,creditos,color):
    dump = NoEscape(f"\draw ({round(5*columna)},{round(-4*semestre)})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump




#print(cursos.head())


def generar_malla(programa):
    cursos = datos[datos.Programa == programa]
    #Geometry
    geometry_options = { 
        "left": "0mm",
        "right": "0mm",
        "top": "0mm",
        "bottom": "0mm",
        "headheight": "1mm",
        "footskip": "1mm"
    }
    #Document options
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper","lanscape"],
                   geometry_options=geometry_options)
    #Packages
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish',"activeacute"]))
    doc.packages.append(Package(name="graphicx"))
    doc.packages.append(Package(name="tikz"))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="xcolor"))
    doc.packages.append(Package(name="colortbl"))
    doc.packages.append(Package(name="array"))
    doc.packages.append(Package(name="float"))
    #doc.packages.append(Package(name="lastpage")) con pagenumbers+true
    doc.packages.append(Package(name="longtable"))
    doc.packages.append(Package(name="multirow"))
    doc.packages.append(Package(name="fancyhdr"))
    #Prueba
    bloqueCurso = NoEscape(
    r'''\tikzset{
            pics/curso/.style args={#1,#2,#3,#4,#5,#6}{
            code={
                \def\ancho{4}
                \def\alto{0.7}
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,-\alto) node[midway,align=center,text width=4cm]{\fontsize{10pt}{12pt}\selectfont \textbf{#2}};
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,\alto + \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #1};
                \draw[fill=#6] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
                \draw[fill=#6] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#6] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }'''
    )

        
    doc.preamble.append(bloqueCurso)
    
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.4",
                "transform shape"
                )
        )) as malla:
        for codigo in cursos.Codigo:
            print(codigo)
            nombre = cursos[cursos.Codigo == codigo].Nombre.item()
            columna = cursos[cursos.Codigo == codigo].Columna.item()
            semestre = cursos[cursos.Codigo == codigo].Semestre.item()
            horasteoria = cursos[cursos.Codigo == codigo].HorasTeoria.item()
            horaspractica = cursos[cursos.Codigo == codigo].HorasPractica.item()
            creditos = cursos[cursos.Codigo == codigo].Creditos.item()
            area = cursos[cursos.Codigo == codigo].Area.item()
            match area:
                case "Mecánica":
                    color = "teal"
                case "Básicas":
                    color = "lime"

            malla.append(colocar_curso(codigo,nombre,columna,semestre,horasteoria,horaspractica,creditos,color))
         
    doc.generate_pdf(f"./mallas/{programa}", clean=True, clean_tex=False, compiler='lualatex')


generar_malla("Electromecánica")