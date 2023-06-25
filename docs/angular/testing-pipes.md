# Тестирование труб

Вы можете протестировать [pipes](guide/pipes) без использования утилит тестирования Angular.

<div class="alert is-helpful">

Если вы хотите поэкспериментировать с приложением, которое описано в этом руководстве, <live-example name="testing" noDownload>запустите его в браузере</live-example> или <live-example name="testing" downloadOnly>скачайте и запустите его локально</live-example>.

</div>

## Тестирование `TitleCasePipe`.

Класс pipe имеет один метод, `transform`, который манипулирует входным значением в преобразованное выходное значение. Реализация `transform` редко взаимодействует с DOM.

Большинство труб не зависят от Angular, кроме метаданных `@Pipe` и интерфейса.

Рассмотрим `TitleCasePipe`, который выводит первую букву каждого слова. Вот реализация с регулярным выражением.

<code-example header="app/shared/title-case.pipe.ts" path="testing/src/app/shared/title-case.pipe.ts"></code-example>.

Все, что использует регулярное выражение, стоит тщательно протестировать. Используйте простой Jasmine для изучения ожидаемых и побочных случаев.

<code-example header="app/shared/title-case.pipe.spec.ts" path="testing/src/app/shared/title-case.pipe.spec.ts" region="excerpt"></code-example>

<a id="write-tests"></a>

## Написание тестов DOM для поддержки теста трубы

Это тесты трубы _в изоляции_. Они не могут определить, правильно ли работает `TitleCasePipe` в компонентах приложения.

Рассмотрите возможность добавления тестов компонентов, таких как этот:

<code-example header="app/hero/hero-detail.component.spec.ts (pipe test)" path="testing/src/app/hero/hero-detail.component.spec.ts" region="title-case-pipe"></code-example>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
