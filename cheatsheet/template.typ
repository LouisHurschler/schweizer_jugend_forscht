// #import "template.typ"
// #show: doc => template
#let template(doc) = [
  #set text(font: "Roboto")
  #set page(numbering:"1", columns: 2)
  #show heading.where(level: 1): it => [
      #place(auto, scope: "parent", float: true)[
      #text(weight: "bold", it.body)
      ]
  ]
  #show link: underline
  #doc
]


#let two_col_text(body) = [
  #columns(2)[
    #body
  ]
]
