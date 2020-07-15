# Домашнее задание к занятию «2.4. Инструменты Git»

Для выполнения заданий в этом разделе давайте склонируем репозиторий с исходным кодом терраформа https://github.com/hashicorp/terraform 

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.
1. Какому тегу соответствует коммит `85024d3`?
1. Сколько родителей у коммита `b8d720`? Напишите их хеши.
1. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами  v0.12.23 и v0.12.24.
1. Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит так `func providerSource(...)` (вместо троеточего перечислены аргументы).
1. Найдите все коммиты в которых была изменена функция `globalPluginDirs`.
1. Кто автор функции `synchronizedWriters`? 

# Ответы
1. Ответ: команда - `git show aefea'. Хеш - aefead2207ef7e2aa5dc81a34aedf0cad4c32545 , комментарий - Update CHANGELOG.md
1. Ответ: команда - `git show 85024d3`, ответ в 1-й строке `tag: v0.12.23`
1. Ответ: команда - `git show b8d720`, ответ во 2-й строке `Merge: 56cd7859e 9ea88f22f`, 2 родителя
1. Ответ: команда - `git log v0.12.23^..v0.12.24 --oneline` (чтобы показало и сами коммиты 23 и 24. Результаты вывода: 

`33ff1c03b (tag: v0.12.24) v0.12.24
b14b74c49 [Website] vmc provider links
3f235065b Update CHANGELOG.md
6ae64e247 registry: Fix panic when server is unreachable
5c619ca1b website: Remove links to the getting started guide's old location
06275647e Update CHANGELOG.md
d5f9411f5 command: Fix bug when using terraform login on Windows
4b6d06cc5 Update CHANGELOG.md
dd01a3507 Update CHANGELOG.md
225466bc3 Cleanup after v0.12.23 release
85024d310 (tag: v0.12.23) v0.12.23`

5. Ответ: команда - `git log -S'func providerSource' --patch`, в коммите `8c928e83589d90a031f811fae52a81be7153e82f`
6. 
