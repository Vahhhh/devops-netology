# devops-netology
1. this is test comment
1. this is second text comment - trying to view some changes in diff output

## Вот что не будет копироваться благодаря содержимому /terraform/.gitignore

любые директории вида:
/terraform/.terraform/ 
/terraform/any_directory/.terraform/

хотя если честно - не очень понятно - почему бы не указать просто .terraform/ , ведь написано, что
шаблоны применяются рекурсивно для всего дерева каталогов.
пока листал документацию - появился вариант - если написать .terraform/ - то только корневая директория
/terraform/.terraform/ в этом случае будет игнорироваться,

`**/.terraform/*`

файлы, заканчивающиеся на .tfstate и содержащие .tfstate. в любых директориях ниже /terraform/
`*.tfstate`
`*.tfstate.*`

файлы crash.log в любых директориях ниже /terraform/
`crash.log`

файлы override.tf override.tf.json в любых директориях ниже /terraform/ 
а также файлы, оканчивающиеся на _override.tf и _override.tf.json, причём в любых поддиректориях
`override.tf`
`override.tf.json`
`*_override.tf`
`*_override.tf.json`

если раскомментировать следующую строчку, то указанные после символа "!" файлы будут копироваться.
`!example_override.tf`

если раскомментировать эту строчку, то будет проигнорирован любой файл, в названии которого встречается
tfplan, неважно где - в середине, начале или конце названия. Причём в любой поддиректории.
`*tfplan*`

# Игнорируются указанные ниже файлы в любой поддиректории ниже /terraform/
.terraformrc
terraform.rc
New line

Let's change this file again!