let g:pymode_lint_checker = "pyflakes,pylint,pep8,mccabe"
let NERDTreeIgnore += ['\.egg$', '\.egg-info$', '\.ropeproject$', '\.tags$', 'dist']
au BufRead *.tmpl set ft=htmldjango
au BufRead *sh\.tmpl set ft=sh
