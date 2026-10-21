# Short defense notes

## English speech — approximately two minutes

In Week 6, I studied a controlled AI model backdoor and its connection to a Python execution scenario.

First, I trained a small convolutional neural network on CIFAR-10. It classifies images into ten categories. The retained notebook run achieved 71.69 percent accuracy on normal test images.

Next, I made a copy of the model. During three additional training epochs, ten percent of the training images received a red X and the target label airplane. The X uses a thirty-percent red blend only on its marked pixels.

The modified model achieved 72.32 percent accuracy on normal images. Its targeted attack success rate was 39.48 percent. This rate excludes images whose real class is already airplane. The attack therefore worked on some inputs, not all inputs. The first cat example did not change to airplane. I then selected a successful dog example from the first five hundred test rows.

For the application demonstration, I connected the observed prediction change to a separate Python component. It sent fictional JSON to a local HTTP server in the same Colab runtime. The server returned status two hundred and the response RECEIVED. The CNN did not send the request itself, and no real information left the runtime.

I use MITRE ATLAS for the model-poisoning steps. For the explicit Python extension, I study ATT&CK T1059.006 under Execution. This is a laboratory emulation, not an unauthorized compromise or a reverse shell.

The main lesson is that normal-image accuracy alone does not describe all model behavior. However, my submitted run lacks a clean-model trigger control and repeated trials. These are important next measurements, not results I claim to have already completed.

## Ответы на частые вопросы

**Где сам бэкдор?** В изменённых весах копии CNN: при дообучении она частично усвоила связь между X и классом airplane. В ней не спрятан исполняемый shell.

**Откуда 39,48%?** Из выполненной ячейки оценки: доля предсказаний airplane на изображениях с X, настоящие метки которых не airplane. Это не доля утечек и не точность всей модели.

**Почему у изменённой модели accuracy выше?** В этом запуске разница +0,63 процентного пункта. Копию дополнительно обучали три эпохи; без равного по бюджету контрольного обучения и повторов нельзя приписать улучшение отравлению.

**Почему собаку выбрали отдельно?** Первая кошка не дала нужного результата. Код искал первый успешный пример среди первых 500 тестовых изображений. Это демонстрационный выбор, а не случайная выборка для оценки ASR.

**Почему уверенность 41,20%, а ответ всё равно airplane?** Это максимальный softmax-балл среди десяти классов. Максимум не обязан превышать 50%. Он не является проверенной вероятностью компрометации.

**А здоровая модель тоже ошибается на X?** В исходном сохранённом эксперименте это не измерялось. Поэтому чистый эффект отравления не отделён полностью от эффекта самой картинки. Второй ноутбук позволяет выполнить такой дополнительный контроль.

**Кто отправил JSON?** Явно написанный Python-код после проверки изменения класса. Сам `forward()` CNN возвращает числа и не обращается к сети.

**Был reverse shell?** Нет. Строки `whoami` и `simulated-user` были напечатаны. Это не выполненная удалённая команда.

**Чем отличается от Week 4?** Там разбирали опубликованный кейс небезопасной загрузки модели. Здесь обучили свою модель и исследовали поведение весов. Это разные механизмы риска AI supply chain.

**Какое главное ограничение ATT&CK mapping?** T1059.006 относится к отдельному Python-компоненту. Отравление весов описано ATLAS, а не выдано за автоматическое выполнение Python из файла модели.
