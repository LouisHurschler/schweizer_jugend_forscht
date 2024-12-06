// #import "template.typ"
// #show: doc => template
#let template(doc) = [
  #set text(font: "Roboto", size: 8pt)
  #set page(numbering:"1", flipped: true, columns: 4)
  #show link: underline
  #doc
  #set raw(tab-size: 4)

]


#let separator = {
  line(length: 100%, stroke: (thickness: 0.25pt, dash: "dashed"))
}
